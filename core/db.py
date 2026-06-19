"""Persistence layer for the exam-prep dashboard.

Supports SQLite for local development and PostgreSQL for production
(Supabase / any hosted Postgres). The DATABASE_URL environment variable
or Streamlit secret selects which backend is used:

    sqlite:////path/to/app.db          → local SQLite (default)
    postgresql://user:pass@host/dbname → Supabase / hosted Postgres
"""
import json
import os
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, inspect as sa_inspect, text

# ── Resolve database URL ───────────────────────────────────────────────────────

_DEFAULT_SQLITE = "sqlite:///" + str(
    Path(__file__).resolve().parent.parent / "data" / "app.db"
)


def _resolve_url() -> str:
    # 1. Streamlit Community Cloud secrets
    try:
        import streamlit as st
        url = (
            st.secrets.get("DATABASE_URL")
            or (st.secrets.get("database") or {}).get("url")
        )
        if url:
            return url.replace("postgres://", "postgresql://", 1)
    except Exception:
        pass
    # 2. Environment variable (.env or Render/Railway)
    url = os.environ.get("DATABASE_URL", _DEFAULT_SQLITE)
    return url.replace("postgres://", "postgresql://", 1)


_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        url = _resolve_url()
        if url.startswith("postgresql"):
            _engine = create_engine(
                url,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10,
                future=True,
            )
        else:
            Path(url.replace("sqlite:///", "")).parent.mkdir(parents=True, exist_ok=True)
            _engine = create_engine(
                url,
                connect_args={"check_same_thread": False},
                future=True,
            )
    return _engine


def _pg() -> bool:
    return _resolve_url().startswith("postgresql")


# ── Helpers ────────────────────────────────────────────────────────────────────

def _row(r):
    return dict(r._mapping) if r is not None else None


def _rows(rs):
    return [dict(r._mapping) for r in rs]


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _serial():
    return "SERIAL PRIMARY KEY" if _pg() else "INTEGER PRIMARY KEY AUTOINCREMENT"


def _insert(conn, sql: str, params: dict) -> int:
    """Run an INSERT and return the new row id (works on both dialects)."""
    if _pg():
        row = conn.execute(text(sql + " RETURNING id"), params).fetchone()
        return row[0]
    result = conn.execute(text(sql), params)
    return result.lastrowid


# ── Schema ─────────────────────────────────────────────────────────────────────

def _schema_statements():
    pk = _serial()
    return [
        f"""CREATE TABLE IF NOT EXISTS subjects (
            id {pk}, name TEXT UNIQUE NOT NULL
        )""",
        f"""CREATE TABLE IF NOT EXISTS chapters (
            id {pk},
            subject_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            summary TEXT,
            source_file TEXT,
            lesson_json TEXT,
            created_at TEXT NOT NULL,
            grade INTEGER NOT NULL DEFAULT 7
        )""",
        f"""CREATE TABLE IF NOT EXISTS profiles (
            id {pk},
            name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )""",
        f"""CREATE TABLE IF NOT EXISTS papers (
            id {pk},
            chapter_id INTEGER NOT NULL,
            title TEXT,
            questions_json TEXT NOT NULL,
            topic_name TEXT,
            created_at TEXT NOT NULL
        )""",
        f"""CREATE TABLE IF NOT EXISTS attempts (
            id {pk},
            paper_id INTEGER NOT NULL,
            profile_id INTEGER,
            total_score REAL NOT NULL,
            max_score REAL NOT NULL,
            percentage REAL NOT NULL,
            created_at TEXT NOT NULL
        )""",
        f"""CREATE TABLE IF NOT EXISTS answer_records (
            id {pk},
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
            skill_category TEXT
        )""",
        f"""CREATE TABLE IF NOT EXISTS quick_check_progress (
            id {pk},
            profile_id INTEGER NOT NULL,
            chapter_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            q_index INTEGER NOT NULL,
            solved INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL,
            UNIQUE(profile_id, chapter_id, topic, q_index)
        )""",
    ]


# Columns added after initial release — applied via ALTER TABLE on existing DBs.
_MIGRATIONS = [
    ("answer_records", "skill_category", "TEXT"),
    ("chapters", "lesson_json", "TEXT"),
    ("chapters", "grade", "INTEGER NOT NULL DEFAULT 7"),
    ("papers", "topic_name", "TEXT"),
    ("attempts", "profile_id", "INTEGER"),
]


