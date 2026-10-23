#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pymysql>=1.1"]
# ///
"""
Direct DB test runner for the qc module — connects straight to MySQL/MariaDB
(NO MCP server) and executes DB-only test cases, returning the raw outputs so
the QC agent can judge Pass/Fail against each case's "Kết quả mong muốn".

Design split:
  - This script is DUMB + SAFE: it runs SQL and reports what happened
    (captured SELECT rows + any SQL errors). It does NOT decide P/F.
  - The QC agent builds the plan, runs this, then compares actual vs expected.

Safety guarantees:
  - Each case runs on its OWN fresh connection with autocommit OFF.
  - Every connection is ROLLED BACK and closed at the end of the case — the DB
    is never mutated, even if the plan forgets a ROLLBACK.
  - Any `COMMIT` statement in the plan is downgraded to a no-op (refuses to
    persist) unless --allow-commit is explicitly passed.
  - Refuses to run if host/db look like production (--prod-guard, on by default).

Connection source (no MCP runtime needed — we only borrow the params):
  Reads .claude/settings.local.json -> mcpServers.<server>.env
  (MYSQL_HOST / MYSQL_PORT / MYSQL_USER / MYSQL_PASS / MYSQL_DB).
  Override any field with --host/--port/--user/--password/--db.

Subcommands:
    smoke [--config PATH] [--server mysql] [conn overrides]
        Connect and SHOW TABLES — verify connectivity. Prints JSON.

    run --plan PLAN_JSON [--out ACTUAL_JSON] [--config PATH] [--server mysql]
        [--allow-commit] [--no-prod-guard] [conn overrides]
        Execute every case in PLAN_JSON, emit ACTUAL_JSON (or stdout).

PLAN_JSON schema:
    {
      "sheet": "1.2-merchant-db",                 # optional, informational
      "cases": [
        {
          "id": "MER-001",
          "skip": false,                          # optional; true => not run
          "skip_reason": "cần 2 phiên đồng thời", # optional
          "statements": [
            {"sql": "BEGIN"},
            {"sql": "INSERT INTO merchants (...) VALUES (...)"},
            {"sql": "SELECT @x := LAST_INSERT_ID() AS new_id", "capture": "b3"},
            {"sql": "SELECT * FROM merchants WHERE merchant_id=@x", "capture": "b4"},
            {"sql": "ROLLBACK"}
          ]
        }
      ]
    }

ACTUAL_JSON schema:
    {
      "connection": {"host": "...", "port": 4006, "db": "...", "ok": true},
      "cases": {
        "MER-001": {
          "ran": true,
          "captures": {"b3": {"columns": [...], "rows": [[...]]}, ...},
          "errors": [{"stmt_index": 1, "sqlstate": "23000", "code": 4025,
                      "message": "CONSTRAINT ... failed"}],
          "fatal": null
        },
        ...
      }
    }
"""
import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pymysql


def load_conn_params(args):
    params = {"host": None, "port": 3306, "user": None, "password": None, "db": None}
    cfg_path = Path(args.config)
    if cfg_path.exists():
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        env = (
            cfg.get("mcpServers", {})
            .get(args.server, {})
            .get("env", {})
        )
        if env.get("MYSQL_HOST"):
            params["host"] = env["MYSQL_HOST"]
        if env.get("MYSQL_PORT"):
            params["port"] = int(env["MYSQL_PORT"])
        if env.get("MYSQL_USER"):
            params["user"] = env["MYSQL_USER"]
        if env.get("MYSQL_PASS"):
            params["password"] = env["MYSQL_PASS"]
        if env.get("MYSQL_DB"):
            params["db"] = env["MYSQL_DB"]
    # CLI overrides win
    if args.host:
        params["host"] = args.host
    if args.port:
        params["port"] = int(args.port)
    if args.user:
        params["user"] = args.user
    if args.password is not None:
        params["password"] = args.password
    if args.db:
        params["db"] = args.db
    return params


def prod_guard(params, enabled):
    if not enabled:
        return
    blob = f"{params.get('host', '')} {params.get('db', '')}".lower()
    for needle in ("prod", "production"):
        if needle in blob:
            raise SystemExit(
                json.dumps(
                    {"error": f"prod-guard: refusing to connect (host/db contains '{needle}'). "
                              f"Pass --no-prod-guard to override."},
                    ensure_ascii=False,
                )
            )


def connect(params):
    return pymysql.connect(
        host=params["host"],
        port=params["port"],
        user=params["user"],
        password=params["password"],
        database=params["db"],
        autocommit=False,
        charset="utf8mb4",
        connect_timeout=10,
        read_timeout=30,
        write_timeout=30,
    )


def cmd_smoke(args):
    params = load_conn_params(args)
    prod_guard(params, not args.no_prod_guard)
    out = {"host": params["host"], "port": params["port"], "db": params["db"]}
    try:
        conn = connect(params)
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT VERSION() AS v")
                version = cur.fetchone()[0]
                cur.execute("SHOW TABLES")
                tables = [r[0] for r in cur.fetchall()]
            out.update({"ok": True, "version": version,
                        "table_count": len(tables), "tables": tables})
        finally:
            conn.rollback()
            conn.close()
    except Exception as e:  # noqa: BLE001
        out.update({"ok": False, "error": f"{type(e).__name__}: {e}"})
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("ok") else 1


