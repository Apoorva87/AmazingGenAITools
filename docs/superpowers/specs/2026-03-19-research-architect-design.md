# Research Architect — Agent A Design Spec

## Context

The Personal Learning OS currently supports knowledge *capture* (raw notes → concept graph → explore/suggest). This spec adds knowledge *generation*: given a topic, the system performs deep web research, curates sources with user approval, and produces a graduate-level learning blueprint. This is the first increment — Agent A (Research Architect) only. Agents B (Learning Composer) and C (Lab Builder) will follow.

## Architecture

**3-phase pipeline with JSON state files and an optional hypothesis-testing loop.**

```
User → /research <topic>
  → research-orchestrator (asks: hypothesis mode? → dispatches phases)
    → Phase 1: UNDERSTAND (intake + decompose)
      ⏸ USER APPROVAL
    → Phase 2: RESEARCH (search + curate + optional hypothesis loop)
      ⏸ USER APPROVAL
    → Phase 3: BLUEPRINT (outline + plans)
```

Each phase agent gets a fresh context window via the Agent tool. All inter-phase communication is via JSON files on disk. The orchestrator is a thin dispatcher that reads `.phase_status.json` to determine progress and can resume at any checkpoint.

## Durability & Re-entrancy Guarantees

These are hard rules — no agent may violate them:

### 1. No intermediate file deletion
Agents **never delete** files they or other agents created. Every JSON state file, source note, search query log, and hypothesis result is permanent by default. Phases append and update; they never truncate or remove.

### 2. Resume from any interruption
If the orchestrator or any phase agent stops mid-execution (crash, timeout, user interrupt, context limit):
- `.phase_status.json` reflects the last completed state
- Re-running `/research <same-topic>` detects the existing project folder
- The orchestrator reads `.phase_status.json` and resumes at the last incomplete phase
- Within the research phase: `source_catalog.json` tracks which nodes have been searched. On resume, already-processed nodes are skipped; only uncovered nodes are searched.
- Within the hypothesis loop: `hypothesis_results.json` tracks tested hypotheses. On resume, already-tested hypotheses are skipped.

### 3. Source provenance is permanent
`source_catalog.json`, `approved_sources.json`, `rejected_sources.json`, and `source_notes/` are **never auto-deleted**. These form the provenance chain — every claim in the final artifact traces back to a source. Even after the learning artifact is complete, sources remain for:
- Future re-invocations to pull better examples
- Cross-referencing with other research projects
- Auditing which sources informed which sections

### 4. Blueprint is re-entrant
`research-phase-blueprint` can be invoked **multiple times** on the same project. Each invocation:
- Reads the latest state from all prior phases
- Can produce more verbose output if asked
- Can re-examine `source_notes/` and `source_catalog.json` for better examples or deeper coverage
- Can follow source links to fetch additional detail
- Writes updated outline files (previous versions are preserved as `master_outline.v1.md`, `master_outline.v2.md`, etc.)

The orchestrator supports a `--phase blueprint` flag to re-run just the blueprint without re-running understand or research.

### 5. Optional cleanup (user-initiated only)
The user can explicitly request metadata cleanup after they are satisfied with the final output. This is **never automatic**. When requested:
- Move `01_research/` contents to `01_research/.archive/`
- Move `00_project/` intermediate files to `00_project/.archive/`
- Keep `02_outline/` and all final artifacts intact
- Or: keep everything as-is for future reference (default)

The orchestrator should ask: "Would you like to archive the research metadata, or keep it for future reference?" Only after the user explicitly confirms archival does any metadata move.

## Components

### 1. Entry Skill: `/research`

**File:** `skills/research/SKILL.md`

**Arguments:**
- `topic` (required): topic string, file path to topic list, or comma-separated topics
- `depth` (optional): survey | advanced_explainer | graduate_note | implementation_handbook | research_frontier. Default: graduate_note
- `labs` (optional): yes | no. Default: yes
- `phase` (optional): force re-run a specific phase (understand | research | blueprint). Useful for re-invoking blueprint for more detail or to re-research with different parameters.
- `cleanup` (optional): archive metadata files after user confirms satisfaction. Default: no