def init_db():
    engine = _get_engine()
    with engine.connect() as conn:
        for stmt in _schema_statements():
            conn.execute(text(stmt))

        # Run column-level migrations
        inspector = sa_inspect(engine)
        for table, column, col_type in _MIGRATIONS:
            try:
                existing = [c["name"] for c in inspector.get_columns(table)]
                if column not in existing:
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"))
            except Exception:
                pass

        conn.commit()

    from core import seed_data
    seed_data.ensure_seeded()


# ── Subjects ───────────────────────────────────────────────────────────────────

def get_or_create_subject(name: str) -> int:
    with _get_engine().connect() as conn:
        row = conn.execute(text("SELECT id FROM subjects WHERE name = :n"), {"n": name}).fetchone()
        if row:
            return row[0]
        try:
            sid = _insert(conn, "INSERT INTO subjects (name) VALUES (:n)", {"n": name})
            conn.commit()
            return sid
        except Exception:
            conn.rollback()
            row = conn.execute(text("SELECT id FROM subjects WHERE name = :n"), {"n": name}).fetchone()
            return row[0]


def list_subjects():
    with _get_engine().connect() as conn:
        return _rows(conn.execute(text("SELECT * FROM subjects ORDER BY name")).fetchall())


# ── Chapters ───────────────────────────────────────────────────────────────────

def add_chapter(subject_id, name, summary, source_file, grade=7) -> int:
    with _get_engine().connect() as conn:
        cid = _insert(
            conn,
            "INSERT INTO chapters (subject_id, name, summary, source_file, created_at, grade) "
            "VALUES (:s, :n, :sum, :sf, :ca, :g)",
            {"s": subject_id, "n": name, "sum": summary, "sf": source_file, "ca": now(), "g": grade},
        )
        conn.commit()
        return cid


def list_chapters(subject_id=None, grade=None):
    q = "SELECT * FROM chapters WHERE 1=1"
    params = {}
    if subject_id:
        q += " AND subject_id = :sid"
        params["sid"] = subject_id
    if grade:
        q += " AND grade = :g"
        params["g"] = grade
    q += " ORDER BY created_at DESC"
    with _get_engine().connect() as conn:
        return _rows(conn.execute(text(q), params).fetchall())


def save_lesson(chapter_id, lesson_json: str):
    with _get_engine().connect() as conn:
        conn.execute(
            text("UPDATE chapters SET lesson_json = :lj WHERE id = :id"),
            {"lj": lesson_json, "id": chapter_id},
        )
        conn.commit()


def get_chapter(chapter_id):
    with _get_engine().connect() as conn:
        return _row(conn.execute(text("SELECT * FROM chapters WHERE id = :id"), {"id": chapter_id}).fetchone())


def get_chapter_by_name(subject_id, name):
    with _get_engine().connect() as conn:
        return _row(
            conn.execute(
                text("SELECT * FROM chapters WHERE subject_id = :s AND name = :n"),
                {"s": subject_id, "n": name},
            ).fetchone()
        )


# ── Profiles ───────────────────────────────────────────────────────────────────

def list_profiles():
    with _get_engine().connect() as conn:
        return _rows(conn.execute(text("SELECT * FROM profiles ORDER BY created_at")).fetchall())


def create_profile(name, grade) -> int:
    with _get_engine().connect() as conn:
        pid = _insert(
            conn,
            "INSERT INTO profiles (name, grade, created_at) VALUES (:n, :g, :ca)",
            {"n": name, "g": grade, "ca": now()},
        )
        conn.commit()
        return pid


def get_profile(profile_id):
    with _get_engine().connect() as conn:
        return _row(conn.execute(text("SELECT * FROM profiles WHERE id = :id"), {"id": profile_id}).fetchone())


# ── Papers ─────────────────────────────────────────────────────────────────────

def save_paper(chapter_id, title, questions, topic_name=None) -> int:
    with _get_engine().connect() as conn:
        pid = _insert(
            conn,
            "INSERT INTO papers (chapter_id, title, questions_json, created_at, topic_name) "
            "VALUES (:c, :t, :q, :ca, :tn)",
            {"c": chapter_id, "t": title, "q": json.dumps(questions), "ca": now(), "tn": topic_name},
        )
        conn.commit()
        return pid


