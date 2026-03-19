---
name: learn-suggest
description: Suggest learning tools to fill representation gaps for concepts in your knowledge graph
user_invocable: true
arguments:
  - name: concept
    description: Concept name/ID to get suggestions for, or "all" to scan everything
    required: true
---

# Learn-Suggest Skill

You analyze the user's concept graph to find representation gaps and suggest specific learning tools to fill them. The graph lives at `personal/learning/concept_graph.json` (relative to the repo root). The Python module at `plugins/concept-graph/` provides all operations you need.

## Loading the Graph

Always start by loading the graph with a Python snippet via Bash:

```bash
python3 -c "
import sys, json
sys.path.insert(0, 'plugins/concept-graph')
import graph as G
g = G.load('personal/learning/concept_graph.json')
# ... your analysis here ...
"
```

Run all Python from the **repo root directory**: `/Users/akarnik/experiments/AmazingGenAITools/.worktrees/learning-os`

If the graph file does not exist yet, `G.load()` returns an empty graph. In that case, tell the user their graph is empty and suggest using `/learn-process` to add content first.

## Step 1: Resolve the Target Concepts

### Single concept — `/learn-suggest "flash attention"`

Find the concept by name or ID:

```python
matches = G.find_nodes(g, type="concept", text="<concept>")
```

If no match, try a broader text search across all node types. If still nothing, tell the user the concept was not found and suggest checking with `/learn-explore`.

If multiple matches, list them and ask the user to pick one.

### All concepts — `/learn-suggest all`

Gather every concept node:

```python
concepts = G.find_nodes(g, type="concept")
```

Sort by gap severity (most missing representations first), then by lowest confidence. This prioritizes the concepts that need the most help.

## Step 2: Analyze Each Concept

For each target concept, collect the following context:

```python
node = concepts[0]  # or matched concept
reps = node.get("representations", {})
missing_reps = [k for k, v in reps.items() if v is None]
present_reps = [k for k, v in reps.items() if v is not None]
confidence = node.get("confidence", 1)
depth = node.get("depth", "intro")

# Get connected resources
neighbors = G.get_neighbors(g, node["id"])
resources = [n for n in neighbors if n.get("type") == "resource"]
resource_types = [r.get("resource_type") for r in resources]
has_video = "video" in resource_types
has_paper = "paper" in resource_types

# Check for related concepts (to gauge research depth)
related = [n for n in neighbors if n.get("type") == "concept"]
```

## Step 3: Generate Suggestions Using the Tool Catalog

Apply these rules in order. For each gap, suggest 1-2 tools with reasoning.

### Missing: audio representation (`"audio": None`)

**Suggest:**
- **NotebookLM (podcast mode)** — Upload the concept's existing resources and generate an audio overview. Best when there are 2+ text resources available.
- **ElevenLabs** or **Speechify** — Convert an existing summary into audio for passive listening. Best when a summary already exists.

*Reasoning to show the user:* "No audio representation exists. Listening to explanations reinforces learning through a different modality."

### Missing: summary (`"summary": None`)

**Suggest:**
- **Claude (deep reasoning)** — Feed the concept's resources and ask for a structured summary with key insights, relationships, and open questions.
- **NotebookLM (multi-doc synthesis)** — When there are 3+ resources, use NotebookLM to synthesize across them into a unified summary.

*Reasoning:* "No summary exists. A summary anchors understanding and makes the concept reviewable at a glance."

### Missing: diagram (`"diagram": None`)

**Suggest:**
- **Mermaid** — Generate code-based diagrams (flowcharts, sequence diagrams, class diagrams) directly in markdown. Best for process flows and hierarchies.
- **Mapify** — Create a mind map showing how this concept relates to its neighbors. Best for exploring the concept's position in the graph.
- **Excalidraw** — Hand-drawn-style diagrams for architecture or system overviews.

*Reasoning:* "No diagram exists. Visual representations help clarify structure and relationships that text alone may obscure."

### Missing: flashcards (`"flashcards": None`)

**Suggest:**
- **Anki + FSRS** — Generate spaced-repetition flashcards from the concept's summary and key questions. FSRS scheduling optimizes review timing.
- **RemNote** — Integrated note-taking and flashcard creation. Good when the concept has detailed notes.
- **LectureScribe** — Auto-generate flashcards from video or lecture resources.

