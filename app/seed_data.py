import sqlite3
import uuid
import random
import json
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "thinking_types.db")

random.seed(42)

def uid():
    return str(uuid.uuid4())[:8]

TEACHER_ID = "t-001"
CLASS_ID = "c-001"

UNITS = [
    ("6A", "Dahl & Narrative", 6, 1),
    ("6B", "Mysteries & Investigations", 6, 2),
    ("6C", "The Dark Is Rising", 6, 3),
    ("6D", "The Greeks", 6, 4),
]

ASSESSMENT_PERIODS = ["BOY", "MOY", "EOY"]

# Per-unit base scores: (first, last, [(depth, structure, evidence) per unit])
# This creates realistic type shifts across units for some students
STUDENT_PROFILES = [
    # Stable deep types
    ("James", "Park",     [(7.5, 2.0, 2.0), (7.8, 2.0, 2.5), (8.0, 1.5, 2.0), (7.5, 2.5, 2.0)]),
    ("Sofia", "Reyes",    [(8.0, 1.5, 2.5), (7.5, 2.0, 2.0), (8.0, 1.5, 2.5), (8.2, 1.5, 2.0)]),

    # Liam: Architect → Architect → Architect → Reporter (depth drops — warning alert)
    ("Liam", "Carter",    [(7.0, 3.0, 1.5), (7.2, 2.5, 2.0), (6.5, 3.0, 2.0), (3.5, 2.5, 2.0)]),

    # Marcus: Architect → Detective → Explorer → Detective (multi-type — positive)
    ("Marcus", "Johnson", [(7.8, 2.5, 3.0), (7.5, 2.0, 7.5), (7.5, 7.0, 7.5), (7.8, 2.0, 7.0)]),

    # Omar: Detective → Detective → Architect → Detective (shift and return)
    ("Omar", "Hassan",    [(7.5, 2.0, 7.5), (7.8, 2.5, 7.0), (7.5, 2.0, 3.0), (7.5, 2.5, 7.5)]),

    ("Elena", "Volkov",   [(8.0, 3.0, 8.0), (7.5, 2.5, 7.5), (8.0, 3.0, 8.0), (8.2, 2.5, 7.5)]),
    ("Kenji", "Tanaka",   [(7.0, 2.5, 7.0), (7.5, 2.0, 7.5), (7.0, 2.5, 7.0), (7.2, 2.5, 7.0)]),

    # Zara: Advocate → Advocate → Explorer → Explorer (structure shift — positive)
    ("Zara", "Ahmed",     [(7.5, 8.0, 2.0), (7.0, 7.5, 2.5), (7.5, 7.0, 7.5), (7.5, 7.5, 7.0)]),

    ("Diego", "Santos",   [(7.0, 7.5, 3.0), (7.5, 8.0, 2.5), (7.0, 7.5, 3.0), (7.2, 7.5, 2.5)]),

    # Maria: Explorer → Advocate → Explorer → Detective (multi-type — positive)
    ("Maria", "Chen",     [(7.5, 7.0, 7.5), (7.5, 7.5, 2.5), (7.5, 7.5, 7.0), (7.5, 2.5, 7.5)]),

    ("Aiden", "O'Brien",  [(8.0, 8.0, 8.0), (7.5, 7.5, 7.5), (8.0, 8.0, 8.0), (8.0, 7.5, 7.5)]),
    ("Priya", "Sharma",   [(7.0, 7.5, 7.0), (7.5, 7.0, 7.5), (7.0, 7.5, 7.0), (7.5, 7.0, 7.5)]),

    # Tyler: Reporter → Reporter → Improviser → Improviser (structure shift — positive)
    ("Tyler", "Brooks",   [(3.0, 2.0, 2.0), (3.5, 2.5, 2.5), (3.0, 7.0, 2.0), (3.0, 7.5, 2.5)]),

    # Grace: Reporter → Collector → Reporter → Collector (oscillating)
    ("Grace", "Kim",      [(3.5, 1.5, 2.5), (3.0, 2.0, 7.5), (3.5, 1.5, 2.5), (3.0, 2.5, 7.0)]),

    ("Kai", "Nakamura",   [(2.5, 2.5, 3.0), (3.0, 2.0, 2.5), (2.5, 2.5, 3.0), (2.5, 2.5, 2.5)]),

    # Amara: Reporter → Reporter → Architect (depth increases — positive)
    ("Amara", "Okafor",   [(3.0, 3.0, 2.0), (3.5, 2.5, 2.5), (5.5, 2.5, 2.0), (7.0, 2.5, 2.0)]),

    # Noah: Reporter → Collector → Wanderer → Reporter (multi-type)
    ("Noah", "Davis",     [(3.5, 2.0, 3.5), (3.0, 2.0, 7.5), (3.0, 7.5, 7.0), (3.5, 2.0, 2.5)]),

    # Lily: Collector → Collector → Wanderer → Wanderer (structure shift)
    ("Lily", "Wang",      [(3.0, 2.0, 7.5), (3.5, 2.5, 7.0), (3.0, 7.5, 7.5), (3.0, 7.0, 8.0)]),

    ("Ryan", "Miller",    [(2.5, 3.0, 8.0), (3.0, 2.5, 7.5), (2.5, 3.0, 8.0), (2.5, 2.5, 7.5)]),
    ("Nia", "Thompson",   [(3.5, 2.5, 7.0), (3.0, 2.0, 7.5), (3.5, 2.5, 7.0), (3.0, 2.0, 7.5)]),
    ("Sam", "Lee",        [(3.0, 1.5, 7.5), (3.5, 2.0, 7.0), (3.0, 1.5, 7.5), (3.0, 2.0, 7.5)]),

    # Jake: Improviser → Improviser → Advocate → Advocate (depth increase — positive)
    ("Jake", "Wilson",    [(3.0, 7.5, 2.0), (3.5, 7.0, 2.5), (7.0, 7.5, 2.0), (7.5, 7.5, 2.5)]),

    ("Mia", "Garcia",     [(3.5, 8.0, 3.0), (3.0, 7.5, 2.5), (3.5, 8.0, 3.0), (3.0, 7.5, 2.5)]),

    # Ethan: Wanderer → Explorer → Wanderer → Explorer (depth oscillation)
    ("Ethan", "Brown",    [(3.0, 7.0, 7.5), (7.0, 7.5, 7.0), (3.5, 7.0, 7.5), (7.0, 7.0, 7.5)]),

    ("Chloe", "Taylor",   [(2.5, 8.0, 8.0), (3.0, 7.5, 7.5), (2.5, 8.0, 8.0), (3.0, 7.5, 7.5)]),
]

