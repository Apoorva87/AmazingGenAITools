---
name: research
description: Launch a deep research project on any technical topic — produces graduate-level learning artifacts
user_invocable: true
arguments:
  - name: topic
    description: "Topic string, file path to a topic list (.md/.txt), or comma-separated topics"
    required: true
  - name: depth
    description: "Depth contract: survey, advanced_explainer, graduate_note, implementation_handbook, research_frontier (default: graduate_note)"
    required: false
  - name: labs
    description: "Whether to include hands-on labs: yes/no (default: yes)"
    required: false
  - name: phase
    description: "Force re-run a specific phase: understand, research, blueprint. Useful for re-invoking blueprint for more detail."
    required: false
  - name: cleanup
    description: "Archive metadata files after user confirms: yes/no (default: no)"
    required: false
---

# /research — Deep Technical Research & Learning Blueprint

You are the entry point for the Technical Learning Research Agent System. Given a topic, you set up a research project, create the folder structure, and dispatch the research orchestrator to run a multi-phase pipeline that produces a graduate-level learning blueprint.

## Inputs

- **topic**: `$topic` — one of:
  - A single topic string (e.g., `"MLX inference batching"`)
  - A file path ending in `.md` or `.txt` (reads one topic per line or bullet)
  - Comma-separated topics (e.g., `"CORS, CSRF, XSS"`)
- **depth**: `$depth` — depth contract. Default: `graduate_note`
- **labs**: `$labs` — include labs. Default: `yes`
- **phase**: `$phase` — force re-run a specific phase (optional)
- **cleanup**: `$cleanup` — archive metadata (optional)

---

## Step 1: Parse the Input

Determine the input mode:

### 1a. File path mode
If `$topic` ends with `.md` or `.txt`, read the file. Extract topics from:
- Lines starting with `- ` or `* ` (bullet lists)
- Non-empty lines (one topic per line)
- Ignore lines starting with `#` (comments/headings)

### 1b. Comma-separated mode
If `$topic` contains commas, split on `,` and trim each entry.

### 1c. Single topic mode
Otherwise, treat the entire string as one topic.

Report what you found:
```
Input mode: [single | file | comma-separated]
Topics found: N
  1. Topic A
  2. Topic B
  ...
```

---

## Step 2: Generate Slug and Check for Existing Project

For each topic:

1. Generate a URL-safe slug: lowercase, replace spaces and special characters with hyphens, collapse multiple hyphens, max 50 characters. Examples:
   - `"MLX inference batching"` → `mlx-inference-batching`
   - `"CORS/CSRF attacks"` → `cors-csrf-attacks`

2. Check if `personal/research/<slug>/` already exists:
   - **If exists AND no `$phase` argument**: This is a **resume**. Tell the user:
     ```
     Found existing project: personal/research/<slug>/
     Resuming from last checkpoint.
     ```
     Skip to Step 4 (dispatch orchestrator).
   - **If exists AND `$phase` argument provided**: This is a **re-run**. Tell the user:
     ```
     Found existing project: personal/research/<slug>/
     Re-running phase: $phase
     ```
     Skip to Step 4.
   - **If does not exist**: Continue to Step 3.

---

## Step 3: Create Folder Structure

Create the full project directory tree:

```bash
mkdir -p personal/research/<slug>/00_project
mkdir -p personal/research/<slug>/01_research/source_notes
mkdir -p personal/research/<slug>/01_research/papers
mkdir -p personal/research/<slug>/01_research/snapshots
mkdir -p personal/research/<slug>/01_research/experiments
mkdir -p personal/research/<slug>/02_outline
mkdir -p personal/research/<slug>/03_content/sections
mkdir -p personal/research/<slug>/04_visuals/diagrams
mkdir -p personal/research/<slug>/04_visuals/flowcharts
mkdir -p personal/research/<slug>/04_visuals/formulas
mkdir -p personal/research/<slug>/05_labs
mkdir -p personal/research/<slug>/06_build/site
mkdir -p personal/research/<slug>/07_review
```

Initialize `.phase_status.json`:

```json
{
  "understand": { "status": "pending" },
  "research": { "status": "pending" },
  "blueprint": { "status": "pending" },
  "hypothesis_mode": false,
  "created_at": "<ISO-8601 now>",
  "last_updated": "<ISO-8601 now>"
}
```

Write it to `personal/research/<slug>/.phase_status.json`.

Report:
```
Created project: personal/research/<slug>/
Folder structure initialized.
Phase status: all pending.
```

---

## Step 4: Handle Multiple Topics

If more than one topic was parsed:

Present the list and ask:
```
Multiple topics detected:
  1. Topic A
  2. Topic B
  3. Topic C

Start with which topic? (Enter number, or "all" for sequential processing)
```

Process topics sequentially — complete one before starting the next.

---

## Step 5: Dispatch the Orchestrator

Invoke the `research-orchestrator` agent with context. Pass the following information in your dispatch prompt:

- `project_dir`: `personal/research/<slug>`
- `topic`: the topic string
- `depth`: `$depth` or `graduate_note` if not specified
- `labs`: `$labs` or `yes` if not specified
- `phase`: `$phase` if provided (for forced re-run)
- `cleanup`: `$cleanup` if provided

The orchestrator will take over from here, managing the multi-phase pipeline with approval checkpoints.

---

## Step 6: Handle Cleanup (if requested)

If `$cleanup` is `yes`, the orchestrator will handle archival at the end of its run. This step is only noted here for completeness — the orchestrator manages the actual archival process after user confirmation.

---

## Error Handling

- **File not found**: If a topic file path does not exist, tell the user and stop.
- **Empty topic**: If no topics are parsed, tell the user the input was empty and stop.
- **Slug collision with different topic**: If the slug exists but the stored `brief.json` has a different `primary_topic`, append a numeric suffix to the slug (e.g., `attention-mechanism-2`).
- **Permission errors**: If directory creation fails, report the error and stop.
