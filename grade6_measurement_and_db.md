# mCLASS Grade 6: Measurement & Database Design

## Overview

This document covers the internal data architecture for Amplify's mCLASS platform, focused on Grade 6 literacy assessment using DIBELS 8th Edition. mCLASS is the sole licensed digital provider of DIBELS 8.

Grade 6 administers two subtests:
- **ORF (Oral Reading Fluency)** — 1-on-1, teacher-administered, 1 minute
- **Maze** — group-administered, student self-paced, 3 minutes

---

## Part 1: How Measurement Works

### 1.1 ORF (Oral Reading Fluency)

**What it measures:** Reading speed, accuracy, and automaticity with connected text at grade level.

**Administration flow:**
1. Teacher opens mCLASS app on iPad, selects student and assessment type
2. App displays a grade-level passage written by published authors
3. Student reads aloud for 1 minute
4. Teacher taps each word in real time: correct or incorrect
5. System auto-marks 3-second hesitations
6. Timer ends at 60 seconds; app calculates scores instantly
7. Data syncs to cloud

**Scoring rules:**
- Errors: substitutions, omissions, hesitations > 3 seconds
- Not errors: self-corrections within 3 seconds
- One passage per benchmark period (DIBELS 8 change from prior editions)

**Data produced per session:**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| words_read_correct | int | Words read correctly in 1 min (WRC) | 142 |
| total_words_read | int | Total words attempted | 148 |
| errors | int | Total errors | 6 |
| accuracy | decimal | WRC / total_words_read | 0.959 |
| passage_id | string | Which passage was used | "G6-BOY-2025-A" |
| measure_transcript | JSON | Per-word correctness record | see below |

**Measure transcript structure:**
```json
[
  {"position": 1, "word": "The", "correct": true},
  {"position": 2, "word": "archaeological", "correct": false, "error_type": "substitution", "substitution": "archeo-logical"},
  {"position": 3, "word": "expedition", "correct": true},
  {"position": 4, "word": "discovered", "correct": false, "error_type": "hesitation"},
  ...
  {"position": 148, "word": "remains", "correct": true, "is_last_word": true}
]
```

**Grade 6 benchmark goals (ORF-WRC):**

| Period | At Risk | Below Benchmark | At/Above Benchmark |
|--------|---------|-----------------|-------------------|
| BOY | < 123 | 123–150 | 151+ |
| MOY | < 133 | 133–156 | 157+ |
| EOY | < 141 | 141–159 | 160+ |

**Accuracy benchmark:** 96%+ across all periods.

---

### 1.2 Maze (Reading Comprehension)

**What it measures:** Reading comprehension — ability to construct meaning from text using vocabulary, syntax, and reasoning.

**Administration flow:**
1. Teacher assigns a Maze assessment to the class via mCLASS platform
2. Students open the assessment on their own devices
3. A passage appears with the first sentence intact; after that, every 7th word is replaced with 3 options
4. Students select the correct word for each blank
5. 3-minute countdown; auto-submits when time runs out
6. System scores automatically

**Example passage:**
> The explorer traveled deep into the jungle. He carried a heavy **(pack / tree / song)** on his back. The **(weather / pencil / chair)** was hot and humid, making every step more difficult.

**Scoring rules:**
- Adjusted Score = correct − (0.5 × incorrect)
- Skipped items count as incorrect
- Items not reached (ran out of time) do NOT count as incorrect

**Data produced per session:**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| correct | int | Number of correct selections | 22 |
| incorrect | int | Wrong selections + skipped items | 4 |
| adjusted_score | decimal | correct − 0.5 × incorrect | 20.0 |
| items_attempted | int | Total items the student reached | 26 |
| items_not_reached | int | Items not reached before time expired | 8 |
| total_items | int | Total blanks in the passage | 34 |
| passage_id | string | Which passage was used | "G6-MAZE-BOY-2025-A" |
| responses | JSON | Per-item response record | see below |

**Response record structure:**
```json
[
  {"position": 1, "options": ["pack", "tree", "song"], "correct_answer": "pack", "selected": "pack", "correct": true},
  {"position": 2, "options": ["weather", "pencil", "chair"], "correct_answer": "weather", "selected": "pencil", "correct": false},
  {"position": 3, "options": ["began", "purple", "eleven"], "correct_answer": "began", "selected": null, "status": "not_reached"}
]
```

---

### 1.3 Composite Score Calculation

The composite score combines ORF and Maze data into a single standardized metric.