CONNECTIVE_WORDS_SYSTEMATIC = ["First", "Second", "Third", "In conclusion", "Next", "Finally"]
CONNECTIVE_WORDS_DIVERSE = ["However", "Meanwhile", "On the other hand", "Interestingly",
                            "Furthermore", "In contrast", "Nevertheless", "Similarly",
                            "Consequently", "Although", "Despite this", "Moreover"]

REASONING_PHRASES = ["because", "therefore", "this shows that", "as a result",
                     "this means", "which suggests", "this proves", "consequently"]

COUNTER_PHRASES = ["some might argue", "on the other hand", "however, others believe",
                   "while some think", "although it could be said"]


def jitter(base, amount=1.5):
    return max(0.0, min(10.0, base + random.uniform(-amount, amount)))


def generate_orf_data(student_id, depth_base, structure_base, unit_idx, period):
    base_wrc = 130 + int(depth_base * 5) + unit_idx * 3
    wrc = base_wrc + random.randint(-10, 10)
    total = wrc + random.randint(2, 12)
    errors = total - wrc
    accuracy = round(wrc / total, 3) if total > 0 else 0
    self_corrections = random.randint(0, 3) if depth_base > 5 else random.randint(0, 1)

    pace_variability = 0.15 if structure_base > 5 else 0.05
    transcript = []
    for i in range(total):
        correct = random.random() > (errors / total)
        word_entry = {"position": i + 1, "word": f"word_{i+1}", "correct": correct}
        if not correct:
            word_entry["error_type"] = random.choice(["substitution", "hesitation", "omission"])
        transcript.append(word_entry)

    base_date = datetime(2025, 9, 1) + timedelta(days=unit_idx * 60)
    return {
        "session_id": uid(),
        "student_id": student_id,
        "unit_id": UNITS[unit_idx][0] if unit_idx < len(UNITS) else None,
        "assessment_period": period,
        "school_year": "2025-2026",
        "words_read_correct": wrc,
        "total_words_read": total,
        "errors": errors,
        "accuracy": accuracy,
        "self_corrections": self_corrections,
        "passage_id": f"G6-{period}-2025-A",
        "measure_transcript": json.dumps(transcript),
        "assessed_at": base_date.isoformat(),
    }


