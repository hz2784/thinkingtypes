# Brain Gym: A Cognitive Capacity Framework for Grade 6

## Core Premise

Inspired by Joshua Landy's theory of formative fiction, this framework treats literacy activities not as tests to pass but as exercises that develop cognitive capacities. The system's goal is to answer one question: **How does this student think?**

Every observable behavior — reading speed, word choices in writing, error patterns, revision habits — is a window into the student's cognitive process. No single signal tells the full story. The system combines signals across products and over time to build a dynamic picture of each student's thinking.

---

## Part 1: Cognitive Capacities

### 1.1 Capacity Definitions

Eight capacities that Grade 6 literacy activities can develop and reveal:

| # | Capacity | Definition | Why It Matters at Grade 6 |
|---|----------|-----------|--------------------------|
| 1 | **Literal Comprehension** | Extracting explicitly stated information from text | Foundation — must be solid before higher-order thinking |
| 2 | **Inferential Reasoning** | Deriving meaning not explicitly stated; reading between the lines | Grade 6 texts increasingly require inference (e.g., character motivation, implied themes) |
| 3 | **Analogical Thinking** | Understanding one thing in terms of another; making connections across contexts | Key to deep learning — linking Greek democracy to modern government, for example |
| 4 | **Evidence Evaluation** | Selecting, judging, and deploying relevant evidence to support a claim | Central to argumentative writing, a Grade 6 ELA standard |
| 5 | **Perspective Taking** | Considering viewpoints other than one's own | Required for literary analysis and persuasive writing |
| 6 | **Metacognition** | Monitoring and regulating one's own comprehension and expression | The difference between a student who knows they're confused and one who doesn't |
| 7 | **Pattern Recognition** | Identifying structural, rhetorical, or thematic patterns in texts | Enables students to read like writers and write like readers |
| 8 | **Compositional Range** | The diversity and flexibility of a student's expressive repertoire | Distinguishes genuine thinking from template reliance — measured as a spectrum, not a binary |

### 1.2 What Compositional Range Captures

Compositional Range replaces the concept of "authenticity detection." It is deliberately neutral — it does not judge whether using a familiar structure or example is good or bad. Instead, it describes the variety and evolution of a student's writing behaviors.

**The spectrum:**

| Narrow Range | → | → | Wide Range |
|-------------|---|---|-----------|
| Same structure every essay | Varies structure occasionally | Adapts structure to purpose | Experiments with new forms |
| Reuses same examples regardless of topic | Selects from a small set of examples | Matches examples to topic | Generates novel examples from current reading |
| Fixed vocabulary | Slowly expanding vocabulary | Attempts new words (sometimes incorrectly) | Deploys varied vocabulary strategically |
| No revision | Surface edits (spelling, grammar) | Structural revision | Revises argument and reasoning |

**Critical design principle:** These patterns are visible only to teachers, never to students. The system provides information, not judgment. A teacher may look at narrow range and decide the student needs encouragement to take risks — or may decide the student needs more scaffolding before they can branch out. That pedagogical judgment belongs to the teacher.

---

## Part 2: Observable Signals → Capacity Mapping

### 2.1 Signals from mCLASS (DIBELS 8) — Low Frequency, Structured

Collected 3x/year (BOY, MOY, EOY) + progress monitoring.

#### ORF (Oral Reading Fluency)

| Signal | How to Extract | Maps to Capacity |
|--------|---------------|-----------------|
| Words read correct (WRC) | Direct score | Literal Comprehension (fluency as prerequisite) |
| Accuracy rate | Direct score | Literal Comprehension |
| Self-correction rate | Count self-corrections in transcript ÷ total errors | **Metacognition** — student is monitoring their own reading |
| Error type: multisyllabic words | Flag errors on words with 3+ syllables | Pattern Recognition (decoding strategy) |
| Error type: academic vocabulary | Flag errors on low-frequency / domain-specific words | Literal Comprehension (vocabulary gap) |
| Error distribution over time | Compare error rate in first 30s vs last 30s | Metacognition (attention/stamina) |
| Substitution patterns | Analyze what word was substituted for what | Inferential Reasoning (semantic substitutions suggest meaning-making; random substitutions suggest guessing) |

