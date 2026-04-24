# Thinking Types — Amplify

A teacher-facing dashboard that analyzes student reading and writing data (mCLASS/DIBELS 8 + Amplify ELA) to identify **how each student thinks**, not just how well they perform.

## Live Demo

**[View the interactive demo](https://hz2784.github.io/thinkingtypes/)**

The demo includes all features with sample data for a Grade 6 class of 25 students.

## Features

- **Overview** — Class-wide thinking type distribution across 8 types, with clickable student chips and type cards
- **Students** — Searchable student table with scores, type history, and detailed profile modals
- **Grouping** — AI-suggested peer review pairs based on complementary thinking styles
- **Alerts** — Flags for depth decrease, stable patterns, and positive growth
- **Guide** — Teacher reference explaining the three dimensions (Depth, Structure, Evidence) and all 8 types

## The 8 Thinking Types

| Type | Profile | Description |
|------|---------|-------------|
| Architect | Deep + Systematic + Convergent | Builds carefully reasoned arguments with precision |
| Detective | Deep + Systematic + Divergent | Examines all angles before drawing a conclusion |
| Advocate | Deep + Exploratory + Convergent | Passionate about a position, argues with energy |
| Explorer | Deep + Exploratory + Divergent | Pursues ideas across boundaries, makes connections |
| Reporter | Surface + Systematic + Convergent | Accurately captures and organizes information |
| Collector | Surface + Systematic + Divergent | Gathers from many sources with strong research instincts |
| Improviser | Surface + Exploratory + Convergent | Quick, confident responses based on instinct |
| Wanderer | Surface + Exploratory + Divergent | Touches many ideas with genuine curiosity |

## Tech Stack

- **Backend**: Python / FastAPI + SQLite
- **Frontend**: Vanilla HTML/CSS/JS
- **Static Demo**: Self-contained single HTML file with embedded data and base64 images

## Running Locally

```bash
cd app
pip install fastapi uvicorn jinja2
uvicorn main:app --reload
```

Open http://localhost:8000

## Data Sources

No new assessments needed. Thinking Types extracts signals from data Amplify already collects:

- **Reading**: mCLASS / DIBELS 8 (ORF + Maze)
- **Writing**: Amplify ELA essays (AWE scores + text analysis)