def run_case(conn_params, case, allow_commit, persist=False):
    result = {"ran": True, "captures": {}, "errors": [], "fatal": None}
    if case.get("skip"):
        result["ran"] = False
        result["skip_reason"] = case.get("skip_reason", "")
        return result
    # Multi-session path: open one connection per declared session, dispatch
    # statements to their session, support "async" statements for lock-wait scenarios.
    if case.get("multi_session"):
        if not case.get("allow_commit"):
            result["ran"] = False
            result["fatal"] = "multi_session case requires allow_commit: true (explicit opt-in)"
            return result
        return _run_multi_session_case(conn_params, case, persist=persist)
    try:
        conn = connect(conn_params)
    except Exception as e:  # noqa: BLE001
        result["ran"] = False
        result["fatal"] = f"connect failed: {type(e).__name__}: {e}"
        return result
    try:
        for idx, stmt in enumerate(case.get("statements", [])):
            sql = (stmt.get("sql") or "").strip().rstrip(";").strip()
            if not sql:
                continue
            upper = sql.upper()
            if upper == "COMMIT" and not (allow_commit or persist):
                # never persist
                continue
            if upper == "ROLLBACK" and persist:
                # persist mode: skip ROLLBACK so the case's INSERT/UPDATE survives
                continue
            cap = stmt.get("capture")
            try:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    if cap:
                        if cur.description is not None:
                            cols = [d[0] for d in cur.description]
                            rows = [list(r) for r in cur.fetchall()]
                        else:
                            cols, rows = [], []
                        result["captures"][cap] = {
                            "columns": cols,
                            "rows": _jsonable(rows),
                            "rowcount": cur.rowcount,
                        }
                    else:
                        # drain any result set so the connection stays clean
                        if cur.description is not None:
                            cur.fetchall()
            except pymysql.MySQLError as e:
                code = e.args[0] if e.args else None
                msg = e.args[1] if len(e.args) > 1 else str(e)
                result["errors"].append({
                    "stmt_index": idx,
                    "sql": sql[:200],
                    "code": code,
                    "message": str(msg),
                })
    except Exception as e:  # noqa: BLE001
        result["fatal"] = f"{type(e).__name__}: {e}"
    finally:
        try:
            if persist:
                conn.commit()
            else:
                conn.rollback()
        except Exception:  # noqa: BLE001
            pass
        conn.close()
    return result


def _jsonable(rows):
    out = []
    for r in rows:
        out.append([_cell(c) for c in r])
    return out


def _cell(c):
    import datetime
    import decimal
    if isinstance(c, (datetime.date, datetime.datetime, datetime.time)):
        return c.isoformat(sep=" ")
    if isinstance(c, decimal.Decimal):
        return str(c)
    if isinstance(c, (bytes, bytearray)):
        try:
            return c.decode("utf-8")
        except Exception:  # noqa: BLE001
            return c.hex()
    return c