#### Maze (Reading Comprehension)

| Signal | How to Extract | Maps to Capacity |
|--------|---------------|-----------------|
| Adjusted score | Direct score | Literal Comprehension + Inferential Reasoning |
| Response time per item | Timestamp each selection (requires platform logging) | Distinguishes: fast+correct = automatized; slow+correct = effortful reasoning; fast+wrong = guessing |
| Error concentration | Where in the passage do errors cluster? | Literal Comprehension (beginning errors = engagement issue; end errors = fatigue or increasing text complexity) |
| Answer changes | Did student select, then change their answer? | **Metacognition** — self-monitoring during comprehension |
| Items attempted vs not reached | Count of each | Processing speed; also interacts with accuracy to distinguish careful-slow from struggling-slow |

### 2.2 Signals from Amplify ELA (AWE) — High Frequency, Unstructured

Collected 2-3x/week. This is the richest data source for cognitive capacity detection.

#### Existing AWE Dimensions (already scored)

| Signal | Maps to Capacity |
|--------|-----------------|
| Focus score | Pattern Recognition (can the student identify and maintain a central idea?) |
| Evidence score | Evidence Evaluation |
| Conventions score | Baseline linguistic competence |

#### New Signals to Extract from Writing (Phase 2+)

**Argument Structure Analysis:**

| Signal | How to Detect | Maps to Capacity |
|--------|--------------|-----------------|
| Claim present? | NLP: does the essay contain a clear thesis/position? | Evidence Evaluation |
| Evidence linked to claim? | NLP: does evidence support the claim, or is it disconnected? | Evidence Evaluation |
| Reasoning present? | NLP: does the student explain WHY the evidence supports the claim? (the "because/therefore" gap) | **Inferential Reasoning** |
| Counterargument acknowledged? | NLP: does the student address opposing viewpoints? | **Perspective Taking** |
| Conclusion synthesizes (vs restates)? | NLP: does the conclusion add insight or just repeat the introduction? | Analogical Thinking |

**Vocabulary and Syntax Analysis:**

| Signal | How to Detect | Maps to Capacity |
|--------|--------------|-----------------|
| Academic vocabulary ratio | Count Tier 2/3 words ÷ total words | Compositional Range |
| Vocabulary relative to student's own history | Compare current essay's word choices to prior essays | Compositional Range (growth signal) |
| Sentence complexity | Average clause count per sentence; subordinate clause usage | Pattern Recognition (linguistic sophistication) |
| Productive errors | Student attempts a complex word/structure but uses it incorrectly | **Positive signal** — student is stretching |

**Cross-Essay Pattern Analysis (Compositional Range):**

| Signal | How to Detect | Maps to Capacity |
|--------|--------------|-----------------|
| Structural similarity across essays | Compare paragraph count, paragraph lengths, overall essay shape | Compositional Range: high similarity = narrow range |
| Example/evidence reuse rate | Semantic similarity of cited examples across essays | Compositional Range: same example in unrelated topics = forced fit |
| Example relevance to current unit | Does the evidence come from the current reading material? | Analogical Thinking (applying new knowledge) |
| Opening/closing formula rigidity | Cosine similarity of first/last paragraphs across essays | Compositional Range |
| Connective diversity | Set of transition words used; does it change across essays? | Compositional Range |

**Writing Process Signals (from platform interaction logs):**

| Signal | How to Detect | Maps to Capacity |
|--------|--------------|-----------------|
| Writing duration | Total time from start to submit | Context-dependent (fast ≠ bad, slow ≠ good) |
| Pause patterns | Where does the student pause for >10 seconds? | Before a new paragraph = planning; mid-sentence = stuck |
| Revision type | What was deleted and rewritten? Spelling vs. whole sentences vs. argument restructuring | **Metacognition**: surface revision vs. deep revision |
| Revision timing | Edits during writing vs. edits at the end | During = real-time monitoring; end-only = proofreading |
| Paste events | Large text blocks pasted from external source | Compositional Range (flag for teacher review, not automatic judgment) |