def generate_maze_data(student_id, depth_base, evidence_base, unit_idx, period):
    total_items = 34
    inferential_total = random.randint(10, 14)
    literal_total = total_items - inferential_total

    if depth_base > 5:
        literal_correct = int(literal_total * random.uniform(0.8, 0.95))
        inferential_correct = int(inferential_total * random.uniform(0.6, 0.85))
    else:
        literal_correct = int(literal_total * random.uniform(0.6, 0.85))
        inferential_correct = int(inferential_total * random.uniform(0.3, 0.55))

    correct = literal_correct + inferential_correct
    items_attempted = correct + random.randint(2, 6)
    incorrect = items_attempted - correct
    adjusted = round(correct - 0.5 * incorrect, 1)
    not_reached = total_items - items_attempted

    answer_changes = random.randint(2, 6) if evidence_base > 5 else random.randint(0, 2)

    base_date = datetime(2025, 9, 1) + timedelta(days=unit_idx * 60 + 5)
    return {
        "session_id": uid(),
        "student_id": student_id,
        "unit_id": UNITS[unit_idx][0] if unit_idx < len(UNITS) else None,
        "assessment_period": period,
        "school_year": "2025-2026",
        "correct": correct,
        "incorrect": incorrect,
        "adjusted_score": adjusted,
        "items_attempted": items_attempted,
        "items_not_reached": not_reached,
        "total_items": total_items,
        "inferential_correct": inferential_correct,
        "inferential_total": inferential_total,
        "literal_correct": literal_correct,
        "literal_total": literal_total,
        "answer_changes": answer_changes,
        "passage_id": f"G6-MAZE-{period}-2025-A",
        "assessed_at": base_date.isoformat(),
    }


def generate_essay_and_signals(student_id, unit_id, unit_idx, depth_base, structure_base, evidence_base):
    d = jitter(depth_base, 1.0)
    s = jitter(structure_base, 1.0)
    e = jitter(evidence_base, 1.0)

    is_deep = d > 5
    is_exploratory = s > 5
    is_divergent = e > 5

    paragraph_count = random.randint(3, 4) if not is_exploratory else random.randint(2, 6)
    sentences_per_para = random.randint(3, 5)
    total_sentences = paragraph_count * sentences_per_para
    word_count = total_sentences * random.randint(12, 18)

    reasoning_count = int(total_sentences * random.uniform(0.3, 0.5)) if is_deep else int(total_sentences * random.uniform(0.05, 0.15))
    cross_text_refs = random.randint(1, 3) if is_deep else random.randint(0, 1)

    if is_exploratory:
        connective_unique = random.randint(5, 10)
        connective_total = random.randint(8, 15)
    else:
        connective_unique = random.randint(2, 4)
        connective_total = random.randint(6, 12)

    topic_sentences = paragraph_count if not is_exploratory else random.randint(0, paragraph_count - 1)

    if is_exploratory:
        revision_surface = random.randint(1, 3)
        revision_structural = random.randint(2, 5)
        revision_argument = random.randint(1, 3) if is_deep else random.randint(0, 1)
    else:
        revision_surface = random.randint(3, 8)
        revision_structural = random.randint(0, 1)
        revision_argument = random.randint(0, 1)

    num_evidence = random.randint(3, 6) if is_divergent else random.randint(1, 2)
    counterargument = 1 if (is_divergent and random.random() > 0.3) else (1 if random.random() > 0.8 else 0)
    evidence_explanation = int(num_evidence * random.uniform(1.5, 3.0)) if not is_divergent else int(num_evidence * random.uniform(0.5, 1.2))

    # AWE scores
    focus = round(random.uniform(2.5, 4.0) if not is_exploratory else random.uniform(1.5, 3.0), 1)
    evidence_awe = round(random.uniform(2.5, 4.0) if is_deep else random.uniform(1.0, 2.5), 1)
    elaboration = round(random.uniform(2.0, 4.0) if is_deep else random.uniform(1.0, 2.5), 1)
    conventions = round(random.uniform(2.5, 4.0), 1)
    language = round(random.uniform(2.0, 4.0) if is_deep else random.uniform(1.5, 3.0), 1)

    base_date = datetime(2025, 9, 15) + timedelta(days=unit_idx * 60 + random.randint(0, 14))

    essay_id = uid()
    score_id = uid()
    signal_id = uid()

    essay = {
        "essay_id": essay_id,
        "student_id": student_id,
        "unit_id": unit_id,
        "school_year": "2025-2026",
        "title": f"Essay for {unit_id}",
        "content": f"[Simulated essay content for {unit_id}]",
        "word_count": word_count,
        "paragraph_count": paragraph_count,
        "draft_number": random.randint(1, 3),
        "submitted_at": base_date.isoformat(),
    }

    awe = {
        "score_id": score_id,
        "essay_id": essay_id,
        "focus_score": focus,
        "evidence_score": evidence_awe,
        "elaboration_score": elaboration,
        "conventions_score": conventions,
        "language_score": language,
    }

    signals = {
        "signal_id": signal_id,
        "essay_id": essay_id,
        "reasoning_sentence_count": reasoning_count,
        "total_sentence_count": total_sentences,
        "cross_text_references": cross_text_refs,
        "num_evidence_sources": num_evidence,
        "counterargument_present": counterargument,
        "connective_words_unique": connective_unique,
        "connective_words_total": connective_total,
        "topic_sentences_count": topic_sentences,
        "revision_surface_edits": revision_surface,
        "revision_structural_edits": revision_structural,
        "revision_argument_edits": revision_argument,
        "evidence_explanation_sentences": evidence_explanation,
    }

    return essay, awe, signals