**Behavior:**
1. Parse input (3 modes: single string, file path, comma-separated)
2. Generate URL-safe slug (lowercase, hyphens, max 50 chars)
3. Check for existing project folder (resume if exists)
4. Create folder structure under `personal/research/<slug>/`
5. If multiple topics: present list, ask user which to start with (or process sequentially)
6. For each topic: initialize `.phase_status.json` with phases: understand, research, blueprint
7. Dispatch `research-orchestrator` agent for the current topic. Multi-topic processing is sequential — complete one topic before starting the next.

### 2. Orchestrator: `research-orchestrator`

**File:** `agents/research-orchestrator.md`
**Tools:** Bash, Read, Write, Glob, Grep, Agent

**Behavior:**
1. Read `.phase_status.json` to determine current state
2. If a `phase` argument was passed (e.g., `phase=blueprint`), skip directly to that phase regardless of status. This enables:
   - Re-running blueprint for more verbose output or better examples
   - Re-running research with different parameters
   - The re-run reads all existing state files from prior phases
3. If first run, ask user: "Enable hypothesis testing mode for this research project?" → save to `user_preferences.json`
4. Find next incomplete phase (or the forced phase from step 2)
5. Check approval gates (between phases, present summary of previous phase output)
6. Dispatch phase agent via Agent tool with project directory context
7. After return, verify completion, loop or finish
8. On completion, present final summary of all outputs
9. If `cleanup` was requested, ask user to confirm, then archive metadata (see Durability section)

**Approval gate summaries:**
- After UNDERSTAND: "Topic graph has N nodes. M prerequisites identified. Review and approve."
- After RESEARCH: "Found N sources (T1: X, T2: Y, T3: Z). N approved, M rejected. [If hypothesis mode: K hypotheses tested, J supported.]"

**Resume:** Re-running `/research <same-topic>` detects existing folder, invokes orchestrator, which picks up at the last incomplete phase.

**Re-entry:** Running `/research <same-topic> phase=blueprint` re-runs the blueprint phase using the latest research data. This is useful for:
- Getting more detailed section plans
- Asking the agent to trace specific source links for better examples
- Regenerating the outline after the user has reviewed and wants changes
- Previous blueprint versions are preserved as `master_outline.v1.md`, etc.

### 3. Phase 1 Agent: `research-phase-understand`

**File:** `agents/research-phase-understand.md`
**Tools:** Bash, Read, Write, WebSearch, WebFetch

**Behavior:**

*Intake:*
1. Quick WebSearch (3-5 queries) to classify the topic: domain (theory/systems/security/applied-ml/economics), standard subtopics, maturity
2. Generate structured brief
3. Ask user 2-3 refinement questions:
   - Prior knowledge (affects prerequisite inclusion)
   - Emphasis: formalism vs implementation vs balanced
   - Must-include sources
   - Output format preference: HTML (hierarchical, clickable pages) or Markdown

*Decompose:*
4. Build topic graph with typed nodes:
   - `prerequisite` — must understand first
   - `core` — essential concepts
   - `advanced` — deeper material
   - `implementation` — practical how-to
   - `pitfall` — common mistakes
   - `open_question` — unresolved/debated
   - `use_case` — real-world applications
5. Build directed edges: requires, related, extends, implements, contrasts
6. Detect prerequisite gaps against user's prior knowledge
7. Present unsatisfied prerequisites, ask which the user already knows

**Outputs:**
- `00_project/brief.json`
- `00_project/user_preferences.json`
- `00_project/topic_graph.json`

### 4. Phase 2 Agent: `research-phase-research`

**File:** `agents/research-phase-research.md`
**Tools:** Bash, Read, Write, WebSearch, WebFetch, Agent

This is the largest and most complex agent. It performs iterative multi-layer search with optional hypothesis validation.

**Search behavior:**
1. For each topic node (prioritized: core → advanced → prerequisites → implementation):
   - Generate 2-4 queries per source layer:
     - Layer 1 (canonical): official docs, specs, RFCs
     - Layer 2 (academic): papers, surveys (arxiv, semantic scholar)
     - Layer 3 (educational): course notes, university tutorials
     - Layer 4 (explanatory): deep-dive blogs, technical writeups
     - Layer 5 (implementation): code examples, repos, guides
     - Layer 6 (community): discussions, forums (Tier 3, used sparingly)
   - Use Firecrawl skill when available (deep crawl, JS rendering, LLM-optimized output)
   - Primary fallback: WebSearch for discovery, WebFetch for content retrieval
   - The agent should try Firecrawl first; if unavailable, fall back to WebSearch/WebFetch transparently