def get_paper(paper_id):
    with _get_engine().connect() as conn:
        row = _row(conn.execute(text("SELECT * FROM papers WHERE id = :id"), {"id": paper_id}).fetchone())
    if not row:
        return None
    row["questions"] = json.loads(row["questions_json"])
    return row


def list_papers(chapter_id=None):
    q = "SELECT * FROM papers"
    params = {}
    if chapter_id:
        q += " WHERE chapter_id = :c"
        params["c"] = chapter_id
    q += " ORDER BY created_at DESC"
    with _get_engine().connect() as conn:
        return _rows(conn.execute(text(q), params).fetchall())


# ── Attempts ───────────────────────────────────────────────────────────────────

def save_attempt(paper_id, total_score, max_score, records, profile_id=None) -> int:
    percentage = round(100 * total_score / max_score, 2) if max_score else 0.0
    with _get_engine().connect() as conn:
        aid = _insert(
            conn,
            "INSERT INTO attempts (paper_id, total_score, max_score, percentage, created_at, profile_id) "
            "VALUES (:p, :ts, :ms, :pct, :ca, :pid)",
            {"p": paper_id, "ts": total_score, "ms": max_score, "pct": percentage, "ca": now(), "pid": profile_id},
        )
        for r in records:
            _insert(
                conn,
                "INSERT INTO answer_records "
                "(attempt_id, q_index, topic, question_text, q_type, max_marks, awarded, "
                "student_answer, correct_answer, feedback, skill_category) "
                "VALUES (:aid,:qi,:t,:qt,:qtype,:mm,:aw,:sa,:ca,:fb,:sc)",
                {
                    "aid": aid, "qi": r.get("q_index"), "t": r.get("topic"),
                    "qt": r.get("question_text"), "qtype": r.get("q_type"),
                    "mm": r.get("max_marks"), "aw": r.get("awarded"),
                    "sa": r.get("student_answer"), "ca": r.get("correct_answer"),
                    "fb": r.get("feedback"), "sc": r.get("skill_category"),
                },
            )
        conn.commit()
        return aid


def get_attempt(attempt_id):
    with _get_engine().connect() as conn:
        attempt = _row(conn.execute(text("SELECT * FROM attempts WHERE id = :id"), {"id": attempt_id}).fetchone())
        records = _rows(
            conn.execute(
                text("SELECT * FROM answer_records WHERE attempt_id = :id ORDER BY q_index"),
                {"id": attempt_id},
            ).fetchall()
        )
    return attempt, records


def get_attempts_for_subject(subject_id, grade=None):
    q = """
        SELECT a.*, p.title, p.chapter_id, c.name AS chapter_name
        FROM attempts a
        JOIN papers p ON p.id = a.paper_id
        JOIN chapters c ON c.id = p.chapter_id
        WHERE c.subject_id = :sid
    """
    params = {"sid": subject_id}
    if grade:
        q += " AND c.grade = :g"
        params["g"] = grade
    q += " ORDER BY a.created_at"
    with _get_engine().connect() as conn:
        return _rows(conn.execute(text(q), params).fetchall())


def get_topic_performance(subject_id, grade=None):
    q = """
        SELECT ar.topic, ar.awarded, ar.max_marks, a.created_at
        FROM answer_records ar
        JOIN attempts a ON a.id = ar.attempt_id
        JOIN papers p ON p.id = a.paper_id
        JOIN chapters c ON c.id = p.chapter_id
        WHERE c.subject_id = :sid AND ar.topic IS NOT NULL
    """
    params = {"sid": subject_id}
    if grade:
        q += " AND c.grade = :g"
        params["g"] = grade
    q += " ORDER BY a.created_at"
    with _get_engine().connect() as conn:
        return _rows(conn.execute(text(q), params).fetchall())


def get_skill_category_performance(subject_id, grade=None):
    q = """
        SELECT ar.skill_category, ar.awarded, ar.max_marks, a.created_at
        FROM answer_records ar
        JOIN attempts a ON a.id = ar.attempt_id
        JOIN papers p ON p.id = a.paper_id
        JOIN chapters c ON c.id = p.chapter_id
        WHERE c.subject_id = :sid
          AND ar.skill_category IS NOT NULL AND ar.skill_category != ''
    """
    params = {"sid": subject_id}
    if grade:
        q += " AND c.grade = :g"
        params["g"] = grade
    q += " ORDER BY a.created_at"
    with _get_engine().connect() as conn:
        return _rows(conn.execute(text(q), params).fetchall())


