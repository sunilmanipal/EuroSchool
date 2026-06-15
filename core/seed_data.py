"""Ensures the demo content for each seeded chapter (analysis, lesson with
deep-dives and interactive quick-checks, and a practice paper) exists in the
database. Called automatically from db.init_db(), so a freshly deployed app
(e.g. on Render, where the local SQLite file starts empty) always has these
chapters ready to use — no manual seeding step required.

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

from scripts import seed_integers_chapter as _integers
from scripts import update_integers_lesson as _integers_lesson
from scripts import update_integers_quickcheck as _integers_quickcheck
from scripts import seed_nutrition_chapter as _nutrition


def _build_integers_lesson():
    lesson = json.loads(json.dumps(_integers_lesson.LESSON))  # deep copy
    for topic in lesson["topics"]:
        name = topic["topic"]
        if name in _integers_quickcheck.QUICK_CHECKS:
            topic["quick_check"] = _integers_quickcheck.QUICK_CHECKS[name]
    return lesson


_CHAPTERS = [
    {
        "subject": _integers.SUBJECT,
        "chapter_name": _integers.CHAPTER_NAME,
        "analysis": _integers.ANALYSIS,
        "source_file": _integers.SOURCE_FILE,
        "grade": getattr(_integers, "GRADE", 7),
        "build_lesson": _build_integers_lesson,
        "paper_title": _integers.PAPER_TITLE,
        "questions": _integers.QUESTIONS,
    },
    {
        "subject": _nutrition.SUBJECT,
        "chapter_name": _nutrition.CHAPTER_NAME,
        "analysis": _nutrition.ANALYSIS,
        "source_file": _nutrition.SOURCE_FILE,
        "grade": _nutrition.GRADE,
        "build_lesson": lambda: _nutrition.LESSON,
        "paper_title": _nutrition.PAPER_TITLE,
        "questions": _nutrition.QUESTIONS,
    },
]


def ensure_seeded():
    from core import db

    for spec in _CHAPTERS:
        subject_id = db.get_or_create_subject(spec["subject"])
        if db.get_chapter_by_name(subject_id, spec["chapter_name"]):
            continue  # already seeded

        chapter_id = db.add_chapter(
            subject_id, spec["chapter_name"], json.dumps(spec["analysis"]),
            spec["source_file"], grade=spec["grade"],
        )
        db.save_lesson(chapter_id, json.dumps(spec["build_lesson"]()))
        db.save_paper(chapter_id, spec["paper_title"], spec["questions"])