*Reasoning:* "No flashcards exist. Active recall via spaced repetition is the most effective method for long-term retention."

### Low confidence (1-2) AND has resources

This means the user has material but hasn't internalized the concept yet.

**Suggest:**
- **SciSpace** — Re-read the original papers/resources with AI-assisted explanation of difficult passages.
- **Perplexity** — Get alternative explanations and cross-referenced sources to build understanding from a different angle.

*Reasoning:* "Confidence is low despite having resources. Alternative explanations or deeper engagement with existing material may help."

### Research depth AND no related papers

The concept is at research depth but lacks academic backing.

**Suggest:**
- **Elicit** — Run a literature review to find foundational and recent papers on this concept.
- **Consensus** — Validate specific claims or findings related to this concept against the research literature.

*Reasoning:* "This is a research-depth concept without linked papers. Academic sources will deepen and validate understanding."

### Has video resources

Enhance existing video resources with summaries.

**Suggest:**
- **Eightify** — Summarize linked YouTube videos into key points and timestamps. Saves re-watching time and creates reviewable notes.

*Reasoning:* "Video resources exist but may not have been distilled into reviewable text. Video summarization bridges the gap."

## Step 4: Present Suggestions Interactively

Format the output as a numbered list grouped by concept. For each suggestion, show:

```
### [Concept Name] (confidence: X/5, depth: Y)

Missing representations: summary, diagram, audio, flashcards

1. **[Tool Name]** — [Gap it fills]
   Why: [One sentence on why this matters for this concept]
   Action: [Brief step — what to feed it, what to do]
   Input: [Which specific resources from the graph to use]
   [APPROVE] [DISMISS]

2. **[Tool Name]** — [Gap it fills]
   ...
```

When in "all" mode, limit output to the **top 10 concepts by gap severity**. Mention the total count and offer to show more.

After presenting, ask:
> "Which suggestions would you like to approve? You can say 'approve 1, 3, 5' or 'approve all'. Approved items become task nodes in your graph."

## Step 5: Handle Approvals

When the user approves suggestions, create task nodes in the graph for each one:

```python
import graph as G

g = G.load('personal/learning/concept_graph.json')

# Create a task node for each approved suggestion
task = {
    "id": "task-<concept_id>-<tool_name_slug>",
    "name": "Create <representation> for <concept_name> using <tool_name>",
    "type": "task",
    "status": "todo",
    "priority": "medium",  # high if confidence <= 2, medium otherwise
    "tags": ["learn-suggest", "<representation_type>", "<tool_name_slug>"],
}
g = G.add_node(g, task)

# Link task to the concept
g = G.add_edge(g, task["id"], node["id"], "action_for",
               context="Fill <representation> gap using <tool_name>")

G.save(g, 'personal/learning/concept_graph.json')
```

Set priority to **high** if the concept's confidence is 1-2, **medium** otherwise.

After creating tasks, confirm what was added:
> "Created X task(s) in your graph. Use `/learn-explore tasks` to see your task queue."

## Step 6: Notion Integration (Optional)

If the user says they want to queue to Notion instead, tell them:
> "To send these to Notion, use `/learn-sync notion` after approving. That will push all todo tasks from the graph to your Notion database."

Do not attempt direct Notion API calls from this skill. Defer to `/learn-sync`.

## Presentation Guidelines

- Be specific about *which* resources from the graph to feed into each tool. Reference them by name and URL if available.
- Prioritize suggestions: missing summary is almost always the highest priority (it enables other representations). Order: summary > flashcards > diagram > audio.
- For "all" mode, sort concepts by: (number of missing reps DESC, confidence ASC, depth DESC). This surfaces the most neglected, least understood, deepest concepts first.
- Keep the tone practical and action-oriented. Each suggestion should feel like a concrete next step, not abstract advice.
- If a concept has zero resources linked, note that resources should be added first before generating representations. Suggest `/learn-process` for ingesting new material.
- When a concept already has all representations filled and high confidence, say so and skip it. Celebrate completeness.