2. Score each source (all 1-5):
   - `authority_score` — source credibility
   - `depth_score` — coverage depth
   - `clarity_score` — pedagogical quality
   - `recency_score` — freshness (timeless fundamentals get 4)
   - `math_usefulness` — formal content
   - `impl_usefulness` — code/implementation content

3. Assign tiers:
   - **Tier 1:** Official docs, published papers, standards, textbooks (authority ≥ 4)
   - **Tier 2:** Respected blogs, conference talks, course notes (authority = 3)
   - **Tier 3:** Community content, videos, forums (authority ≤ 2)

4. Compute composite score (weights vary by user_preferences.source_preference):
   - paper_heavy: authority(0.3) + depth(0.25) + math(0.2) + clarity(0.15) + recency(0.1)
   - implementation_heavy: impl(0.3) + clarity(0.25) + depth(0.2) + recency(0.15) + authority(0.1)
   - balanced: authority(0.2) + depth(0.2) + clarity(0.2) + recency(0.15) + math(0.1) + impl(0.15)

**Hypothesis loop (optional, if enabled at startup):**

5. Extract testable hypotheses from high-tier sources. A hypothesis is a specific claim that can be validated. Examples:
   - "Dynamic batching outperforms static batching for variable-length sequences on Apple Silicon"
   - "KV-cache memory scales linearly with batch size for multi-head attention"

6. For each hypothesis, dispatch `research-hypothesis-reviewer` agent with:
   - The hypothesis statement
   - Supporting sources
   - Topic classification (determines validation mode)
   - Max validation time/budget

7. Collect results. Loop until: no more hypotheses OR max iterations (configurable, default 5)

**Curation (within same agent):**

8. Group sources by category: Canonical, Deep Explanations, Papers, Implementation, Videos, Repos
9. Present each with: title, URL, author, why selected, difficulty, unique value, foundational vs supplementary, tier badge
10. User can: approve all, exclude by number, force-include a URL, switch to paper-heavy or impl-heavy ranking
11. Process selections

**Outputs:**
- `01_research/search_queries.md`
- `01_research/source_catalog.json`
- `01_research/approved_sources.json`
- `01_research/rejected_sources.json`
- `01_research/source_notes/<source-slug>.md` (for Tier 1-2 sources)
- `01_research/hypothesis_results.json` (if hypothesis mode enabled)

### 5. Hypothesis Reviewer: `research-hypothesis-reviewer`

**File:** `agents/research-hypothesis-reviewer.md`
**Tools:** Bash, Read, Write, WebSearch, WebFetch

This agent is dispatched by `research-phase-research` to validate a single hypothesis. It operates in one of two modes based on topic classification:

**Code experiment mode (systems/ML/applied topics):**
1. Design a minimal experiment to test the hypothesis
2. Write Python/shell code in a temporary workspace
3. Run the experiment, collect metrics
4. Compare results against the hypothesis
5. Report: supported/refuted/inconclusive + evidence (numbers, charts, logs)

**Research validation mode (theory/economics/emerging topics):**
1. Search for additional evidence supporting or refuting the hypothesis
2. Find contradicting papers or implementations
3. Check for consensus vs disagreement in the literature
4. Report: supported/refuted/inconclusive + evidence (citations, quotes, data points)

**Output:** Returns structured result to the calling agent:
```json
{
  "hypothesis": "string",
  "verdict": "supported | refuted | inconclusive",
  "confidence": 0.8,
  "mode": "code_experiment | research_validation",
  "evidence": ["string"],
  "code_artifacts": ["path"] | null,
  "sources_consulted": ["url"],
  "notes": "string"
}
```

### 6. Phase 3 Agent: `research-phase-blueprint`

**File:** `agents/research-phase-blueprint.md`
**Tools:** Bash, Read, Write

**Behavior:**
1. Read all prior state: brief, preferences, topic_graph, approved_sources, hypothesis_results
2. Generate learning objectives (scaled to depth contract):
   - survey: 3-4 high-level objectives
   - graduate_note: 5-7 objectives including derivation and implementation
   - research_frontier: 7+ objectives including open problems
3. Design section hierarchy using 3-layer model for each core concept:
   - **Intuition:** What is this? Why does it exist? Mental model / analogy
   - **Formalism:** Definitions, math, equations, proofs, assumptions
   - **Engineering reality:** What breaks in practice? Real tradeoffs?