# ── Quick-check progress ───────────────────────────────────────────────────────

def set_quick_check_solved(profile_id, chapter_id, topic, q_index, solved=True):
    if _pg():
        sql = """
            INSERT INTO quick_check_progress
                (profile_id, chapter_id, topic, q_index, solved, updated_at)
            VALUES (:pid, :cid, :t, :qi, :s, :ua)
            ON CONFLICT (profile_id, chapter_id, topic, q_index)
            DO UPDATE SET solved = EXCLUDED.solved, updated_at = EXCLUDED.updated_at
        """
    else:
        sql = """
            INSERT INTO quick_check_progress
                (profile_id, chapter_id, topic, q_index, solved, updated_at)
            VALUES (:pid, :cid, :t, :qi, :s, :ua)
            ON CONFLICT(profile_id, chapter_id, topic, q_index)
            DO UPDATE SET solved=excluded.solved, updated_at=excluded.updated_at
        """
    params = {
        "pid": profile_id, "cid": chapter_id, "t": topic,
        "qi": q_index, "s": int(solved), "ua": now(),
    }
    with _get_engine().connect() as conn:
        conn.execute(text(sql), params)
        conn.commit()


def get_quick_check_progress(profile_id, chapter_id):
    with _get_engine().connect() as conn:
        rows = conn.execute(
            text("SELECT topic, q_index, solved FROM quick_check_progress "
                 "WHERE profile_id = :pid AND chapter_id = :cid"),
            {"pid": profile_id, "cid": chapter_id},
        ).fetchall()
    return {(r[0], r[1]): bool(r[2]) for r in rows}


def get_topic_assessment_attempts(profile_id, chapter_id, topic_name):
    with _get_engine().connect() as conn:
        return _rows(
            conn.execute(
                text("""
                    SELECT a.* FROM attempts a
                    JOIN papers p ON p.id = a.paper_id
                    WHERE p.chapter_id = :cid AND p.topic_name = :tn AND a.profile_id = :pid
                    ORDER BY a.created_at DESC
                """),
                {"cid": chapter_id, "tn": topic_name, "pid": profile_id},
            ).fetchall()
        )


# ── seed_data compatibility shim ───────────────────────────────────────────────
# seed_data.py calls get_conn() and uses raw sqlite3-style conn.execute().
# We expose a thin wrapper that delegates to SQLAlchemy so seed_data works
# without modification.

class _ConnShim:
    """Wraps a SQLAlchemy connection to look like sqlite3 for seed_data.py."""

    def __init__(self, conn):
        self._c = conn

    def execute(self, sql, params=()):
        if isinstance(params, (list, tuple)):
            # positional → convert to dict (sqlite3 uses ? placeholders)
            if "?" in sql:
                # replace ? with :p0, :p1, ...
                for i in range(len(params)):
                    sql = sql.replace("?", f":_p{i}", 1)
                params = {f"_p{i}": v for i, v in enumerate(params)}
            else:
                params = {}
        result = self._c.execute(text(sql), params)

        class _FakeResult:
            def __init__(self, r):
                self._r = r
                self.lastrowid = None

            def fetchone(self_r):
                row = self_r._r.fetchone()
                return _DictRow(row) if row else None

            def fetchall(self_r):
                return [_DictRow(r) for r in self_r._r.fetchall()]

            def __iter__(self_r):
                for r in self_r._r:
                    yield _DictRow(r)

        fr = _FakeResult(result)
        # capture lastrowid for INSERT statements
        if sql.strip().upper().startswith("INSERT") and _pg():
            pass  # seed_data doesn't use lastrowid
        return fr

    def executescript(self, script):
        for stmt in script.split(";"):
            s = stmt.strip()
            if s:
                try:
                    self._c.execute(text(s))
                except Exception:
                    pass

    def commit(self):
        self._c.commit()

    def close(self):
        self._c.close()


class _DictRow:
    def __init__(self, row):
        self._d = dict(row._mapping)

    def __getitem__(self, key):
        return self._d[key]

    def __iter__(self):
        return iter(self._d.values())

    def keys(self):
        return self._d.keys()

    def get(self, key, default=None):
        return self._d.get(key, default)


def get_conn():
    """Return a shim connection compatible with seed_data.py's sqlite3 usage."""
    conn = _get_engine().connect()
    return _ConnShim(conn)