**Formula (6 steps):**
1. Multiply each raw score by its grade-specific weight
2. Sum all weighted scores
3. Subtract the grade-specific mean
4. Divide by the grade-specific standard deviation
5. Multiply by 40 (scaling factor)
6. Add the season-specific constant for the grade

**Result:** A score centered at 400 (MOY mean) with SD = 40, comparable across grades and time periods.

**Risk classification from composite:**

| Composite Score | Risk Level | Tier | Action |
|----------------|------------|------|--------|
| Below risk cut | Well Below Benchmark | 3 | Intensive intervention |
| Between cuts | Below Benchmark | 2 | Strategic small-group support |
| At/above benchmark cut | At/Above Benchmark | 1 | Core instruction, no intervention |

---

## Part 2: Database Design

### 2.1 Entity Relationship Diagram

```
District 1──* School 1──* Teacher
                School 1──* Classroom
                             Classroom *──* Student  (via student_classrooms)
                                            Student 1──* AssessmentSession
                                                          AssessmentSession 1──1 OrfScore
                                                          AssessmentSession 1──1 MazeScore
                                                          AssessmentSession 1──1 CompositeResult
                                                          CompositeResult   1──* Recommendation
```

### 2.2 Table Definitions

#### districts
```sql
CREATE TABLE districts (
    district_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(200) NOT NULL,
    state           CHAR(2) NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT now()
);
```

#### schools
```sql
CREATE TABLE schools (
    school_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    district_id     UUID NOT NULL REFERENCES districts(district_id),
    name            VARCHAR(200) NOT NULL,
    school_type     VARCHAR(20) CHECK (school_type IN ('elementary', 'middle', 'k8', 'high'))
);
```

#### teachers
```sql
CREATE TABLE teachers (
    teacher_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id       UUID NOT NULL REFERENCES schools(school_id),
    name            VARCHAR(100) NOT NULL,
    email           VARCHAR(200) UNIQUE
);
```

#### students
```sql
CREATE TABLE students (
    student_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    district_id     UUID NOT NULL REFERENCES districts(district_id),
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    date_of_birth   DATE,
    current_grade   SMALLINT NOT NULL CHECK (current_grade BETWEEN 0 AND 12),
    ethnicity       VARCHAR(50),
    is_ell          BOOLEAN DEFAULT FALSE,
    has_iep         BOOLEAN DEFAULT FALSE,
    is_frl          BOOLEAN DEFAULT FALSE
);
```

#### student_classrooms
```sql
CREATE TABLE student_classrooms (
    student_id      UUID NOT NULL REFERENCES students(student_id),
    classroom_id    UUID NOT NULL,
    teacher_id      UUID NOT NULL REFERENCES teachers(teacher_id),
    school_id       UUID NOT NULL REFERENCES schools(school_id),
    school_year     VARCHAR(9) NOT NULL,
    PRIMARY KEY (student_id, classroom_id, school_year)
);
```

#### assessment_sessions
```sql
CREATE TABLE assessment_sessions (
    session_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id          UUID NOT NULL REFERENCES students(student_id),
    assessor_id         UUID NOT NULL REFERENCES teachers(teacher_id),
    assessment_period   VARCHAR(3) NOT NULL CHECK (assessment_period IN ('BOY', 'MOY', 'EOY', 'PM')),
    school_year         VARCHAR(9) NOT NULL,
    assessment_date     DATE NOT NULL,
    grade_at_assessment SMALLINT NOT NULL,
    created_at          TIMESTAMPTZ DEFAULT now()
);
```

#### orf_scores
```sql
CREATE TABLE orf_scores (
    session_id          UUID PRIMARY KEY REFERENCES assessment_sessions(session_id),
    words_read_correct  SMALLINT NOT NULL,
    total_words_read    SMALLINT NOT NULL,
    errors              SMALLINT NOT NULL,
    accuracy            DECIMAL(4,3) NOT NULL,
    passage_id          VARCHAR(50) NOT NULL,
    measure_transcript  JSONB NOT NULL
);
```

#### maze_scores
```sql
CREATE TABLE maze_scores (
    session_id          UUID PRIMARY KEY REFERENCES assessment_sessions(session_id),
    correct             SMALLINT NOT NULL,
    incorrect           SMALLINT NOT NULL,
    adjusted_score      DECIMAL(5,1) NOT NULL,
    items_attempted     SMALLINT NOT NULL,
    items_not_reached   SMALLINT NOT NULL,
    total_items         SMALLINT NOT NULL,
    passage_id          VARCHAR(50) NOT NULL,
    responses           JSONB NOT NULL
);
```