def insert_dict(conn, table, data):
    cols = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})", list(data.values()))


KNOWLEDGE_NODES = [
    # Reading skills
    ("r-decode", "Decoding & Fluency", "reading", 5),
    ("r-vocab", "Vocabulary in Context", "reading", 5),
    ("r-literal", "Literal Comprehension", "reading", 5),
    ("r-inference", "Inferential Comprehension", "reading", 6),
    ("r-main-idea", "Main Idea & Theme", "reading", 6),
    ("r-text-structure", "Text Structure Analysis", "reading", 6),
    ("r-cross-text", "Cross-Text Comparison", "reading", 6),
    # Writing skills
    ("w-conventions", "Writing Conventions", "writing", 5),
    ("w-organization", "Essay Organization", "writing", 5),
    ("w-evidence", "Using Evidence", "writing", 6),
    ("w-elaboration", "Elaboration & Reasoning", "writing", 6),
    ("w-counterargument", "Counterargument", "writing", 6),
    ("w-revision", "Revision Strategy", "writing", 6),
    # Higher-order
    ("h-synthesis", "Synthesis Across Sources", "thinking", 6),
    ("h-argumentation", "Argumentation", "thinking", 6),
]

KNOWLEDGE_EDGES = [
    ("r-decode", "r-literal", "prerequisite"),
    ("r-decode", "r-vocab", "prerequisite"),
    ("r-literal", "r-inference", "prerequisite"),
    ("r-vocab", "r-inference", "prerequisite"),
    ("r-inference", "r-main-idea", "prerequisite"),
    ("r-inference", "r-cross-text", "prerequisite"),
    ("r-main-idea", "r-text-structure", "prerequisite"),
    ("w-conventions", "w-organization", "prerequisite"),
    ("w-organization", "w-evidence", "prerequisite"),
    ("w-evidence", "w-elaboration", "prerequisite"),
    ("w-evidence", "w-counterargument", "prerequisite"),
    ("w-elaboration", "w-revision", "related"),
    ("r-cross-text", "h-synthesis", "prerequisite"),
    ("w-evidence", "h-synthesis", "prerequisite"),
    ("w-elaboration", "h-argumentation", "prerequisite"),
    ("w-counterargument", "h-argumentation", "prerequisite"),
    ("h-synthesis", "h-argumentation", "related"),
]

NODE_SCORE_DRIVERS = {
    "r-decode": lambda d, s, e: min(1.0, d / 10 * 1.2),
    "r-vocab": lambda d, s, e: min(1.0, d / 10 * 1.1),
    "r-literal": lambda d, s, e: min(1.0, (d + 1) / 10),
    "r-inference": lambda d, s, e: min(1.0, d / 10 * 0.9),
    "r-main-idea": lambda d, s, e: min(1.0, (d * 0.6 + s * 0.4) / 10),
    "r-text-structure": lambda d, s, e: min(1.0, s / 10),
    "r-cross-text": lambda d, s, e: min(1.0, (d * 0.5 + e * 0.5) / 10),
    "w-conventions": lambda d, s, e: min(1.0, 0.5 + random.uniform(0, 0.3)),
    "w-organization": lambda d, s, e: min(1.0, s / 10 * 1.1),
    "w-evidence": lambda d, s, e: min(1.0, e / 10),
    "w-elaboration": lambda d, s, e: min(1.0, d / 10 * 0.85),
    "w-counterargument": lambda d, s, e: min(1.0, e / 10 * 0.8),
    "w-revision": lambda d, s, e: min(1.0, (s * 0.6 + d * 0.4) / 10),
    "h-synthesis": lambda d, s, e: min(1.0, (d * 0.4 + e * 0.3 + s * 0.3) / 10),
    "h-argumentation": lambda d, s, e: min(1.0, (d * 0.5 + e * 0.3 + s * 0.2) / 10),
}


