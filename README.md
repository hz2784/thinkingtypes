# Thinking Types — Amplify

A teacher-facing dashboard that transforms existing student assessment data into actionable insights about **how each student thinks** — not just how well they perform.

**[View the Interactive Demo](https://hz2784.github.io/thinkingtypes/)**

---

## Vision

An end-to-end, research-grade pipeline that transforms student work into actionable insights teachers value to improve learning outcomes and validate those outcomes.

```
Eliciting Rich          Capturing         Analyzing/          Making            Useful Reports
Student Data  ───────>  that Data  ────>  Interpreting  ───>  Rigorous   ────>  and
                                          the Data            Claims            Recommendations
```

## The Problem

Traditional assessments tell teachers **how well** a student performs (e.g., "Inferential Reasoning: 4/10"), but not **how** they think. Two students can score identically yet need completely different support. Thinking Types bridges this gap by analyzing patterns across reading and writing data to surface each student's cognitive style.

## Data Collection: What Signals We Use

No new assessments are needed. Thinking Types extracts signals from data Amplify already collects through two existing systems:

### Reading Data — mCLASS / DIBELS 8

| Assessment | Signals Extracted | Used For |
|---|---|---|
| Oral Reading Fluency (ORF) | Words correct, accuracy, self-corrections, error rate | Structure dimension (self-correction patterns indicate metacognitive monitoring) |
| Maze Comprehension | Literal vs. inferential accuracy, answer changes, items attempted | Depth dimension (inferential accuracy) and Evidence dimension (answer changes indicate willingness to reconsider) |

Collected 3x per year (Beginning, Middle, End of Year).

### Writing Data — Amplify ELA Essays

| Data Source | Signals Extracted | Used For |
|---|---|---|
| AWE Scores | Focus, Evidence, Elaboration, Conventions, Language (each 0–4) | Depth dimension (evidence score reflects analytical engagement) |
| Essay Text Analysis | Reasoning sentence count, cross-text references, counterargument presence, evidence source count, connective word diversity, topic sentence structure | All three dimensions — these are the richest signals |
| Revision History | Surface edits vs. structural edits vs. argument edits | Structure dimension (deep revisers show systematic thinking) |

Collected continuously throughout the school year, across multiple curriculum units.

## How We Classify: The Three Dimensions

Every student is scored on three dimensions (0–10 scale), computed as weighted composites of the signals above:

### Depth (Surface ← → Deep)

How deeply does this student engage with material?

| Signal | Weight | What It Measures |
|---|---|---|
| Inferential accuracy (Maze) | 15% | Can they read between the lines? |
| AWE evidence score | 20% | Quality of evidence use in writing |
| Reasoning sentence ratio | 25% | What fraction of their writing contains reasoning? |
| Cross-text references | 20% | Do they connect ideas across sources? |
| Reasoning growth over time | 20% | Is their analytical depth improving? |

### Structure (Systematic ← → Exploratory)

How does this student organize their thinking?

| Signal | Weight | What It Measures |
|---|---|---|
| Topic sentence consistency | 25% | Do they maintain organized paragraph structure? |
| Connective word diversity | 20% | Variety of logical connectors (because, however, therefore...) |
| Revision depth ratio | 25% | Do they make structural/argument edits, or just surface fixes? |
| Organization score | 15% | Topic sentence density as a structure proxy |
| Self-correction rate (ORF) | 15% | Metacognitive monitoring during reading |

### Evidence (Convergent ← → Divergent)

How does this student handle evidence?

| Signal | Weight | What It Measures |
|---|---|---|
| Number of evidence sources | 25% | Do they draw from many sources or few? |
| Counterargument presence | 25% | Do they consider opposing views? |
| Source count variance | 20% | Consistency in evidence breadth across essays |
| Answer changes (Maze) | 15% | Willingness to reconsider initial answers |
| Evidence explanation depth | 15% | Do they explain evidence deeply (convergent) or cite broadly (divergent)? |

## The 8 Thinking Types

Three binary dimensions (above/below 5.0) produce 8 types:

| Type | Depth | Structure | Evidence | Description |
|------|-------|-----------|----------|-------------|
| **Architect** | Deep | Systematic | Convergent | Builds carefully reasoned arguments with precision |
| **Detective** | Deep | Systematic | Divergent | Examines all angles before drawing a conclusion |
| **Advocate** | Deep | Exploratory | Convergent | Passionate about a position, argues with energy |
| **Explorer** | Deep | Exploratory | Divergent | Pursues ideas across boundaries, makes connections |
| **Reporter** | Surface | Systematic | Convergent | Accurately captures and organizes information |
| **Collector** | Surface | Systematic | Divergent | Gathers from many sources with strong research instincts |
| **Improviser** | Surface | Exploratory | Convergent | Quick, confident responses based on instinct |
| **Wanderer** | Surface | Exploratory | Divergent | Touches many ideas with genuine curiosity |

### Boundary Zone & Confidence

When a dimension score falls in the **boundary zone (4.0–6.0)**, the classification is less certain. The system:

- Assigns a **primary type** based on which side of 5.0 the score falls
- Identifies a **secondary type** (the type they'd be if that dimension flipped)
- Computes a **confidence score** based on distance from all boundaries — farther from boundaries = higher confidence

This means a teacher sees "Maria is an Explorer, but also shows Detective traits (42% confidence)" rather than a false certainty.

## Dashboard Features

### Overview
Class-wide distribution across all 8 types. Click any type card to see detailed strengths, growth areas, and teacher tips. Click a student name to see their full profile with dimension scores.

### Students
Searchable table with scores, confidence, and type history across curriculum units. Each row shows how a student's type has evolved over time.

### Grouping
AI-suggested peer review pairs based on complementary opposites:
- Architect ↔ Wanderer (structure meets creativity)
- Detective ↔ Improviser (thoroughness meets instinct)
- Advocate ↔ Collector (conviction meets breadth)
- Explorer ↔ Reporter (connections meet precision)

### Alerts
Flags three patterns teachers should know about:
- **Needs Attention**: Depth decreased between units (may need analytical support)
- **Stable Pattern**: Same type for 3+ units (consider a stretch activity)
- **Positive Growth**: Depth increasing or developing new thinking patterns

### Teacher Guide
Built-in reference explaining the framework, dimensions, all 8 types, and how to use the dashboard — so teachers can understand the system without external documentation.

## Key Design Principles

- **Not a score** — Thinking Types describes *style*, not *ability*. No type is better or worse.
- **Teacher decides direction** — The system shows where a student is. The teacher knows where they need to go.
- **Students never see labels** — The system uses types internally to personalize feedback, but students receive specific, actionable suggestions instead of type names.
- **No new assessments** — Everything is derived from data Amplify already collects.

## Tech Stack

- **Backend**: Python / FastAPI + SQLite
- **Frontend**: Vanilla HTML/CSS/JS
- **Static Demo**: Self-contained single HTML file with embedded data and base64 images
- **Deployment**: Render (full app) / GitHub Pages (interactive demo)

## Running Locally

```bash
cd app
pip install fastapi uvicorn jinja2
uvicorn main:app --reload
```

Open http://localhost:8000