#### composite_results
```sql
CREATE TABLE composite_results (
    session_id          UUID PRIMARY KEY REFERENCES assessment_sessions(session_id),
    composite_score     SMALLINT NOT NULL,
    risk_level          VARCHAR(25) NOT NULL CHECK (risk_level IN ('well_below', 'below', 'at_benchmark', 'above_benchmark')),
    tier                SMALLINT NOT NULL CHECK (tier IN (1, 2, 3)),
    percentile          SMALLINT,
    previous_session_id UUID REFERENCES assessment_sessions(session_id),
    growth              SMALLINT
);
```

#### recommendations
```sql
CREATE TABLE recommendations (
    recommendation_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id          UUID NOT NULL REFERENCES assessment_sessions(session_id),
    skill_area          VARCHAR(50) NOT NULL,
    priority            SMALLINT NOT NULL,
    description         TEXT NOT NULL,
    grouping_suggestion VARCHAR(200)
);
```

### 2.3 Indexes

```sql
CREATE INDEX idx_sessions_student_year ON assessment_sessions(student_id, school_year);
CREATE INDEX idx_sessions_period ON assessment_sessions(assessment_period, school_year, grade_at_assessment);
CREATE INDEX idx_composite_risk ON composite_results(risk_level, tier);
CREATE INDEX idx_students_grade_district ON students(current_grade, district_id);
CREATE INDEX idx_student_classrooms_year ON student_classrooms(school_year, school_id);
```

### 2.4 Key Design Decisions

**Why JSONB for transcripts/responses:**
ORF transcripts vary in length (depends on how many words the student reaches). Maze responses vary by passage. JSONB allows flexible storage while still supporting indexed queries (e.g., finding all students who got a specific word wrong).

**Why `previous_session_id` in composite_results:**
Enables direct growth calculation without complex joins. When a new session is scored, the system links it to the most recent prior session for the same student.

**Why `grade_at_assessment` in assessment_sessions:**
A student's grade may change (retention, mid-year transfer). The grade at the time of assessment determines which benchmark goals and composite weights apply.

**Why `assessment_period` includes 'PM':**
Progress monitoring (PM) probes happen between benchmarks for Tier 2/3 students. These use the same subtests but at higher frequency (weekly/biweekly).

---

## Part 3: Data Flow (Step 2 → Step 3)

```
STEP 2: CAPTURE
─────────────────────────────────────────────────────
Teacher opens mCLASS app
    │
    ├─ ORF (1-on-1, 1 min)
    │   ├─ Real-time word-by-word marking
    │   ├─ → INSERT orf_scores (WRC, ACC, transcript)
    │   └─ → INSERT assessment_sessions
    │
    └─ Maze (group, 3 min)
        ├─ Students select answers on devices
        ├─ Auto-scored on submission
        ├─ → INSERT maze_scores (correct, incorrect, adjusted, responses)
        └─ → INSERT assessment_sessions

STEP 3: ANALYZE
─────────────────────────────────────────────────────
On assessment completion:
    │
    ├─ 1. Compute composite score (weighted formula)
    ├─ 2. Look up benchmark cut points for grade + period
    ├─ 3. Classify risk level → assign tier
    ├─ 4. Find previous session → compute growth
    ├─ 5. Analyze error patterns from transcripts
    ├─ 6. Generate skill-based recommendations
    │
    ├─ → INSERT composite_results
    └─ → INSERT recommendations

REPORTS (output)
─────────────────────────────────────────────────────
    ├─ Student Report: individual trajectory + next steps
    ├─ Class Report: tier distribution + skill-based grouping
    ├─ School/District Report: demographic breakdowns + trends
    └─ Home Connect: simplified chart for caregivers
```

---

## Sources

- [DIBELS 8 Materials — University of Oregon](https://dibels.uoregon.edu/materials/dibels)
- [DIBELS 8 Composite Score Calculation Guide](https://dibels.uoregon.edu/sites/default/files/2021-06/dibels_8_composite_score_calculation_guide_supplement_072020.pdf)
- [DIBELS 8 Grade 6 Benchmark Goals](https://dibels.amplify.com/docs/DIBELS8thEditionGoals_6.pdf)
- [mCLASS Program Details — Amplify](https://amplify.com/programs/mclass/mclass-program-details/)
- [DIBELS 8 Maze — Academic Intervention Tools Chart](https://charts.intensiveintervention.org/screening/tool/?id=64d78d44f474b338)
- [About DIBELS — University of Oregon](https://dibels.uoregon.edu/about-dibels)
