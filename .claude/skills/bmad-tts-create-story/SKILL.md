---
name: bmad-tts-create-story
description: 'TTS-team variant of create-story. Creates a dedicated story FOLDER under implementation_artifacts containing story.md (dev context), detail-design.md (kiến trúc & thiết kế chi tiết), srs.md (đặc tả + kịch bản nghiệp vụ), and source-code-links.md (Bitbucket + local path + module map). Use when the user says "create the next story", "create story [identifier]", or "/bmad-tts-create-story".'
---

# Create Story Workflow (TTS variant — folder layout)

**Goal:** Create a comprehensive story FOLDER that gives the dev agent everything needed for flawless implementation. Output is a per-story directory with 4 artifacts (story, detail design, SRS, source-code links) instead of a single flat file.

**Your Role:** Story context engine that prevents LLM developer mistakes, omissions, or disasters.
- Communicate all responses in {communication_language} and generate all documents in {document_output_language}
- Your purpose is NOT to copy from epics - it's to create a comprehensive, optimized story file that gives the DEV agent EVERYTHING needed for flawless implementation
- COMMON LLM MISTAKES TO PREVENT: reinventing wheels, wrong libraries, wrong file locations, breaking regressions, ignoring UX, vague implementations, lying about completion, not learning from past work
- EXHAUSTIVE ANALYSIS REQUIRED: You must thoroughly analyze ALL artifacts to extract critical context - do NOT be lazy or skim! This is the most important function in the entire development process!
- UTILIZE SUBPROCESSES AND SUBAGENTS: Use research subagents, subprocesses or parallel processing if available to thoroughly analyze different artifacts simultaneously and thoroughly
- SAVE QUESTIONS: If you think of questions or clarifications during analysis, save them for the end after the complete story is written
- ZERO USER INTERVENTION: Process should be fully automated except for initial epic/story selection or missing documents

## Conventions

