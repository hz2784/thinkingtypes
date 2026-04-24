# Amplify mCLASS / DIBELS 8 — Data Model & Pipeline Reference

## Vision (from slide)
An end-to-end research-grade pipeline that transforms student work into actionable insights and recommendations teachers value to improve learning outcomes.

**Our focus: Step 2 (Capturing Data / Measurement) → Step 3 (Analyzing / Interpreting Data / Data Flow)**

---

## 1. Assessment Components (What Data Is Captured)

### DIBELS 8 Subtests by Grade Level

| Subtest | Abbreviation | K | 1 | 2 | 3 | 4 | 5 | 6-8 |
|---------|-------------|---|---|---|---|---|---|-----|
| Letter Naming Fluency | LNF | ✓ | ✓ | | | | | |
| Phoneme Segmentation Fluency | PSF | ✓ | ✓ | | | | | |
| Nonsense Word Fluency – Correct Letter Sounds | NWF-CLS | ✓ | ✓ | ✓ | ✓ | | | |
| Nonsense Word Fluency – Whole Words Read | NWF-WRC | ✓ | ✓ | ✓ | ✓ | | | |
| Word Reading Fluency | WRF | ✓ | ✓ | ✓ | ✓ | | | |
| Oral Reading Fluency – Words Read Correct | ORF-WRC | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Oral Reading Fluency – Accuracy | ORF-ACC | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Maze (Comprehension) | MAZE | | | ✓ | ✓ | ✓ | ✓ | ✓ |

### Optional/Experimental Subtests (K-3)
- Rapid Automatized Naming (RAN)
- Vocabulary
- Oral Language
- Encoding / Spelling (K-1, experimental)

### What Each Assessment Captures
- **Raw score**: count of correct responses in 1 minute (fluency measures)
- **Accuracy rate**: percentage of items read correctly (ORF-ACC)
- **Maze adjusted score**: comprehension measure
- **Measure transcript**: detailed record of every student response during assessment
- **Administration metadata**: date, assessor, benchmark period, grade, student ID

---

## 2. Assessment Schedule (Benchmark Periods)

| Period | Abbreviation | Typical Months |
|--------|-------------|----------------|
| Beginning of Year | BOY | September – November |
| Middle of Year | MOY | December – February |
| End of Year | EOY | March – June |

**Progress Monitoring**: Additional probes between benchmarks for at-risk students (frequency varies by tier).

---

## 3. Composite Score Calculation (How Data Is Transformed)

### Formula (6 steps)
1. Multiply each subtest raw score × Weight for that grade
2. Sum all weighted scores
3. Subtract the Mean for that grade
4. Divide by Standard Deviation for that grade (round to hundredths)
5. Multiply by 40 (round to ones)
6. Add the Scaling Constant for grade + season

**Scaling**: 400 = mean at MOY for each grade; SD = 40

### Weights by Grade

#### Kindergarten
| Subtest | BOY Weight | MOY/EOY Weight |
|---------|-----------|----------------|
| LNF | 35.44 | 8.86 |
| PSF | 4.13 | 4.13 |
| NWF-CLS | 14.93 | 14.93 |
| NWF-WRC | 3.56 | 3.56 |
| WRF | 5.62 | 5.62 |

- Mean: 729 (fall), 630 (winter)
- Constants: 289 (fall), 364 (winter), 398 (spring)

#### First Grade
| Subtest | Weight |
|---------|--------|
| LNF | 10.72 |
| PSF | included |
| NWF-CLS | included |
| NWF-WRC | included |
| WRF | included |
| ORF-WRC | included |
| ORF-ACC | included |

- Mean: 3371, SD: 2251
- Constants: 360 (fall), 400 (winter), 440 (spring)

#### Second Grade
| Subtest | Weight |
|---------|--------|
| NWF-CLS | 32.00 |
| NWF-WRC | 10.85 |
| WRF | 21.77 |
| ORF-WRC | 35.78 |
| ORF-ACC | 0.88 |
| MAZE | 4.33 |

- Mean: 7085, SD: 3811
- Constants: 360 (fall), 400 (winter), 440 (spring)

#### Third Grade
| Subtest | Weight |
|---------|--------|
| NWF-CLS | 40.06 |
| NWF-WRC | 11.78 |
| WRF | 19.35 |
| ORF-WRC | 39.48 |
| ORF-ACC | 0.90 |
| MAZE | 4.54 |

