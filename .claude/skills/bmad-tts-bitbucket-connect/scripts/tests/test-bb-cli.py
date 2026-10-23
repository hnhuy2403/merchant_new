#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Unit tests for bb-cli.py — pure helpers (no network).

Covers Cloud + Server flavor logic: state mapping, participant summarization
(both shapes), PR slimming (both shapes), payload building (both shapes),
flavor detection, and Server REST base URL resolution.

Run: python3 scripts/tests/test-bb-cli.py
Exits non-zero on failure.
"""

import importlib.util
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


def _load_bb_cli():
    here = Path(__file__).resolve().parent.parent
    spec = importlib.util.spec_from_file_location("bb_cli", here / "bb-cli.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bb = _load_bb_cli()


# ─── State mapping ──────────────────────────────────────────────────────────

class NormalizeStateTests(unittest.TestCase):
    def test_known_states(self):
        self.assertEqual(bb._normalize_state("OPEN"), "open")
        self.assertEqual(bb._normalize_state("MERGED"), "merged")
        self.assertEqual(bb._normalize_state("DECLINED"), "closed_unmerged")
        self.assertEqual(bb._normalize_state("SUPERSEDED"), "closed_unmerged")

    def test_unknown_state(self):
        self.assertEqual(bb._normalize_state("BANANA"), "unknown")
        self.assertEqual(bb._normalize_state(""), "unknown")


# ─── Cloud participant summary ──────────────────────────────────────────────

class CloudParticipantTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(
            bb._summarize_participants_cloud([]),
            {"approvals": 0, "changes_requested": 0, "pending_reviewers": 0},
        )

    def test_only_non_reviewers_ignored(self):
        ps = [
            {"role": "PARTICIPANT", "approved": True},
            {"role": "AUTHOR", "approved": True},
        ]
        self.assertEqual(
            bb._summarize_participants_cloud(ps),
            {"approvals": 0, "changes_requested": 0, "pending_reviewers": 0},
        )

    def test_mixed_reviewer_states(self):
        ps = [
            {"role": "REVIEWER", "approved": True},
            {"role": "REVIEWER", "approved": False, "state": "changes_requested"},
            {"role": "REVIEWER", "approved": False, "state": None},
            {"role": "REVIEWER", "approved": False},
            {"role": "PARTICIPANT", "approved": True},  # ignored
        ]
        self.assertEqual(
            bb._summarize_participants_cloud(ps),
            {"approvals": 1, "changes_requested": 1, "pending_reviewers": 2},
        )

    def test_back_compat_alias(self):
        # _summarize_participants is the back-compat alias → must equal _cloud variant.
        ps = [{"role": "REVIEWER", "approved": True}]
        self.assertEqual(bb._summarize_participants(ps), bb._summarize_participants_cloud(ps))


# ─── Server participant summary (different shape) ───────────────────────────

class ServerParticipantTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(
            bb._summarize_participants_server([]),
            {"approvals": 0, "changes_requested": 0, "pending_reviewers": 0},
        )

    def test_status_enum_dispatch(self):
        # Server reviewers have `approved` (bool) AND `status` (UNAPPROVED/APPROVED/NEEDS_WORK).
        rs = [
            {"approved": True, "status": "APPROVED"},          # approved
            {"approved": False, "status": "APPROVED"},         # approved (status wins)
            {"approved": False, "status": "NEEDS_WORK"},       # changes requested
            {"approved": False, "status": "UNAPPROVED"},       # pending
            {"approved": False},                                # pending (no status)
        ]
        self.assertEqual(
            bb._summarize_participants_server(rs),
            {"approvals": 2, "changes_requested": 1, "pending_reviewers": 2},
        )


# ─── Cloud slim PR ──────────────────────────────────────────────────────────

class SlimPRCloudTests(unittest.TestCase):
    def test_minimum_fields(self):
        pr = {
            "id": 42,
            "title": "Add feature X",
            "state": "OPEN",
            "updated_on": "2026-05-06T10:00:00+00:00",
            "links": {"html": {"href": "https://bitbucket.org/ws/repo/pull-requests/42"}},
            "source": {"branch": {"name": "features/3-2-foo-dev"}},
            "destination": {"branch": {"name": "features/3-2-foo"}},
            "participants": [],
        }
        slim = bb._slim_pr_cloud(pr)
        self.assertEqual(slim["id"], 42)
        self.assertEqual(slim["state"], "open")
        self.assertEqual(slim["raw_state"], "OPEN")
        self.assertIsNone(slim["merged_at"])
        self.assertEqual(slim["url"], "https://bitbucket.org/ws/repo/pull-requests/42")
        self.assertEqual(slim["source_branch"], "features/3-2-foo-dev")
        self.assertEqual(slim["destination_branch"], "features/3-2-foo")
        self.assertEqual(slim["review_summary"]["approvals"], 0)

    def test_merged_pr_carries_timestamp(self):
        pr = {
            "id": 7,
            "state": "MERGED",
            "updated_on": "2026-05-05T08:30:00+00:00",
            "links": {},
            "source": {"branch": {"name": "x-dev"}},
            "destination": {"branch": {"name": "x"}},
            "participants": [{"role": "REVIEWER", "approved": True}],
        }
        slim = bb._slim_pr_cloud(pr)
        self.assertEqual(slim["state"], "merged")
        self.assertEqual(slim["merged_at"], "2026-05-05T08:30:00+00:00")
        self.assertEqual(slim["review_summary"]["approvals"], 1)

    def test_back_compat_alias(self):
        pr = {"id": 1, "state": "OPEN", "links": {}, "source": {}, "destination": {}, "participants": []}
        self.assertEqual(bb._slim_pr(pr), bb._slim_pr_cloud(pr))


# ─── Server slim PR (different shape) ───────────────────────────────────────

class SlimPRServerTests(unittest.TestCase):
    def test_open_pr(self):
        pr = {
            "id": 17,
            "title": "Design 3-2",
            "state": "OPEN",
            "links": {"self": [{"href": "http://bitbucket.example/projects/VSS/repos/r/pull-requests/17"}]},
            "fromRef": {"displayId": "features/3-2-foo-dev", "id": "refs/heads/features/3-2-foo-dev"},
            "toRef": {"displayId": "features/3-2-foo", "id": "refs/heads/features/3-2-foo"},
            "reviewers": [{"approved": True, "status": "APPROVED"}],
        }
        slim = bb._slim_pr_server(pr)
        self.assertEqual(slim["id"], 17)
        self.assertEqual(slim["state"], "open")
        self.assertEqual(slim["raw_state"], "OPEN")
        self.assertIsNone(slim["merged_at"])
        self.assertEqual(slim["url"], "http://bitbucket.example/projects/VSS/repos/r/pull-requests/17")
        self.assertEqual(slim["source_branch"], "features/3-2-foo-dev")
        self.assertEqual(slim["destination_branch"], "features/3-2-foo")
        self.assertEqual(slim["review_summary"]["approvals"], 1)

    def test_merged_pr_uses_closedDate(self):
        pr = {
            "id": 3,
            "state": "MERGED",
            "closedDate": 1714978800000,
            "links": {"self": [{"href": "http://bb/pr/3"}]},
            "fromRef": {"displayId": "x-dev"},
            "toRef": {"displayId": "x"},
            "reviewers": [],
        }
        slim = bb._slim_pr_server(pr)
        self.assertEqual(slim["state"], "merged")
        self.assertEqual(slim["merged_at"], 1714978800000)

    def test_missing_self_links_yields_none_url(self):
        pr = {"id": 1, "state": "OPEN", "links": {}, "fromRef": {}, "toRef": {}, "reviewers": []}
        slim = bb._slim_pr_server(pr)
        self.assertIsNone(slim["url"])
        self.assertIsNone(slim["source_branch"])
        self.assertIsNone(slim["destination_branch"])


# ─── Flavor detection + URL helpers ─────────────────────────────────────────

class FlavorDetectionTests(unittest.TestCase):
    def test_cloud_url(self):
        self.assertEqual(bb._detect_flavor("https://api.bitbucket.org/2.0"), "cloud")

    def test_server_url(self):
        self.assertEqual(bb._detect_flavor("http://bitbucket.digital.vn"), "server")
        self.assertEqual(bb._detect_flavor("https://internal-bb.example.com"), "server")

    def test_resolve_flavor_explicit_override(self):
        # Explicit --api-flavor wins over URL detection.
        args = SimpleNamespace(api_flavor="server", api_base_url="https://api.bitbucket.org/2.0")
        self.assertEqual(bb._resolve_flavor(args), "server")

    def test_resolve_flavor_auto_from_url(self):
        args = SimpleNamespace(api_flavor=None, api_base_url="https://api.bitbucket.org/2.0")
        self.assertEqual(bb._resolve_flavor(args), "cloud")
        args = SimpleNamespace(api_flavor=None, api_base_url="http://bitbucket.digital.vn")
        self.assertEqual(bb._resolve_flavor(args), "server")


class ServerRestBaseTests(unittest.TestCase):
    def test_appends_rest_path(self):
        self.assertEqual(bb._server_rest_base("http://bb.example"), "http://bb.example/rest/api/1.0")

    def test_strips_trailing_slash(self):
        self.assertEqual(bb._server_rest_base("http://bb.example/"), "http://bb.example/rest/api/1.0")

    def test_idempotent_when_already_includes_rest_path(self):
        self.assertEqual(bb._server_rest_base("http://bb.example/rest/api/1.0"), "http://bb.example/rest/api/1.0")


# ─── PR-create payload builders ─────────────────────────────────────────────

class PrCreatePayloadTests(unittest.TestCase):
    def test_cloud_minimal(self):
        args = SimpleNamespace(title="t", source="s", dest="d", close_source_branch=False)
        payload = bb._pr_create_payload_cloud(args, "body", [])
        self.assertEqual(payload["title"], "t")
        self.assertEqual(payload["description"], "body")
        self.assertEqual(payload["source"], {"branch": {"name": "s"}})
        self.assertEqual(payload["destination"], {"branch": {"name": "d"}})
        self.assertNotIn("reviewers", payload)
        self.assertNotIn("close_source_branch", payload)

    def test_cloud_with_reviewers_and_close(self):
        args = SimpleNamespace(title="t", source="s", dest="d", close_source_branch=True)
        payload = bb._pr_create_payload_cloud(args, "body", ["{a-b-c}", "{d-e-f}"])
        self.assertEqual(payload["reviewers"], [{"uuid": "{a-b-c}"}, {"uuid": "{d-e-f}"}])
        self.assertTrue(payload["close_source_branch"])

    def test_server_minimal_uses_refs_heads(self):
        args = SimpleNamespace(title="Design 3-2", source="features/3-2-foo-dev",
                               dest="features/3-2-foo", workspace="VSS", repository="repo-x")
        payload = bb._pr_create_payload_server(args, "body", [])
        self.assertEqual(payload["title"], "Design 3-2")
        self.assertEqual(payload["fromRef"]["id"], "refs/heads/features/3-2-foo-dev")
        self.assertEqual(payload["toRef"]["id"], "refs/heads/features/3-2-foo")
        self.assertEqual(payload["fromRef"]["repository"]["slug"], "repo-x")
        self.assertEqual(payload["fromRef"]["repository"]["project"]["key"], "VSS")
        self.assertEqual(payload["state"], "OPEN")
        self.assertNotIn("reviewers", payload)

    def test_server_reviewers_use_user_name(self):
        args = SimpleNamespace(title="t", source="s", dest="d", workspace="P", repository="r")
        payload = bb._pr_create_payload_server(args, "", ["alice", "bob"])
        self.assertEqual(payload["reviewers"], [{"user": {"name": "alice"}}, {"user": {"name": "bob"}}])


# ─── Git remote URL parsing ─────────────────────────────────────────────────

class GitRemoteParserTests(unittest.TestCase):
    def test_cloud_https(self):
        r = bb._parse_git_remote("https://bitbucket.org/myws/myrepo.git")
        self.assertEqual(r["flavor"], "cloud")
        self.assertEqual(r["host"], "bitbucket.org")
        self.assertEqual(r["workspace"], "myws")
        self.assertEqual(r["repository"], "myrepo")
        self.assertEqual(r["api_base_url"], "https://api.bitbucket.org/2.0")

    def test_cloud_https_no_dot_git(self):
        r = bb._parse_git_remote("https://bitbucket.org/myws/myrepo")
        self.assertEqual(r["repository"], "myrepo")

    def test_cloud_ssh_scp_style(self):
        r = bb._parse_git_remote("git@bitbucket.org:myws/myrepo.git")
        self.assertEqual(r["flavor"], "cloud")
        self.assertEqual(r["scheme"], "ssh")
        self.assertEqual(r["workspace"], "myws")
        self.assertEqual(r["repository"], "myrepo")

    def test_server_http_scm_path_uppercases_project_key(self):
        # BBS clone URLs use lowercase project key in /scm/, but the API
        # canonical form is uppercase — parser must normalize.
        r = bb._parse_git_remote("http://bitbucket.digital.vn/scm/vss/vss-catalog-service-bmad.git")
        self.assertEqual(r["flavor"], "server")
        self.assertEqual(r["workspace"], "VSS")
        self.assertEqual(r["repository"], "vss-catalog-service-bmad")
        self.assertEqual(r["api_base_url"], "http://bitbucket.digital.vn")

    def test_server_https_keeps_https_for_api(self):
        r = bb._parse_git_remote("https://bitbucket.example.com/scm/proj/repo.git")
        self.assertEqual(r["api_base_url"], "https://bitbucket.example.com")

    def test_server_ssh_defaults_api_to_https(self):
        # SSH remote → API URL should default to https (safer than http).
        r = bb._parse_git_remote("ssh://git@bitbucket.digital.vn:8081/vss/vss-catalog-service-bmad.git")
        self.assertEqual(r["scheme"], "ssh")
        self.assertEqual(r["api_base_url"], "https://bitbucket.digital.vn")

    def test_server_ssh_scp_style(self):
        r = bb._parse_git_remote("git@bitbucket.digital.vn:vss/repo.git")
        self.assertEqual(r["flavor"], "server")
        self.assertEqual(r["host"], "bitbucket.digital.vn")
        self.assertEqual(r["workspace"], "VSS")
        self.assertEqual(r["repository"], "repo")
        # SSH scp-style → default to https
        self.assertEqual(r["api_base_url"], "https://bitbucket.digital.vn")

    def test_https_with_embedded_credentials_strips_them(self):
        r = bb._parse_git_remote("https://user:secret@bitbucket.digital.vn/scm/p/r.git")
        self.assertEqual(r["host"], "bitbucket.digital.vn")
        self.assertNotIn("secret", str(r))

    def test_rejects_non_bitbucket_host(self):
        # Default mode: host must contain 'bitbucket'.
        self.assertIsNone(bb._parse_git_remote("https://github.com/foo/bar.git"))
        self.assertIsNone(bb._parse_git_remote("git@gitlab.com:foo/bar.git"))

    def test_force_accepts_any_host(self):
        r = bb._parse_git_remote("https://git.example.com/scm/proj/repo.git", accept_any_host=True)
        self.assertIsNotNone(r)
        self.assertEqual(r["flavor"], "server")
        self.assertEqual(r["workspace"], "PROJ")

    def test_empty_or_garbage_url(self):
        self.assertIsNone(bb._parse_git_remote(""))
        self.assertIsNone(bb._parse_git_remote(None))
        self.assertIsNone(bb._parse_git_remote("not-a-url"))


class LooksLikeBitbucketTests(unittest.TestCase):
    def test_exact_cloud_host(self):
        self.assertTrue(bb._looks_like_bitbucket("bitbucket.org"))

    def test_self_hosted_with_bitbucket_in_name(self):
        self.assertTrue(bb._looks_like_bitbucket("bitbucket.digital.vn"))
        self.assertTrue(bb._looks_like_bitbucket("BITBUCKET.example.com"))
        self.assertTrue(bb._looks_like_bitbucket("bb-bitbucket.corp"))

    def test_rejects_other_hosts(self):
        self.assertFalse(bb._looks_like_bitbucket("github.com"))
        self.assertFalse(bb._looks_like_bitbucket("gitlab.example.com"))
        self.assertFalse(bb._looks_like_bitbucket(""))
        self.assertFalse(bb._looks_like_bitbucket(None))


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    sys.exit(0 if result.wasSuccessful() else 1)