def generate_student_knowledge(student_id, depth_base, structure_base, evidence_base):
    rows = []
    for node_id, _, _, _ in KNOWLEDGE_NODES:
        driver = NODE_SCORE_DRIVERS[node_id]
        mastery = driver(depth_base, structure_base, evidence_base)
        mastery = round(max(0.0, min(1.0, mastery + random.uniform(-0.08, 0.08))), 2)
        source = "orf" if node_id.startswith("r-") else ("essay" if node_id.startswith("w-") else "composite")
        rows.append({
            "student_id": student_id,
            "node_id": node_id,
            "mastery_level": mastery,
            "evidence_source": source,
            "updated_at": datetime(2026, 3, 15).isoformat(),
        })
    return rows


def seed():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    from database import init_db
    init_db()

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    insert_dict(conn, "teachers", {"teacher_id": TEACHER_ID, "name": "Mr. Thompson"})
    insert_dict(conn, "classes", {
        "class_id": CLASS_ID, "teacher_id": TEACHER_ID,
        "name": "Mr. Thompson's Class", "grade": 6, "school_year": "2025-2026"
    })

    for unit_id, name, grade, seq in UNITS:
        insert_dict(conn, "units", {"unit_id": unit_id, "name": name, "grade": grade, "sequence": seq})

    for node_id, label, domain, grade in KNOWLEDGE_NODES:
        insert_dict(conn, "knowledge_nodes", {
            "node_id": node_id, "label": label, "domain": domain, "grade_level": grade,
        })
    for parent_id, child_id, relation in KNOWLEDGE_EDGES:
        insert_dict(conn, "knowledge_edges", {
            "parent_id": parent_id, "child_id": child_id, "relation": relation,
        })

    for i, (first, last, unit_scores) in enumerate(STUDENT_PROFILES):
        student_id = f"s-{i+1:03d}"
        insert_dict(conn, "students", {
            "student_id": student_id, "class_id": CLASS_ID,
            "first_name": first, "last_name": last, "grade": 6
        })

        for unit_idx, (unit_id, _, _, _) in enumerate(UNITS):
            period = ASSESSMENT_PERIODS[min(unit_idx, 2)]
            depth_b, struct_b, evid_b = unit_scores[unit_idx]

            orf = generate_orf_data(student_id, depth_b, struct_b, unit_idx, period)
            insert_dict(conn, "orf_sessions", orf)

            maze = generate_maze_data(student_id, depth_b, evid_b, unit_idx, period)
            insert_dict(conn, "maze_sessions", maze)

            for essay_num in range(3):
                essay, awe, signals = generate_essay_and_signals(
                    student_id, unit_id, unit_idx, depth_b, struct_b, evid_b
                )
                essay["essay_id"] = f"{essay['essay_id']}-{essay_num}"
                awe["score_id"] = f"{awe['score_id']}-{essay_num}"
                awe["essay_id"] = essay["essay_id"]
                signals["signal_id"] = f"{signals['signal_id']}-{essay_num}"
                signals["essay_id"] = essay["essay_id"]

                insert_dict(conn, "essays", essay)
                insert_dict(conn, "awe_scores", awe)
                insert_dict(conn, "essay_signals", signals)

        last_depth, last_struct, last_evid = unit_scores[-1]
        for kn in generate_student_knowledge(student_id, last_depth, last_struct, last_evid):
            insert_dict(conn, "student_knowledge", kn)

    conn.commit()

    # Print summary
    cursor = conn.cursor()
    for table in ["students", "orf_sessions", "maze_sessions", "essays", "awe_scores", "essay_signals",
                   "knowledge_nodes", "knowledge_edges", "student_knowledge"]:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")

    conn.close()
    print(f"\nDatabase seeded at {DB_PATH}")


if __name__ == "__main__":
    seed()