def _run_multi_session_case(conn_params, case, persist=False):
    """Execute a case that needs concurrent independent sessions (e.g. row-lock
    contention). Each declared `session` gets its own pymysql connection and a
    single-worker thread. Statements run in plan order; statements marked
    `"async": true` are submitted to their session's executor without waiting,
    so they can block on a DB lock while OTHER sessions proceed. Captures named
    via `"capture": "name"` (first row, first column) become `{name}` placeholders
    that subsequent statements substitute literally — used to share newly-inserted
    primary keys across sessions.

    Safety: even when allow_commit=True at case level (required), every session
    is force-rolled-back and closed in finally, so a half-committed state from an
    in-flight async statement still gets cleaned up at session close.
    """
    result = {"ran": True, "captures": {}, "errors": [], "fatal": None, "multi_session": True}
    sessions = {}     # session name -> pymysql connection
    executors = {}    # session name -> ThreadPoolExecutor (1 worker)
    pending = {}      # session name -> Future of last unawaited async stmt
    captures_simple = {}  # capture label -> first-row first-col scalar (for {name} substitution)

    def _ensure_session(name):
        if name in sessions:
            return None
        try:
            sessions[name] = connect(conn_params)
            executors[name] = ThreadPoolExecutor(max_workers=1, thread_name_prefix=f"db-{name}")
            return None
        except Exception as e:  # noqa: BLE001
            return f"session '{name}' connect failed: {type(e).__name__}: {e}"

    def _wait_pending(name):
        fut = pending.pop(name, None)
        if fut is None:
            return
        try:
            fut.result(timeout=30)
        except Exception as e:  # noqa: BLE001
            result["errors"].append({
                "stmt_index": -1, "session": name,
                "message": f"pending async failed: {type(e).__name__}: {e}",
            })

    def _make_exec(conn, sql, idx, cap_label, session_name):
        def _do():
            try:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    if cap_label:
                        if cur.description is not None:
                            cols = [d[0] for d in cur.description]
                            rows = [list(r) for r in cur.fetchall()]
                        else:
                            cols, rows = [], []
                        result["captures"][cap_label] = {
                            "columns": cols,
                            "rows": _jsonable(rows),
                            "rowcount": cur.rowcount,
                            "session": session_name,
                        }
                        if rows and cols:
                            captures_simple[cap_label] = rows[0][0]
                    else:
                        if cur.description is not None:
                            cur.fetchall()
            except pymysql.MySQLError as e:
                code = e.args[0] if e.args else None
                msg = e.args[1] if len(e.args) > 1 else str(e)
                result["errors"].append({
                    "stmt_index": idx, "session": session_name,
                    "sql": sql[:200], "code": code, "message": str(msg),
                })
        return _do

    try:
        for idx, stmt in enumerate(case.get("statements", [])):
            session = stmt.get("session", "default")
            raw_sql = (stmt.get("sql") or "").strip().rstrip(";").strip()
            if not raw_sql:
                continue
            # Persist mode: skip ROLLBACK so this case's data survives for visual review
            if persist and raw_sql.upper() == "ROLLBACK":
                continue
            # Substitute {label} placeholders from prior captures
            sql = re.sub(
                r"\{(\w+)\}",
                lambda m: str(captures_simple.get(m.group(1), m.group(0))),
                raw_sql,
            )
            # Before submitting, drain this session's prior async (preserves order)
            _wait_pending(session)
            err = _ensure_session(session)
            if err:
                result["fatal"] = err
                return result
            conn = sessions[session]
            cap_label = stmt.get("capture")
            is_async = bool(stmt.get("async"))
            fut = executors[session].submit(_make_exec(conn, sql, idx, cap_label, session))
            if is_async:
                pending[session] = fut
            else:
                try:
                    fut.result(timeout=30)
                except Exception as e:  # noqa: BLE001
                    result["errors"].append({
                        "stmt_index": idx, "session": session,
                        "sql": sql[:200], "message": f"sync exec failed: {type(e).__name__}: {e}",
                    })
        # Wait for any remaining async work
        for name in list(pending.keys()):
            _wait_pending(name)
    except Exception as e:  # noqa: BLE001
        result["fatal"] = f"{type(e).__name__}: {e}"
    finally:
        for name, conn in sessions.items():
            try:
                if persist:
                    conn.commit()
                else:
                    conn.rollback()
            except Exception:  # noqa: BLE001
                pass
            try:
                conn.close()
            except Exception:  # noqa: BLE001
                pass
        for name, ex in executors.items():
            try:
                ex.shutdown(wait=False)
            except Exception:  # noqa: BLE001
                pass
    return result


def cmd_run(args):
    params = load_conn_params(args)
    prod_guard(params, not args.no_prod_guard)
    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    out = {
        "connection": {"host": params["host"], "port": params["port"], "db": params["db"]},
        "sheet": plan.get("sheet"),
        "cases": {},
    }
    # connectivity probe first
    try:
        c = connect(params)
        c.rollback()
        c.close()
        out["connection"]["ok"] = True
    except Exception as e:  # noqa: BLE001
        out["connection"]["ok"] = False
        out["connection"]["error"] = f"{type(e).__name__}: {e}"
        _emit(out, args)
        return 1

    persist = getattr(args, "no_rollback", False)
    out["persist"] = persist
    for case in plan.get("cases", []):
        cid = case.get("id", "?")
        out["cases"][cid] = run_case(params, case, args.allow_commit, persist=persist)

    _emit(out, args)
    return 0


def _emit(out, args):
    text = json.dumps(out, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps({"status": "ok", "out": args.out,
                          "cases": len(out.get("cases", {})),
                          "connection_ok": out.get("connection", {}).get("ok")},
                         ensure_ascii=False))
    else:
        print(text)


def add_conn_args(p):
    p.add_argument("--config", default=".claude/settings.local.json",
                   help="JSON file with mcpServers.<server>.env creds (default .claude/settings.local.json)")
    p.add_argument("--server", default="mysql", help="server key inside mcpServers (default mysql)")
    p.add_argument("--host")
    p.add_argument("--port")
    p.add_argument("--user")
    p.add_argument("--password")
    p.add_argument("--db")
    p.add_argument("--no-prod-guard", action="store_true",
                   help="allow connecting even if host/db contain 'prod'")


def main():
    ap = argparse.ArgumentParser(description="Direct (non-MCP) DB test runner for qc module")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("smoke", help="connect + SHOW TABLES")
    add_conn_args(ps)
    ps.set_defaults(func=cmd_smoke)

    pr = sub.add_parser("run", help="execute plan.json against DB")
    pr.add_argument("--plan", required=True)
    pr.add_argument("--out")
    pr.add_argument("--allow-commit", action="store_true",
                    help="permit COMMIT statements to persist (DANGEROUS; default ignores COMMIT)")
    pr.add_argument("--no-rollback", action="store_true",
                    help="KEEP test data in DB after each case for visual review "
                         "(skips ROLLBACK statements, COMMITs at end of each session). "
                         "Implies --allow-commit. Use ONLY on dev/test envs.")
    add_conn_args(pr)
    pr.set_defaults(func=cmd_run)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