4. Topological sort of topic graph edges → linear reading order respecting prerequisites
5. Map approved sources → sections (primary and secondary per section)
6. Plan visuals: one diagram per major conceptual jump, one formula block per math claim, one worked example per hard abstraction
7. Classify topic for lab suggestions:
   - theory-heavy → "reproduce the derivation" labs
   - systems-heavy → "build a minimal implementation" labs (suggest benchmarks, demo servers)
   - security-heavy → sandboxed attack/defense demos (e.g., CSRF with server+client+malicious client)
   - applied-ML → benchmark notebooks, profiling, mini-implementations
8. Read `user_preferences.json.output_format` for HTML/MD preference (already captured in Phase 1). Ask only about code demos: "Which sections should include code demos?"
9. If hypothesis results exist, incorporate validated hypotheses as "experimentally confirmed" annotations

**Outputs:**
- `02_outline/master_outline.md` — hierarchical section outline with numbers
- `02_outline/dependency_map.json` — topologically sorted reading order
- `02_outline/section_plan.md` — per-section: objective, prerequisites, depth, formulas, diagrams, examples, sources, lab relevance
- `02_outline/visuals_plan.md` — every diagram needed with description, type, section
- `02_outline/labs_plan.md` — each lab: title, objective, prerequisites, tools, difficulty, sections reinforced
- `00_project/learning_objectives.md`

## Folder Structure

```
personal/research/<topic-slug>/
  .phase_status.json              ← orchestrator's progress tracker
  00_project/
    brief.json                    ← normalized topic + metadata
    user_preferences.json         ← output format, depth, emphasis, sources
    topic_graph.json              ← decomposed topic with typed nodes + edges
    learning_objectives.md        ← generated by blueprint phase
  01_research/
    search_queries.md             ← all queries executed, organized by node
    source_catalog.json           ← full catalog with scores
    approved_sources.json         ← user-approved subset
    rejected_sources.json         ← rejected with reasons
    hypothesis_results.json       ← hypothesis test outcomes (optional)
    source_notes/                 ← per-source summaries for Tier 1-2
    papers/                       ← downloaded papers (future)
    snapshots/                    ← page snapshots (future)
  02_outline/
    master_outline.md             ← hierarchical learning outline
    dependency_map.json           ← topological reading order
    section_plan.md               ← detailed per-section plan
    visuals_plan.md               ← diagram/formula plan
    labs_plan.md                  ← practical demos plan
  03_content/                     ← Agent B (future increment)
  04_visuals/                     ← Agent B (future increment)
  05_labs/                        ← Agent C (future increment)
  06_build/                       ← Agent B (future increment)
  07_review/                      ← Agent B (future increment)
```

## JSON Schemas

### .phase_status.json
```json
{
  "understand": { "status": "complete", "completed_at": "ISO-8601", "output_files": [] },
  "research": { "status": "in_progress", "started_at": "...", "queries_completed": 14, "queries_total": 20 },
  "blueprint": { "status": "pending" },
  "hypothesis_mode": true,
  "created_at": "ISO-8601",
  "last_updated": "ISO-8601"
}
```
Statuses: `pending`, `in_progress`, `awaiting_approval`, `complete`, `failed`

### brief.json
```json
{
  "primary_topic": "string",
  "related_topics": ["string"],
  "depth": "survey | advanced_explainer | graduate_note | implementation_handbook | research_frontier",
  "audience_level": "undergraduate | graduate | researcher | practitioner",
  "format": "markdown | html",
  "labs_wanted": true,
  "classification": "theory | systems | security | applied-ml | economics | other",
  "domain_tags": ["string"],
  "estimated_scope": "small | medium | large",
  "created_at": "ISO-8601"
}
```

### user_preferences.json
```json
{
  "output_format": "markdown | html",
  "depth_contract": "string",
  "citation_mode": "inline | footnote | bibliography",
  "source_preference": "paper_heavy | implementation_heavy | balanced",
  "prior_knowledge": ["string"],
  "must_include_sources": ["url"],
  "exclude_topics": ["string"],
  "emphasis": "formalism | implementation | intuition | balanced",
  "hypothesis_mode": true
}
```

