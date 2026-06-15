"""SQLite persistence layer for the exam-prep dashboard."""
import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

_default_db_path = Path(__file__).resolve().parent.parent / "data" / "app.db"
DB_PATH = Path(os.environ["DB_PATH"]) if os.environ.get("DB_PATH") else _default_db_path

SCHEMA = """
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    summary TEXT,
    source_file TEXT,
    created_at TEXT NOT NULL,
    grade INTEGER NOT NULL DEFAULT 7,
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);

CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    grade INTEGER NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS papers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER NOT NULL,
    title TEXT,
    questions_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (chapter_id) REFERENCES chapters(id)
);

CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id INTEGER NOT NULL,
    total_score REAL NOT NULL,
    max_score REAL NOT NULL,
    percentage REAL NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (paper_id) REFERENCES papers(id)
);

CREATE TABLE IF NOT EXISTS answer_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id INTEGER NOT NULL,
    q_index INTEGER NOT NULL,
    topic TEXT,
    question_text TEXT,
    q_type TEXT,
    max_marks REAL,
    awarded REAL,
    student_answer TEXT,
    correct_answer TEXT,
    feedback TEXT,
    skill_category TEXT,
    FOREIGN KEY (attempt_id) REFERENCES attempts(id)
);
"""

# Columns added after the initial release — applied via ALTER TABLE for
# existing databases (CREATE TABLE above already includes them for new DBs).
MIGRATIONS = [
    ("answer_records", "skill_category", "TEXT"),
    ("chapters", "lesson_json", "TEXT"),
    ("chapters", "grade", "INTEGER NOT NULL DEFAULT 7"),
]


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript(SCHEMA)
    for table, column, col_type in MIGRATIONS:
        existing = [row["name"] for row in conn.execute(f"PRAGMA table_info({table})")]
        if column not in existing:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
    conn.commit()
    conn.close()

    from core import seed_data
    seed_data.ensure_seeded()


def now():
    return datetime.now().isoformat(timespec="seconds")


# ---------------------------------------------------------------- subjects
def get_or_create_subject(name):
    conn = get_conn()
    cur = conn.execute("SELECT id FROM subjects WHERE name = ?", (name,))
    row = cur.fetchone()
    if row:
        conn.close()
        return row["id"]
    try:
        cur = conn.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
        conn.commit()
        sid = cur.lastrowid
    except sqlite3.IntegrityError:
        # Another concurrent request inserted this subject between our SELECT
        # and INSERT (e.g. two Streamlit sessions both running init_db() on
        # startup) - fall back to the row that won the race.
        row = conn.execute("SELECT id FROM subjects WHERE name = ?", (name,)).fetchone()
        sid = row["id"]
    conn.close()
    return sid


def list_subjects():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM subjects ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------- chapters
def add_chapter(subject_id, name, summary, source_file, grade=7):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO chapters (subject_id, name, summary, source_file, created_at, grade) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (subject_id, name, summary, source_file, now(), grade),
    )
    conn.commit()
    cid = cur.lastrowid
    conn.close()
    return cid


def list_chapters(subject_id=None, grade=None):
    conn = get_conn()
    query = "SELECT * FROM chapters WHERE 1=1"
    params = []
    if subject_id:
        query += " AND subject_id = ?"
        params.append(subject_id)
    if grade:
        query += " AND grade = ?"
        params.append(grade)
    query += " ORDER BY created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_lesson(chapter_id, lesson_json):
    conn = get_conn()
    conn.execute("UPDATE chapters SET lesson_json = ? WHERE id = ?", (lesson_json, chapter_id))
    conn.commit()
    conn.close()


def get_chapter_by_name(subject_id, name):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM chapters WHERE subject_id = ? AND name = ?", (subject_id, name)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# --------------------------------------------------------------- profiles
def list_profiles():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM profiles ORDER BY created_at").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_profile(name, grade):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO profiles (name, grade, created_at) VALUES (?, ?, ?)",
        (name, grade, now()),
    )
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid


def get_profile(profile_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_chapter(chapter_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ------------------------------------------------------------------ papers
def save_paper(chapter_id, title, questions):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO papers (chapter_id, title, questions_json, created_at) VALUES (?, ?, ?, ?)",
        (chapter_id, title, json.dumps(questions), now()),
    )
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid


def get_paper(paper_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM papers WHERE id = ?", (paper_id,)).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["questions"] = json.loads(d["questions_json"])
    return d


def list_papers(chapter_id=None):
    conn = get_conn()
    if chapter_id:
        rows = conn.execute(
            "SELECT * FROM papers WHERE chapter_id = ? ORDER BY created_at DESC",
            (chapter_id,),
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM papers ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------- attempts
def save_attempt(paper_id, total_score, max_score, records):
    percentage = round(100 * total_score / max_score, 2) if max_score else 0.0
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO attempts (paper_id, total_score, max_score, percentage, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (paper_id, total_score, max_score, percentage, now()),
    )
    attempt_id = cur.lastrowid
    for r in records:
        conn.execute(
            "INSERT INTO answer_records "
            "(attempt_id, q_index, topic, question_text, q_type, max_marks, awarded, "
            "student_answer, correct_answer, feedback, skill_category) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                attempt_id,
                r.get("q_index"),
                r.get("topic"),
                r.get("question_text"),
                r.get("q_type"),
                r.get("max_marks"),
                r.get("awarded"),
                r.get("student_answer"),
                r.get("correct_answer"),
                r.get("feedback"),
                r.get("skill_category"),
            ),
        )
    conn.commit()
    conn.close()
    return attempt_id


def get_attempt(attempt_id):
    conn = get_conn()
    attempt = conn.execute("SELECT * FROM attempts WHERE id = ?", (attempt_id,)).fetchone()
    records = conn.execute(
        "SELECT * FROM answer_records WHERE attempt_id = ? ORDER BY q_index", (attempt_id,)
    ).fetchall()
    conn.close()
    return dict(attempt), [dict(r) for r in records]


def get_attempts_for_subject(subject_id, grade=None):
    conn = get_conn()
    query = """
        SELECT a.*, p.title, p.chapter_id, c.name AS chapter_name
        FROM attempts a
        JOIN papers p ON p.id = a.paper_id
        JOIN chapters c ON c.id = p.chapter_id
        WHERE c.subject_id = ?
        """
    params = [subject_id]
    if grade:
        query += " AND c.grade = ?"
        params.append(grade)
    query += " ORDER BY a.created_at"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_topic_performance(subject_id, grade=None):
    conn = get_conn()
    query = """
        SELECT ar.topic, ar.awarded, ar.max_marks, a.created_at
        FROM answer_records ar
        JOIN attempts a ON a.id = ar.attempt_id
        JOIN papers p ON p.id = a.paper_id
        JOIN chapters c ON c.id = p.chapter_id
        WHERE c.subject_id = ? AND ar.topic IS NOT NULL
        """
    params = [subject_id]
    if grade:
        query += " AND c.grade = ?"
        params.append(grade)
    query += " ORDER BY a.created_at"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_skill_category_performance(subject_id, grade=None):
    conn = get_conn()
    query = """
        SELECT ar.skill_category, ar.awarded, ar.max_marks, a.created_at
        FROM answer_records ar
        JOIN attempts a ON a.id = ar.attempt_id
        JOIN papers p ON p.id = a.paper_id
        JOIN chapters c ON c.id = p.chapter_id
        WHERE c.subject_id = ? AND ar.skill_category IS NOT NULL AND ar.skill_category != ''
        """
    params = [subject_id]
    if grade:
        query += " AND c.grade = ?"
        params.append(grade)
    query += " ORDER BY a.created_at"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]