- Bare paths (e.g. `discover-inputs.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

### Step 1: Resolve the Workflow Block

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow`

**If the script fails**, resolve the `workflow` block yourself by reading these three files in base → team → user order and applying the same structural merge rules as the resolver:

1. `{skill-root}/customize.toml` — defaults
2. `{project-root}/_bmad/custom/{skill-name}.toml` — team overrides
3. `{project-root}/_bmad/custom/{skill-name}.user.toml` — personal overrides

Any missing file is skipped. Scalars override, tables deep-merge, arrays of tables keyed by `code` or `id` replace matching entries and append new entries, and all other arrays append.

### Step 2: Execute Prepend Steps

Execute each entry in `{workflow.activation_steps_prepend}` in order before proceeding.

### Step 3: Load Persistent Facts

Treat every entry in `{workflow.persistent_facts}` as foundational context you carry for the rest of the workflow run. Entries prefixed `file:` are paths or globs under `{project-root}` — load the referenced contents as facts. All other entries are facts verbatim.

### Step 4: Load Config

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:

- `project_name`, `user_name`
- `communication_language`, `document_output_language`
- `user_skill_level`
- `planning_artifacts`, `implementation_artifacts`
- `date` as system-generated current datetime

### Step 5: Greet the User

Greet `{user_name}`, speaking in `{communication_language}`.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. Begin the workflow below.

## Paths

- `sprint_status` = `{implementation_artifacts}/sprint-status.yaml`
- `epics_file` = `{planning_artifacts}/epics.md`
- `prd_file` = `{planning_artifacts}/prd.md`
- `architecture_file` = `{planning_artifacts}/architecture.md`
- `ux_file` = `{planning_artifacts}/*ux*.md`
- `story_title` = "" (will be elicited if not derivable)
- `story_dir` = `{implementation_artifacts}/{{story_key}}/`
- `default_output_file` = `{story_dir}/story.md`
- `detail_design_file` = `{story_dir}/detail-design.md`
- `srs_file` = `{story_dir}/srs.md`
- `source_code_links_file` = `{story_dir}/source-code-links.md`

## Input Files

| Input | Description | Path Pattern(s) | Load Strategy |
|-------|-------------|------------------|---------------|
| prd | PRD (fallback - epics file should have most content) | whole: `{planning_artifacts}/*prd*.md`, sharded: `{planning_artifacts}/*prd*/*.md` | SELECTIVE_LOAD |
| architecture | Architecture (fallback - epics file should have relevant sections) | whole: `{planning_artifacts}/*architecture*.md`, sharded: `{planning_artifacts}/*architecture*/*.md` | SELECTIVE_LOAD |
| ux | UX design (fallback - epics file should have relevant sections) | whole: `{planning_artifacts}/*ux*.md`, sharded: `{planning_artifacts}/*ux*/*.md` | SELECTIVE_LOAD |
| epics | Enhanced epics+stories file with BDD and source hints | whole: `{planning_artifacts}/*epic*.md`, sharded: `{planning_artifacts}/*epic*/*.md` | SELECTIVE_LOAD |

## Execution

<workflow>

<step n="1" goal="Determine target story">
  <check if="{{story_path}} is provided by user or user provided the epic and story number such as 2-4 or 1.6 or epic 1 story 5">
    <action>Parse user-provided story path: extract epic_num, story_num, story_title from format like "1-2-user-auth"</action>
    <action>Set {{epic_num}}, {{story_num}}, {{story_key}} from user input</action>
    <action>GOTO step 2a</action>
  </check>

  <action>Check if {{sprint_status}} file exists for auto discover</action>
  <check if="sprint status file does NOT exist">
    <output>🚫 No sprint status file found and no story specified</output>
    <output>
      **Required Options:**
      1. Run `sprint-planning` to initialize sprint tracking (recommended)
      2. Provide specific epic-story number to create (e.g., "1-2-user-auth")
      3. Provide path to story documents if sprint status doesn't exist yet
    </output>
    <ask>Choose option [1], provide epic-story number, path to story docs, or [q] to quit:</ask>

    <check if="user chooses 'q'">
      <action>HALT - No work needed</action>
    </check>

    <check if="user chooses '1'">
      <output>Run sprint-planning workflow first to create sprint-status.yaml</output>
      <action>HALT - User needs to run sprint-planning</action>
    </check>

    <check if="user provides epic-story number">
      <action>Parse user input: extract epic_num, story_num, story_title</action>
      <action>Set {{epic_num}}, {{story_num}}, {{story_key}} from user input</action>
      <action>GOTO step 2a</action>
    </check>

    <check if="user provides story docs path">
      <action>Use user-provided path for story documents</action>
      <action>GOTO step 2a</action>
    </check>
  </check>

  <!-- Auto-discover from sprint status only if no user input -->
  <check if="no user input provided">
    <critical>MUST read COMPLETE {sprint_status} file from start to end to preserve order</critical>
    <action>Load the FULL file: {{sprint_status}}</action>
    <action>Read ALL lines from beginning to end - do not skip any content</action>
    <action>Parse the development_status section completely</action>

    <action>Find the FIRST story (by reading in order from top to bottom) where:
      - Key matches pattern: number-number-name (e.g., "1-2-user-auth")
      - NOT an epic key (epic-X) or retrospective (epic-X-retrospective)
      - Status value equals "backlog"
    </action>

    <check if="no backlog story found">
      <output>📋 No backlog stories found in sprint-status.yaml

        All stories are either already created, in progress, or done.

        **Options:**
        1. Run sprint-planning to refresh story tracking
        2. Load PM agent and run correct-course to add more stories
        3. Check if current sprint is complete and run retrospective
      </output>
      <action>HALT</action>
    </check>

    <action>Extract from found story key (e.g., "1-2-user-authentication"):
      - epic_num: first number before dash (e.g., "1")
      - story_num: second number after first dash (e.g., "2")
      - story_title: remainder after second dash (e.g., "user-authentication")
    </action>
    <action>Set {{story_id}} = "{{epic_num}}.{{story_num}}"</action>
    <action>Store story_key for later use (e.g., "1-2-user-authentication")</action>

    <!-- Mark epic as in-progress if this is first story -->
    <action>Check if this is the first story in epic {{epic_num}} by looking for {{epic_num}}-1-* pattern</action>
    <check if="this is first story in epic {{epic_num}}">
      <action>Load {{sprint_status}} and check epic-{{epic_num}} status</action>
      <action>If epic status is "backlog" → update to "in-progress"</action>
      <action>If epic status is "contexted" (legacy status) → update to "in-progress" (backward compatibility)</action>
      <action>If epic status is "in-progress" → no change needed</action>
      <check if="epic status is 'done'">
        <output>🚫 ERROR: Cannot create story in completed epic</output>
        <output>Epic {{epic_num}} is marked as 'done'. All stories are complete.</output>
        <output>If you need to add more work, either:</output>
        <output>1. Manually change epic status back to 'in-progress' in sprint-status.yaml</output>
        <output>2. Create a new epic for additional work</output>
        <action>HALT - Cannot proceed</action>
      </check>
      <check if="epic status is not one of: backlog, contexted, in-progress, done">
        <output>🚫 ERROR: Invalid epic status '{{epic_status}}'</output>
        <output>Epic {{epic_num}} has invalid status. Expected: backlog, in-progress, or done</output>
        <output>Please fix sprint-status.yaml manually or run sprint-planning to regenerate</output>
        <action>HALT - Cannot proceed</action>
      </check>
      <output>📊 Epic {{epic_num}} status updated to in-progress</output>
    </check>

    <action>GOTO step 2a</action>
  </check>
  <action>Load the FULL file: {{sprint_status}}</action>
  <action>Read ALL lines from beginning to end - do not skip any content</action>
  <action>Parse the development_status section completely</action>

  <action>Find the FIRST story (by reading in order from top to bottom) where:
    - Key matches pattern: number-number-name (e.g., "1-2-user-auth")
    - NOT an epic key (epic-X) or retrospective (epic-X-retrospective)
    - Status value equals "backlog"
  </action>

  <check if="no backlog story found">
    <output>No backlog stories found in sprint-status.yaml

      All stories are either already created, in progress, or done.

      **Options:**
      1. Run sprint-planning to refresh story tracking
      2. Load PM agent and run correct-course to add more stories
      3. Check if current sprint is complete and run retrospective
    </output>
    <action>HALT</action>
  </check>

  <action>Extract from found story key (e.g., "1-2-user-authentication"):
    - epic_num: first number before dash (e.g., "1")
    - story_num: second number after first dash (e.g., "2")
    - story_title: remainder after second dash (e.g., "user-authentication")
  </action>
  <action>Set {{story_id}} = "{{epic_num}}.{{story_num}}"</action>
  <action>Store story_key for later use (e.g., "1-2-user-authentication")</action>

  <!-- Mark epic as in-progress if this is first story -->
  <action>Check if this is the first story in epic {{epic_num}} by looking for {{epic_num}}-1-* pattern</action>
  <check if="this is first story in epic {{epic_num}}">
    <action>Load {{sprint_status}} and check epic-{{epic_num}} status</action>
    <action>If epic status is "backlog" → update to "in-progress"</action>
    <action>If epic status is "contexted" (legacy status) → update to "in-progress" (backward compatibility)</action>
    <action>If epic status is "in-progress" → no change needed</action>
    <check if="epic status is 'done'">
      <output>ERROR: Cannot create story in completed epic</output>
      <output>Epic {{epic_num}} is marked as 'done'. All stories are complete.</output>
      <output>If you need to add more work, either:</output>
      <output>1. Manually change epic status back to 'in-progress' in sprint-status.yaml</output>
      <output>2. Create a new epic for additional work</output>
      <action>HALT - Cannot proceed</action>
    </check>
    <check if="epic status is not one of: backlog, contexted, in-progress, done">
      <output>ERROR: Invalid epic status '{{epic_status}}'</output>
      <output>Epic {{epic_num}} has invalid status. Expected: backlog, in-progress, or done</output>
      <output>Please fix sprint-status.yaml manually or run sprint-planning to regenerate</output>
      <action>HALT - Cannot proceed</action>
    </check>
    <output>Epic {{epic_num}} status updated to in-progress</output>
  </check>

  <action>GOTO step 2a</action>
</step>

<step n="2" goal="Load and analyze core artifacts">
  <critical>🔬 EXHAUSTIVE ARTIFACT ANALYSIS - This is where you prevent future developer mistakes!</critical>

  <!-- Load all available content through discovery protocol -->
  <action>Read fully and follow `./discover-inputs.md` to load all input files</action>
  <note>Available content: {epics_content}, {prd_content}, {architecture_content}, {ux_content}, plus the project-context facts loaded during activation via `persistent_facts`.</note>

  <!-- Analyze epics file for story foundation -->
  <action>From {epics_content}, extract Epic {{epic_num}} complete context:</action> **EPIC ANALYSIS:** - Epic
  objectives and business value - ALL stories in this epic for cross-story context - Our specific story's requirements, user story
  statement, acceptance criteria - Technical requirements and constraints - Dependencies on other stories/epics - Source hints pointing to
  original documents <!-- Extract specific story requirements -->
  <action>Extract our story ({{epic_num}}-{{story_num}}) details:</action> **STORY FOUNDATION:** - User story statement
  (As a, I want, so that) - Detailed acceptance criteria (already BDD formatted) - Technical requirements specific to this story -
  Business context and value - Success criteria <!-- Previous story analysis for context continuity -->
  <check if="story_num > 1">
    <action>Find {{previous_story_num}}: scan {implementation_artifacts} for the story file in epic {{epic_num}} with the highest story number less than {{story_num}}</action>
    <action>Load previous story file: {implementation_artifacts}/{{epic_num}}-{{previous_story_num}}-*.md</action> **PREVIOUS STORY INTELLIGENCE:** -
  Dev notes and learnings from previous story - Review feedback and corrections needed - Files that were created/modified and their
  patterns - Testing approaches that worked/didn't work - Problems encountered and solutions found - Code patterns established <action>Extract
  all learnings that could impact current story implementation</action>
  </check>

  <!-- Git intelligence for previous work patterns -->
  <check
    if="previous story exists AND git repository detected">
    <action>Get last 5 commit titles to understand recent work patterns</action>
    <action>Analyze 1-5 most recent commits for relevance to current story:
      - Files created/modified
      - Code patterns and conventions used
      - Library dependencies added/changed
      - Architecture decisions implemented
      - Testing approaches used
    </action>
    <action>Extract actionable insights for current story implementation</action>
  </check>
</step>

<step n="3" goal="Architecture analysis for developer guardrails">
  <critical>🏗️ ARCHITECTURE INTELLIGENCE - Extract everything the developer MUST follow!</critical> **ARCHITECTURE DOCUMENT ANALYSIS:** <action>Systematically
  analyze architecture content for story-relevant requirements:</action>

  <!-- Load architecture - single file or sharded -->
  <check if="architecture file is single file">
    <action>Load complete {architecture_content}</action>
  </check>
  <check if="architecture is sharded to folder">
    <action>Load architecture index and scan all architecture files</action>
  </check> **CRITICAL ARCHITECTURE EXTRACTION:** <action>For
  each architecture section, determine if relevant to this story:</action> - **Technical Stack:** Languages, frameworks, libraries with
  versions - **Code Structure:** Folder organization, naming conventions, file patterns - **API Patterns:** Service structure, endpoint
  patterns, data contracts - **Database Schemas:** Tables, relationships, constraints relevant to story - **Security Requirements:**
  Authentication patterns, authorization rules - **Performance Requirements:** Caching strategies, optimization patterns - **Testing
  Standards:** Testing frameworks, coverage expectations, test patterns - **Deployment Patterns:** Environment configurations, build
  processes - **Integration Patterns:** External service integrations, data flows <action>Extract any story-specific requirements that the
  developer MUST follow</action>
  <action>Identify any architectural decisions that override previous patterns</action>

  <!-- Read existing code being modified — non-negotiable -->
  <critical>📂 READ FILES BEING MODIFIED — skipping this is the primary cause of implementation failures and review cycles</critical>
  <action>From the architecture directory structure, identify every file marked UPDATE (not NEW) that this story will touch</action>
  <action>Read each relevant UPDATE file completely. For each one, document in dev notes:
    - Current state: what it does today (state machine, API calls, data shapes, existing behaviors)
    - What this story changes: the specific sections or behaviors being modified
    - What must be preserved: existing interactions and behaviors the story must not break
  </action>
  <critical>A story implementation must leave the system working end-to-end — not just satisfy its stated ACs.
  If a behavior is required for the feature to work correctly in the existing system, it is a requirement
  whether or not it is explicitly written in the story. The dev agent owns this.</critical>
</step>

<step n="4" goal="Web research for latest technical specifics">
  <critical>🌐 ENSURE LATEST TECH KNOWLEDGE - Prevent outdated implementations!</critical> **WEB INTELLIGENCE:** <action>Identify specific
  technical areas that require latest version knowledge:</action>

  <!-- Check for libraries/frameworks mentioned in architecture -->
  <action>From architecture analysis, identify specific libraries, APIs, or
  frameworks</action>
  <action>For each critical technology, research latest stable version and key changes:
    - Latest API documentation and breaking changes
    - Security vulnerabilities or updates
    - Performance improvements or deprecations
    - Best practices for current version
  </action>
  **EXTERNAL CONTEXT INCLUSION:** <action>Include in story any critical latest information the developer needs:
    - Specific library versions and why chosen
    - API endpoints with parameters and authentication
    - Recent security patches or considerations
    - Performance optimization techniques
    - Migration considerations if upgrading
  </action>
</step>

<step n="5" goal="Create comprehensive story file">
  <critical>📝 CREATE ULTIMATE STORY FILE - The developer's master implementation guide!</critical>

  <action>Ensure the story directory exists: create `{{story_dir}}` if missing (mkdir -p semantics)</action>

  <action>Initialize from template.md:
  {default_output_file}</action>
  <template-output file="{default_output_file}">story_header</template-output>

  <!-- Story foundation from epics analysis -->
  <template-output
    file="{default_output_file}">story_requirements</template-output>

  <!-- Developer context section - MOST IMPORTANT PART -->
  <template-output file="{default_output_file}">
  developer_context_section</template-output> **DEV AGENT GUARDRAILS:** <template-output file="{default_output_file}">
  technical_requirements</template-output>
  <template-output file="{default_output_file}">architecture_compliance</template-output>
  <template-output
    file="{default_output_file}">library_framework_requirements</template-output>
  <template-output file="{default_output_file}">
  file_structure_requirements</template-output>
  <template-output file="{default_output_file}">testing_requirements</template-output>

  <!-- Previous story intelligence -->
  <check
    if="previous story learnings available">
    <template-output file="{default_output_file}">previous_story_intelligence</template-output>
  </check>

  <!-- Git intelligence -->
  <check
    if="git analysis completed">
    <template-output file="{default_output_file}">git_intelligence_summary</template-output>
  </check>

  <!-- Latest technical specifics -->
  <check if="web research completed">
    <template-output file="{default_output_file}">latest_tech_information</template-output>
  </check>

  <!-- Project context reference -->
  <template-output
    file="{default_output_file}">project_context_reference</template-output>

  <!-- Final status update -->
  <template-output file="{default_output_file}">
  story_completion_status</template-output>

  <!-- CRITICAL: Set status to ready-for-dev -->
  <action>Set story Status to: "ready-for-dev"</action>
  <action>Add completion note: "Ultimate
  context engine analysis completed - comprehensive developer guide created"</action>
</step>

<step n="5b" goal="Generate companion implementation documents">
  <critical>📁 IMPLEMENTATION FOLDER ARTIFACTS — populate detail-design, SRS, and source-code-links from analysis already performed in steps 2-4. Reuse extracted context; do NOT re-analyze artifacts.</critical>

  <!-- Detail Design -->
  <action>Initialize {detail_design_file} from `assets/detail-design-template.md` — copy template content as-is, then for each `{{detail_design_*}}` placeholder, fill from architecture extraction (step 3) and story foundation (step 2).</action>
  <action>Filling rules for detail-design:
    - Use `{document_output_language}` for all generated prose.
    - If a section has insufficient context, replace the placeholder with `[CẦN BỔ SUNG: <one-line reason>]` instead of leaving it blank or hallucinating.
    - Preserve all headings exactly. Do NOT delete sections even if empty — leave the placeholder marker so reviewers see the gap.
    - Tables: use markdown table syntax. If only one row, still use table format.
  </action>
  <action>Save {detail_design_file}</action>

  <!-- SRS -->
  <action>Initialize {srs_file} from `assets/srs-template.md` — fill `{{srs_*}}` placeholders from epic/PRD analysis (step 2) and acceptance criteria.</action>
  <action>Filling rules for SRS:
    - `srs_acceptance_criteria`: copy ACs from epic verbatim, prefix each with `AC-1`, `AC-2`, ... preserving the original BDD wording.
    - `srs_scenario_*`: derive Given/When/Then scenarios that map to the ACs. Identify edge cases the developer might miss (boundary values, concurrent actions, error states) — these are scenarios that MUST exist for the system to work end-to-end even if not literally in ACs.
    - `srs_business_rules`: extract invariants from PRD or epic; if none stated, derive from domain knowledge in `persistent_facts` or `project-context.md`.
    - Same gap-handling rule as detail-design: use `[CẦN BỔ SUNG: ...]` markers, do not invent.
  </action>
  <action>Save {srs_file}</action>

  <!-- Source Code Links -->
  <action>Initialize {source_code_links_file} from `assets/source-code-links-template.md`.</action>
  <action>Resolve repository facts (best-effort, in this order):
    1. Read `{project-root}/_bmad/config.user.yaml` and locate `tts.bitbucket` section if present. Extract `api_base_url`, `workspace`, and any configured `repository`/`repo_slug`.
    2. Run `git -C {project-root} remote get-url origin` to get the canonical remote URL. Convert to web URL:
       - Cloud SSH `git@bitbucket.org:<ws>/<repo>.git` → `https://bitbucket.org/<ws>/<repo>`
       - Cloud HTTPS as-is (strip `.git`)
       - Server/DC SSH `ssh://git@<host>:<port>/<KEY>/<slug>.git` → `https://<host>/projects/<KEY>/repos/<slug>`
       - Server/DC HTTPS `https://<host>/scm/<KEY>/<slug>.git` → `https://<host>/projects/<KEY>/repos/<slug>`
    3. If git command fails or remote is non-Bitbucket, set `src_main_repo_bitbucket_url` to `[CẦN BỔ SUNG: URL Bitbucket — chưa kết nối Bitbucket, chạy /bmad-tts-bitbucket-connect hoặc điền tay]`.
    4. `src_main_repo_local_path`: absolute path of `{project-root}`.
    5. `src_main_repo_name`: prefer the Bitbucket repo slug; fall back to `basename` of project root.
    6. `story_title_slug`: kebab-case of `{{story_title}}`.
  </action>
  <action>Fill `src_modules_affected` from the same UPDATE/NEW file list extracted in step 3. Use the exact table format from the template.</action>
  <action>Fill `src_dependent_repos` and `src_reference_links` if extractable from architecture or PRD; otherwise write `_Không có_` or `[CẦN BỔ SUNG: ...]`.</action>
  <action>Save {source_code_links_file}</action>
</step>

<step n="6" goal="Update sprint status and finalize">
  <action>Validate the newly created story file {default_output_file} against `./checklist.md` and apply any required fixes before finalizing</action>
  <action>Save story document unconditionally</action>

  <!-- Update sprint status -->
  <check if="sprint status file exists">
    <action>Update {{sprint_status}}</action>
    <action>Load the FULL file and read all development_status entries</action>
    <action>Find development_status key matching {{story_key}}</action>
    <action>Verify current status is "backlog" (expected previous state)</action>
    <action>Update development_status[{{story_key}}] = "ready-for-dev"</action>
    <action>Update last_updated field to current date</action>
    <action>Save file, preserving ALL comments and structure including STATUS DEFINITIONS</action>
  </check>

  <action>Report completion</action>
  <output>**🎯 ULTIMATE BMad Method STORY CONTEXT CREATED, {user_name}!**

    **Story Details:**
    - Story ID: {{story_id}}
    - Story Key: {{story_key}}
    - Folder: {{story_dir}}
    - Status: ready-for-dev

    **Generated artifacts (in story folder):**
    - `story.md` — context engine output for the dev agent
    - `detail-design.md` — kiến trúc & thiết kế chi tiết
    - `srs.md` — đặc tả nghiệp vụ + kịch bản
    - `source-code-links.md` — repo / module / Bitbucket links

    **TTS Pipeline — next steps (in order):**
    1. Review the comprehensive story in {{story_dir}}/story.md and the 3 companion docs
    2. Fill in any `[CẦN BỔ SUNG: ...]` markers in detail-design.md / srs.md / source-code-links.md if needed (architect/dev)
    3. Run `/bmad-tts-design-story` to produce the **overall design** (thiết kế tổng thể) — this is REQUIRED before dev-story can run
    4. Run `/bmad-tts-design-story-pr` to open the design review PR on Bitbucket (techlead/SA gate)
    5. Run `/bmad-tts-check-review` to wait until the design PR is approved/merged
    6. Run `/bmad-tts-dev-story` to implement — gated on the design doc existing (HALT otherwise)
    7. Run `/code-review` when complete (auto-marks done)
    8. Optional: If Test Architect module installed, run `/bmad:tea:automate` after `bmad-tts-dev-story` to generate guardrail tests

    **The story folder is ready. Design phase is the next gate before code can be written.**
  </output>
  <action>Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete` — if the resolved value is non-empty, follow it as the final terminal instruction before exiting.</action>
</step>

</workflow>
