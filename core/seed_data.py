"""Ensures the 'Chapter 1 - Integers' demo content (analysis, lesson with
deep-dives and interactive quick-checks, and a practice paper) exists in the
database. Called automatically from db.init_db(), so a freshly deployed app
(e.g. on Render, where the local SQLite file starts empty) always has this
chapter ready to use — no manual seeding step required.

This module reuses the content defined in the one-off scripts under
scripts/, whose db-writing code only runs when executed directly
(`if __name__ == "__main__":`), so importing them here has no side effects.
"""
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts import seed_integers_chapter as _seed
from scripts import update_integers_lesson as _lesson
from scripts import update_integers_quickcheck as _quickcheck


def _build_lesson():
    lesson = json.loads(json.dumps(_lesson.LESSON))  # deep copy
    for topic in lesson["topics"]:
        name = topic["topic"]
        if name in _quickcheck.QUICK_CHECKS:
            topic["quick_check"] = _quickcheck.QUICK_CHECKS[name]
    return lesson


# Chapters that were seeded by mistake in a previous version and should be
# removed from any existing database on startup (the app only seeds content
# that was actually uploaded by the user, not pre-authored demo chapters).
_REMOVE_CHAPTERS = [
    ("Science", "Chapter 1 - Nutrition in Plants"),
]


def _remove_stale_chapters():
    from core import db

    conn = db.get_conn()
    for subject_name, chapter_name in _REMOVE_CHAPTERS:
        row = conn.execute("SELECT id FROM subjects WHERE name = ?", (subject_name,)).fetchone()
        if not row:
            continue
        subject_id = row["id"]
        chap = conn.execute(
            "SELECT id FROM chapters WHERE subject_id = ? AND name = ? AND source_file = 'hand-authored'",
            (subject_id, chapter_name),
        ).fetchone()
        if chap:
            chapter_id = chap["id"]
            paper_ids = [r["id"] for r in conn.execute("SELECT id FROM papers WHERE chapter_id = ?", (chapter_id,))]
            for paper_id in paper_ids:
                attempt_ids = [r["id"] for r in conn.execute("SELECT id FROM attempts WHERE paper_id = ?", (paper_id,))]
                for attempt_id in attempt_ids:
                    conn.execute("DELETE FROM answer_records WHERE attempt_id = ?", (attempt_id,))
                conn.execute("DELETE FROM attempts WHERE paper_id = ?", (paper_id,))
            conn.execute("DELETE FROM papers WHERE chapter_id = ?", (chapter_id,))
            conn.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))
        # Remove the subject too if it has no chapters left
        remaining = conn.execute("SELECT COUNT(*) AS c FROM chapters WHERE subject_id = ?", (subject_id,)).fetchone()
        if remaining["c"] == 0:
            conn.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
    conn.commit()
    conn.close()


def ensure_seeded():
    from core import db

    _remove_stale_chapters()

    subject_id = db.get_or_create_subject(_seed.SUBJECT)
    if db.get_chapter_by_name(subject_id, _seed.CHAPTER_NAME):
        return  # already seeded

    chapter_id = db.add_chapter(
        subject_id, _seed.CHAPTER_NAME, json.dumps(_seed.ANALYSIS), _seed.SOURCE_FILE
    )
    db.save_lesson(chapter_id, json.dumps(_build_lesson()))
    db.save_paper(chapter_id, _seed.PAPER_TITLE, _seed.QUESTIONS)