### 2.3 Cross-Product Signals

| Signal | How to Detect | Maps to Capacity |
|--------|--------------|-----------------|
| Reading-writing alignment | ORF/Maze on track but writing weak, or vice versa | Identifies specific capacity gaps (can comprehend but can't produce, or vice versa) |
| Knowledge transfer | Student reads about Greek mythology in CKLA unit → uses Greek examples in writing | **Analogical Thinking** |
| Growth correlation | Does improvement in Maze track with improvement in AWE Evidence score? | Validates whether reading intervention is also improving writing |
| Consistency of metacognition | High self-correction in ORF AND deep revision in writing = consistent metacognitive strength | **Metacognition** (cross-validated) |

---

## Part 3: The Thinking Profile

All signals roll up into a per-student Thinking Profile. This is NOT a report card. It is a diagnostic tool for teachers.

### 3.1 Profile Structure

```
Student: Maria Chen, Grade 6
Assessment Period: MOY 2025-2026
Data Sources: mCLASS (BOY, MOY) + Amplify ELA (14 essays to date)

READING INDICATORS
├── ORF: 155 wpm, 97% accuracy (At Benchmark)
├── Maze: adjusted 22 (At Benchmark)
└── mCLASS Tier: 1 (Core instruction)

COGNITIVE CAPACITY PROFILE
├── Literal Comprehension      ████████░░  Strong
├── Inferential Reasoning      █████░░░░░  Developing
├── Analogical Thinking        ███░░░░░░░  Emerging
├── Evidence Evaluation        █████░░░░░  Developing
├── Perspective Taking         ██░░░░░░░░  Emerging
├── Metacognition              ████████░░  Strong
├── Pattern Recognition        ██████░░░░  Developing
└── Compositional Range        ████░░░░░░  Developing

KEY OBSERVATIONS (teacher-facing only)
├── Strength: High self-correction rate in ORF + deep revision 
│   in writing → strong self-monitoring
├── Gap: Can identify evidence (Maze high) but struggles to 
│   explain WHY evidence matters (reasoning absent in 9/14 essays)
├── Pattern: Has used the same Martin Luther King example in 
│   4 essays across different topics — may need support 
│   diversifying evidence sources
├── Growth: Evidence Evaluation improved from BOY to MOY 
│   (3 → 5 on internal scale) after targeted instruction
└── Note: Essay #12 showed vocabulary complexity 2 SD above 
    Maria's historical mean — review recommended

SUGGESTED NEXT EXERCISES
├── Priority: Practice "because... therefore..." reasoning chains
├── Activity: Compare two texts on the same topic, write about
│   which presents stronger evidence and WHY
└── Grouping: Pair with students who also show 
    comprehension-to-production gap
```

### 3.2 What Teachers See vs What Students See

| Layer | Teachers See | Students See |
|-------|-------------|-------------|
| mCLASS scores | Full scores + tier + growth | Their own scores (if district allows) |
| AWE feedback | Scores + capacity signals + patterns | Focus/Evidence/Conventions feedback only |
| Thinking Profile | Full profile with all 8 capacities | Nothing — this is a teacher diagnostic tool |
| Compositional Range | Pattern analysis + specific examples | Nothing |
| Writing process data | Revision patterns, timing, paste events | Nothing |
| Recommendations | Specific capacity-targeted activities | General next steps |

---

## Part 4: Database Additions for Brain Gym

### 4.1 New Tables (additions to existing schema)

#### cognitive_capacities (reference table)
```sql
CREATE TABLE cognitive_capacities (
    capacity_id     SMALLINT PRIMARY KEY,
    name            VARCHAR(50) NOT NULL,
    description     TEXT NOT NULL
);

INSERT INTO cognitive_capacities VALUES
(1, 'literal_comprehension', 'Extracting explicitly stated information from text'),
(2, 'inferential_reasoning', 'Deriving meaning not explicitly stated'),
(3, 'analogical_thinking', 'Understanding one thing in terms of another'),
(4, 'evidence_evaluation', 'Selecting and deploying relevant evidence'),
(5, 'perspective_taking', 'Considering viewpoints other than one''s own'),
(6, 'metacognition', 'Monitoring and regulating one''s own comprehension'),
(7, 'pattern_recognition', 'Identifying structural and rhetorical patterns'),
(8, 'compositional_range', 'Diversity and flexibility of expressive repertoire');
```

#### capacity_observations (individual signal detections)
```sql
CREATE TABLE capacity_observations (
    observation_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id          UUID NOT NULL REFERENCES students(student_id),
    capacity_id         SMALLINT NOT NULL REFERENCES cognitive_capacities(capacity_id),
    source_type         VARCHAR(20) NOT NULL,  -- 'mclass_orf', 'mclass_maze', 'ela_writing'
    source_id           UUID NOT NULL,          -- session_id or writing_id
    signal_name         VARCHAR(100) NOT NULL,  -- e.g., 'self_correction_rate', 'example_reuse'
    signal_value        DECIMAL(8,4),           -- numeric value
    signal_detail       JSONB,                  -- additional context
    observed_at         DATE NOT NULL
);
```

#### capacity_scores (aggregated per student per period)
```sql
CREATE TABLE capacity_scores (
    score_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id          UUID NOT NULL REFERENCES students(student_id),
    capacity_id         SMALLINT NOT NULL REFERENCES cognitive_capacities(capacity_id),
    assessment_period   VARCHAR(3) NOT NULL,  -- 'BOY', 'MOY', 'EOY'
    school_year         VARCHAR(9) NOT NULL,
    score               DECIMAL(4,2) NOT NULL, -- 0-10 scale
    confidence          DECIMAL(3,2),           -- how many signals contributed
    level               VARCHAR(20) NOT NULL,   -- 'emerging', 'developing', 'strong', 'exemplary'
    previous_score      DECIMAL(4,2),
    growth              DECIMAL(4,2),
    evidence_summary    JSONB,                  -- key signals that drove this score
    UNIQUE (student_id, capacity_id, assessment_period, school_year)
);
```

#### writing_submissions (Amplify ELA writing data)
```sql
CREATE TABLE writing_submissions (
    writing_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id          UUID NOT NULL REFERENCES students(student_id),
    unit_id             VARCHAR(20) NOT NULL,   -- e.g., '6A', '6B'
    assignment_id       VARCHAR(50) NOT NULL,
    submitted_at        TIMESTAMPTZ NOT NULL,
    content             TEXT NOT NULL,
    word_count          INT NOT NULL,
    awe_focus           DECIMAL(3,1),
    awe_evidence        DECIMAL(3,1),
    awe_conventions     DECIMAL(3,1),
    writing_duration_seconds INT,
    revision_count      INT,
    paste_event_count   INT DEFAULT 0
);
```

#### writing_process_events (keystroke/interaction level)
```sql
CREATE TABLE writing_process_events (
    event_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    writing_id          UUID NOT NULL REFERENCES writing_submissions(writing_id),
    event_type          VARCHAR(30) NOT NULL,  -- 'pause', 'delete', 'paste', 'revision', 'submit'
    event_timestamp     TIMESTAMPTZ NOT NULL,
    detail              JSONB                  -- e.g., {"deleted_text": "...", "replacement": "..."}
);
```

#### writing_analysis (AI-generated analysis per essay)
```sql
CREATE TABLE writing_analysis (
    analysis_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    writing_id          UUID NOT NULL REFERENCES writing_submissions(writing_id),
    has_claim            BOOLEAN,
    has_evidence         BOOLEAN,
    has_reasoning        BOOLEAN,
    has_counterargument  BOOLEAN,
    conclusion_type     VARCHAR(20),            -- 'restates', 'synthesizes', 'extends'
    academic_vocab_ratio DECIMAL(4,3),
    avg_sentence_length  DECIMAL(5,1),
    subordinate_clause_rate DECIMAL(4,3),
    structural_similarity_to_prior DECIMAL(4,3), -- cosine sim with student's previous essays
    example_reuse_flag   BOOLEAN,
    vocabulary_anomaly   BOOLEAN,               -- significantly above/below student's historical mean
    analysis_detail     JSONB                   -- full AI analysis output
);
```

### 4.2 Key Indexes

```sql
CREATE INDEX idx_capacity_obs_student ON capacity_observations(student_id, capacity_id, observed_at);
CREATE INDEX idx_capacity_scores_student ON capacity_scores(student_id, school_year);
CREATE INDEX idx_writing_student ON writing_submissions(student_id, unit_id);
CREATE INDEX idx_writing_analysis ON writing_analysis(writing_id);
CREATE INDEX idx_process_events ON writing_process_events(writing_id, event_type);
```

### 4.3 Updated Data Flow

```
LAYER 1: DATA CAPTURE (existing + enhanced)
─────────────────────────────────────────────
mCLASS app                    Amplify ELA platform
├── ORF transcript             ├── Student essay text
├── Maze responses             ├── AWE scores (Focus/Evidence/Conventions)
└── (existing)                 ├── Writing process events (NEW)
                               │   ├── pause timestamps
                               │   ├── revision history
                               │   └── paste events
                               └── Submission metadata


LAYER 2: SIGNAL EXTRACTION
─────────────────────────────────────────────
mCLASS signals                 ELA writing signals
├── Self-correction rate       ├── Argument structure (claim/evidence/reasoning)
├── Error type distribution    ├── Vocabulary complexity vs history
├── Maze response timing       ├── Structural similarity to prior essays
└── (rule-based)               ├── Example reuse detection
                               ├── Revision depth analysis
                               └── (AI-powered, LLM-based)

         → INSERT capacity_observations


LAYER 3: CAPACITY SCORING
─────────────────────────────────────────────
Aggregate observations per student per capacity
├── Weight signals by recency and reliability
├── Compare to prior period → compute growth
├── Assign level (emerging / developing / strong / exemplary)
└── Generate evidence summary

         → INSERT capacity_scores


LAYER 4: THINKING PROFILE
─────────────────────────────────────────────
Combine all 8 capacity scores into student profile
├── Identify strengths and gaps
├── Detect cross-product patterns (reading × writing)
├── Generate capacity-targeted recommendations
└── Surface to teacher dashboard (NEVER to students)
```

---

## Part 5: Phase 1 Implementation (Zero New AI)

Phase 1 uses only existing data and rule-based logic to validate the framework before investing in AI-powered analysis.

### Available signals in Phase 1:

| Source | Signal | Capacity | Logic |
|--------|--------|----------|-------|
| ORF transcript | Self-correction count ÷ total errors | Metacognition | Rule: > 0.3 = strong metacognitive monitoring |
| ORF transcript | Errors on 3+ syllable words ÷ total errors | Pattern Recognition | Rule: > 0.5 = decoding strategy gap |
| Maze | Adjusted score | Literal Comprehension + Inferential Reasoning | Existing benchmark mapping |
| AWE Focus | Score trend over essays | Pattern Recognition | Rule: improving trend = capacity developing |
| AWE Evidence | Score trend over essays | Evidence Evaluation | Same |
| AWE Conventions | Score trend over essays | Baseline | Same |
| Cross-product | Maze high + AWE Evidence low | Comprehension-to-production gap | Rule: difference > 1 SD = flag |

### What Phase 1 does NOT include:
- No NLP analysis of essay content
- No writing process tracking
- No cross-essay similarity detection
- No AI-generated capacity observations

Phase 1 is a reporting-layer overlay on existing data — it reframes scores as capacity indicators.

---

## Sources

- Landy, J. (2012). "Formative Fictions: Imaginative Literature and the Training of the Capacities." *Poetics Today*, 33(2), 169-216.
- Landy, J. (2012). *How to Do Things with Fictions*. Oxford University Press.
- [Amplify AI](https://amplify.com/artificial-intelligence/)
- [Amplify ELA: Automated Writing Evaluation](https://service.amplify.com/article/5899278-amplify-ela-automated-writing-evaluation-overview)
- [DIBELS 8 Materials — University of Oregon](https://dibels.uoregon.edu/materials/dibels)
- [mCLASS — Amplify](https://amplify.com/programs/mclass/)
