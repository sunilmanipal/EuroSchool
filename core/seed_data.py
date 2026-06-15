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


def ensure_seeded():
    from core import db

    subject_id = db.get_or_create_subject(_seed.SUBJECT)
    if db.get_chapter_by_name(subject_id, _seed.CHAPTER_NAME):
        return  # already seeded

    chapter_id = db.add_chapter(
        subject_id, _seed.CHAPTER_NAME, json.dumps(_seed.ANALYSIS), _seed.SOURCE_FILE
    )
    db.save_lesson(chapter_id, json.dumps(_build_lesson()))
    db.save_paper(chapter_id, _seed.PAPER_TITLE, _seed.QUESTIONS)
