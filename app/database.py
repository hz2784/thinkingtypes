import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "thinking_types.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS classes (
            class_id TEXT PRIMARY KEY,
            teacher_id TEXT NOT NULL REFERENCES teachers(teacher_id),
            name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            school_year TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            class_id TEXT NOT NULL REFERENCES classes(class_id),
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            grade INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS units (
            unit_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            sequence INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orf_sessions (
            session_id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            unit_id TEXT REFERENCES units(unit_id),
            assessment_period TEXT NOT NULL,
            school_year TEXT NOT NULL,
            words_read_correct INTEGER NOT NULL,
            total_words_read INTEGER NOT NULL,
            errors INTEGER NOT NULL,
            accuracy REAL NOT NULL,
            self_corrections INTEGER DEFAULT 0,
            passage_id TEXT,
            measure_transcript TEXT,
            assessed_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS maze_sessions (
            session_id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            unit_id TEXT REFERENCES units(unit_id),
            assessment_period TEXT NOT NULL,
            school_year TEXT NOT NULL,
            correct INTEGER NOT NULL,
            incorrect INTEGER NOT NULL,
            adjusted_score REAL NOT NULL,
            items_attempted INTEGER NOT NULL,
            items_not_reached INTEGER DEFAULT 0,
            total_items INTEGER NOT NULL,
            inferential_correct INTEGER DEFAULT 0,
            inferential_total INTEGER DEFAULT 0,
            literal_correct INTEGER DEFAULT 0,
            literal_total INTEGER DEFAULT 0,
            answer_changes INTEGER DEFAULT 0,
            passage_id TEXT,
            assessed_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS essays (
            essay_id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            unit_id TEXT NOT NULL REFERENCES units(unit_id),
            school_year TEXT NOT NULL,
            title TEXT,
            content TEXT NOT NULL,
            word_count INTEGER NOT NULL,
            paragraph_count INTEGER NOT NULL,
            draft_number INTEGER DEFAULT 1,
            submitted_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS awe_scores (
            score_id TEXT PRIMARY KEY,
            essay_id TEXT NOT NULL REFERENCES essays(essay_id),
            focus_score REAL NOT NULL,
            evidence_score REAL NOT NULL,
            elaboration_score REAL NOT NULL,
            conventions_score REAL NOT NULL,
            language_score REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS essay_signals (
            signal_id TEXT PRIMARY KEY,
            essay_id TEXT NOT NULL REFERENCES essays(essay_id),
            reasoning_sentence_count INTEGER DEFAULT 0,
            total_sentence_count INTEGER DEFAULT 0,
            cross_text_references INTEGER DEFAULT 0,
            num_evidence_sources INTEGER DEFAULT 0,
            counterargument_present INTEGER DEFAULT 0,
            connective_words_unique INTEGER DEFAULT 0,
            connective_words_total INTEGER DEFAULT 0,
            topic_sentences_count INTEGER DEFAULT 0,
            revision_surface_edits INTEGER DEFAULT 0,
            revision_structural_edits INTEGER DEFAULT 0,
            revision_argument_edits INTEGER DEFAULT 0,
            evidence_explanation_sentences INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS thinking_profiles (
            profile_id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL REFERENCES students(student_id),
            unit_id TEXT REFERENCES units(unit_id),
            school_year TEXT NOT NULL,
            depth_score REAL NOT NULL,
            structure_score REAL NOT NULL,
            evidence_score REAL NOT NULL,
            thinking_type TEXT NOT NULL,
            secondary_type TEXT,
            confidence REAL NOT NULL,
            boundary_dimensions TEXT,
            signal_count INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE (student_id, unit_id, school_year)
        );
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
