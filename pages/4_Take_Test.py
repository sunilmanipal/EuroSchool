import json

import streamlit as st
from dotenv import load_dotenv

from core import ai_engine, db
from core.auth_ui import require_login

load_dotenv()
db.init_db()

st.set_page_config(page_title="Take Test", page_icon="✍️", layout="wide")
profile = require_login()
st.title("✍️ Take a Test")

grade = profile["grade"]
subjects = db.list_subjects()
subjects = [s for s in subjects if db.list_chapters(s["id"], grade=grade)]
if not subjects:
    st.warning(f"No chapters yet for Grade {grade}. Upload material first on the **📤 Upload Material** page.")
    st.stop()

subject_names = [s["name"] for s in subjects]
subj_choice = st.selectbox("Subject", subject_names)
subject_id = next(s["id"] for s in subjects if s["name"] == subj_choice)

chapters = db.list_chapters(subject_id, grade=grade)
if not chapters:
    st.warning(f"No chapters uploaded yet for {subj_choice} (Grade {grade}).")
    st.stop()

chapter_labels = [c["name"] for c in chapters]
chap_idx = st.selectbox("Chapter / Topic", range(len(chapters)), format_func=lambda i: chapter_labels[i])
chapter = chapters[chap_idx]

papers = db.list_papers(chapter["id"])
if not papers:
    st.warning("No question papers generated yet for this chapter. Go to **📝 Generate Test** first.")
    st.stop()

paper_labels = [f"{p['title']} (created {p['created_at'][:16]})" for p in papers]
default_idx = 0
active_id = st.session_state.get("active_paper_id")
if active_id:
    for i, p in enumerate(papers):
        if p["id"] == active_id:
            default_idx = i
paper_idx = st.selectbox("Paper", range(len(papers)), format_func=lambda i: paper_labels[i], index=default_idx)
paper = db.get_paper(papers[paper_idx]["id"])
questions = paper["questions"]

st.subheader(paper["title"])
total_marks = sum(q.get("max_marks", 1) for q in questions)
st.caption(f"{len(questions)} questions · {total_marks} marks total")

with st.expander("ℹ️ How will this be graded?", expanded=False):
    st.markdown(
        "- **🔵 Multiple choice (MCQ):** pick the correct option — graded **instantly**.\n"
        "- **🟢 Numeric / Show-your-work problems:** type your working **step by step**, "
        "then write the final answer on the last line. The AI tutor checks your steps "
        "and final answer, and gives **partial credit** if your method is right but you "
        "made a small slip.\n"
        "- **🟣 Short answer:** write 1-2 sentences. Graded by AI for correctness and "
        "completeness.\n"
        "- **🟠 Long answer:** write a few sentences / a paragraph. Graded by AI for "
        "content, with partial credit for partially correct points.\n\n"
        "Every answer gets **written feedback** explaining what was right, what was "
        "missing, and the model answer — so your son learns from every attempt."
    )

TYPE_LABELS = {
    "mcq": ("🔵 Multiple Choice", "Choose the correct option."),
    "numeric": ("🟢 Solve & Answer", "Show your working step by step, then write your final answer on the last line."),
    "short": ("🟣 Short Answer", "Write a short answer (1-2 sentences)."),
    "long": ("🟠 Long Answer", "Write a detailed answer (a few sentences / a paragraph)."),
}

result_key = f"result_{paper['id']}"

with st.form(key=f"test_form_{paper['id']}"):
    answers = {}
    for q in questions:
        label, help_text = TYPE_LABELS.get(q["type"], ("Question", ""))
        with st.container(border=True):
            st.markdown(
                f"**Q{q['q_index'] + 1}. {label} · {q.get('max_marks', 1)} mark"
                f"{'s' if q.get('max_marks', 1) != 1 else ''}**"
            )
            st.caption(f"Topic: {q.get('topic','')} · Category: {q.get('skill_category','')}")
            st.write(q["question"])

            if q["type"] == "mcq" and q.get("options"):
                answers[q["q_index"]] = st.radio(
                    help_text, q["options"], index=None, key=f"q_{paper['id']}_{q['q_index']}"
                )
            elif q["type"] == "long":
                answers[q["q_index"]] = st.text_area(
                    help_text, key=f"q_{paper['id']}_{q['q_index']}", height=150,
                    placeholder="Write your answer here...",
                )
            elif q["type"] == "numeric":
                answers[q["q_index"]] = st.text_area(
                    help_text, key=f"q_{paper['id']}_{q['q_index']}", height=110,
                    placeholder="Step 1: ...\nStep 2: ...\nFinal answer: ...",
                )
            else:  # short
                answers[q["q_index"]] = st.text_area(
                    help_text, key=f"q_{paper['id']}_{q['q_index']}", height=80,
                    placeholder="Write your answer here...",
                )

    submitted = st.form_submit_button("✅ Submit for Grading", type="primary", use_container_width=True)

if submitted:
    progress = st.progress(0, text="Starting grading...")
    records = []
    total_score = 0.0
    for i, q in enumerate(questions):
        progress.progress(
            i / len(questions),
            text=f"Grading question {i + 1} of {len(questions)}...",
        )
        student_answer = answers.get(q["q_index"]) or ""
        if q["type"] == "mcq":
            grade = ai_engine.grade_mcq_answer(q, student_answer)
        else:
            grade = ai_engine.grade_subjective_answer(subj_choice, q, student_answer)
        awarded = float(grade.get("awarded", 0))
        total_score += awarded
        records.append(
            {
                "q_index": q["q_index"],
                "topic": q.get("topic"),
                "question_text": q["question"],
                "q_type": q["type"],
                "max_marks": q.get("max_marks", 1),
                "awarded": awarded,
                "student_answer": student_answer,
                "correct_answer": q.get("correct_answer"),
                "feedback": grade.get("feedback", ""),
                "skill_category": q.get("skill_category", ""),
            }
        )
    progress.progress(1.0, text="Done!")
    attempt_id = db.save_attempt(paper["id"], total_score, total_marks, records)
    st.session_state[result_key] = (attempt_id, total_score, total_marks, records)
    progress.empty()

if result_key in st.session_state:
    attempt_id, total_score, total_marks, records = st.session_state[result_key]
    pct = round(100 * total_score / total_marks, 1) if total_marks else 0
    st.success(f"## Score: {total_score:.1f} / {total_marks}  ({pct}%)")

    needs_work = [r for r in records if r["awarded"] < r["max_marks"] - 1e-6]
    if needs_work:
        st.markdown("**📌 Focus on these next:** " + ", ".join(sorted({r["topic"] for r in needs_work if r["topic"]})))

    for r in records:
        q = questions[r["q_index"]]
        ok = r["awarded"] >= r["max_marks"] - 1e-6
        partial = 0 < r["awarded"] < r["max_marks"]
        icon = "✅" if ok else ("🟡" if partial else "❌")
        with st.expander(f"{icon} Q{r['q_index']+1} — {r['awarded']}/{r['max_marks']} marks — {r['topic']}"):
            st.write(f"**Question:** {r['question_text']}")
            st.write(f"**Your answer:** {r['student_answer'] or '_(blank)_'}")
            st.write(f"**Correct/model answer:** {r['correct_answer']}")
            st.write(f"**Feedback:** {r['feedback']}")
            if q.get("explanation"):
                st.write(f"**Explanation:** {q['explanation']}")

    st.info("Check **📊 Analytics** to see updated topic-wise mastery and score predictions.")