- Mean: 10051, SD: 4349
- Constants: 360 (fall), 400 (winter), 440 (spring)

---

## 4. Risk Classification (How Data Is Interpreted)

### Two Cut Points per Grade × Period
| Level | Label | Action |
|-------|-------|--------|
| Below risk cut | **Well Below Benchmark / At Risk** | Intensive intervention (Tier 3) |
| Between cuts | **Below Benchmark** | Strategic support (Tier 2) |
| Above benchmark cut | **At/Above Benchmark** | Core instruction (Tier 1) |

### Classification Accuracy (Sensitivity / Specificity)
| Grade | Period | Sensitivity | Specificity | n |
|-------|--------|-------------|-------------|---|
| K | Spring | .80 | .93 | 321 |
| 1 | Winter | .80 | .79 | 135 |
| 2 | Fall | .82 | .93 | 174 |
| 2 | Spring | .80 | .89 | 187 |
| 3 | Fall | .71 | .85 | 95 |
| 5 | Winter | .80 | .86 | 130 |

---

## 5. Data Flow: From Capture → Reports

```
Student Assessment (1 min each subtest)
        │
        ▼
┌─────────────────────┐
│  Raw Scores          │  ← LNF, PSF, NWF-CLS, NWF-WRC, WRF, ORF-WRC, ORF-ACC, MAZE
│  Measure Transcripts │  ← detailed student response record
│  Metadata            │  ← student, grade, school, date, assessor
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Composite Score     │  ← weighted formula → scaled score (mean=400, SD=40)
│  Risk Classification │  ← at-risk / below benchmark / on-track
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Instructional       │
│  Recommendations     │
│  - Skill grouping    │  ← groups by discrete skill needs, not just composite
│  - Tier placement    │  ← Tier 1 / 2 / 3
│  - mCLASS Instruction│  ← specific lesson recommendations
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Reports             │
│  - Student detail    │
│  - Class summary     │
│  - School/District   │  ← demographic breakdowns
│  - Caregiver (Home Connect) │
│  - Growth over time  │  ← BOY → MOY → EOY trajectory
└─────────────────────┘
```

---

## 6. Key Data Entities (for Synthetic Data Design)

### Student
- student_id, first_name, last_name, grade, school_id, district_id
- demographics: ethnicity, ELL status, IEP status, free/reduced lunch

### Assessment Session
- session_id, student_id, assessment_period (BOY/MOY/EOY), date, assessor_id
- grade_at_assessment

### Subtest Scores
- session_id, subtest_type (LNF/PSF/NWF-CLS/NWF-WRC/WRF/ORF-WRC/ORF-ACC/MAZE)
- raw_score, measure_transcript (JSON of individual responses)

### Composite Result
- session_id, composite_score, risk_level (at_risk/below_benchmark/on_track/above_benchmark)
- tier_recommendation (1/2/3)

### Instructional Recommendation
- session_id, skill_group, recommended_intervention, grouping_suggestion

---

## 7. Sources

- [DIBELS 8th Edition Materials — University of Oregon](https://dibels.uoregon.edu/materials/dibels)
- [DIBELS 8 Composite Score Calculation Guide](https://dibels.uoregon.edu/sites/default/files/2021-06/dibels_8_composite_score_calculation_guide_supplement_072020.pdf)
- [DIBELS 8 Benchmark Goals](https://dibels.uoregon.edu/sites/default/files/2024-01/dibels8_benchmark_goals.pdf)
- [Understanding DIBELS 8 Composite Scores](https://dibels.uoregon.edu/sites/default/files/2023-08/understandingdibels8compositescores_0.pdf)
- [mCLASS Program Details — Amplify](https://amplify.com/programs/mclass/mclass-program-details/)
- [mCLASS Overview — California Dept of Education](https://www.cde.ca.gov/ci/cl/mclassinfooverview.asp)
- [DIBELS 8 Academic Intervention Tools Chart](https://charts.intensiveintervention.org/screening/tool/?id=cf893d2246db95c3)
- [Oklahoma mCLASS Technical Guidance](https://oklahoma.gov/content/dam/ok/en/osde/strong-readers-files/25-26ScreeningTechnicalGuidanceDIBELS8.pdf)