### topic_graph.json
```json
{
  "nodes": [
    {
      "id": "slug",
      "name": "Human Name",
      "type": "prerequisite | core | advanced | implementation | pitfall | open_question | use_case",
      "description": "1-2 sentences",
      "estimated_depth": "intro | intermediate | research",
      "prerequisite_satisfied": false,
      "tags": ["string"]
    }
  ],
  "edges": [
    {
      "source": "node-id",
      "target": "node-id",
      "type": "requires | related | extends | implements | contrasts",
      "weight": 0.8
    }
  ],
  "metadata": {
    "total_nodes": 0,
    "total_edges": 0,
    "unsatisfied_prerequisites": ["node-id"],
    "estimated_sections": 0,
    "created_at": "ISO-8601"
  }
}
```

### source_catalog.json
```json
{
  "sources": [
    {
      "id": "slug",
      "title": "string",
      "url": "string",
      "author": "string | null",
      "publisher": "string | null",
      "date": "string | null",
      "source_type": "documentation | paper | course_notes | blog | video | repo | forum | book",
      "tier": 1,
      "authority_score": 5,
      "depth_score": 4,
      "clarity_score": 4,
      "recency_score": 3,
      "math_usefulness": 2,
      "impl_usefulness": 4,
      "composite_score": 3.8,
      "status": "pending | approved | rejected",
      "rejection_reason": "string | null",
      "notes": "why this source is valuable",
      "unique_value": "what this offers that others don't",
      "difficulty": "beginner | intermediate | advanced",
      "foundational": true,
      "sections_covered": ["node-id"],
      "discovered_via": "query string",
      "fetched": true,
      "fetch_error": null
    }
  ],
  "metadata": {
    "total_sources": 0,
    "tier_counts": { "1": 0, "2": 0, "3": 0 },
    "queries_executed": 0,
    "nodes_covered": 0,
    "nodes_uncovered": ["node-id"],
    "created_at": "ISO-8601"
  }
}
```

### hypothesis_results.json
```json
{
  "hypotheses": [
    {
      "id": "hyp-001",
      "statement": "string",
      "source_id": "source that generated this hypothesis",
      "verdict": "supported | refuted | inconclusive",
      "confidence": 0.8,
      "mode": "code_experiment | research_validation",
      "evidence": ["string"],
      "code_artifacts": ["relative path"] | null,
      "sources_consulted": ["url"],
      "notes": "string",
      "tested_at": "ISO-8601"
    }
  ],
  "metadata": {
    "total_tested": 0,
    "supported": 0,
    "refuted": 0,
    "inconclusive": 0
  }
}
```

## Source Quality Policy

### Tier Assignment
- **Tier 1:** Official docs, published papers, standards/specs, textbooks, university lecture notes. These are authoritative and should dominate the learning artifact.
- **Tier 2:** Respected engineering blogs, conference talks with substance, deep technical writeups, repo docs from authoritative maintainers. Good for explanation and context.
- **Tier 3:** Videos, forum discussions, Stack Overflow, Reddit, social posts. Use ONLY to clarify edge cases, find examples, discover repos, locate pain points.

### Timeless vs Recent
- Fundamentals (math, theory, algorithms): prefer timeless sources even if old
- Implementation details (tooling, APIs, frameworks): prefer recent sources
- The source_catalog tracks this via `recency_score` — timeless fundamentals get a score of 4 (not penalized for age)

## Implementation Order

1. `skills/research/SKILL.md` — entry point, folder creation
2. `agents/research-orchestrator.md` — dispatcher, phase tracking, approval gates
3. `agents/research-phase-understand.md` — intake + decompose
4. `agents/research-phase-research.md` — search + curate + hypothesis dispatch
5. `agents/research-hypothesis-reviewer.md` — hypothesis validation
6. `agents/research-phase-blueprint.md` — outline + plans
7. Symlinks in `.claude/skills/` and `.claude/agents/`

## Verification

1. Run `/research "attention mechanism"` → verify folder created with correct structure
2. Verify Phase 1 produces valid brief.json, user_preferences.json, topic_graph.json
3. Verify Phase 2 performs web searches, scores sources, presents for approval
4. Verify hypothesis loop dispatches and returns results (when enabled)
5. Verify Phase 3 produces master_outline.md with source-backed sections
6. Test resume: interrupt mid-Phase 2, re-run, verify it picks up correctly
7. Test multi-topic: provide comma-separated topics, verify sequential processing
