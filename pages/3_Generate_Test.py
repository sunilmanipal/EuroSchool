import json

import streamlit as st
from dotenv import load_dotenv

from core import ai_engine, db, question_bank
from core.auth_ui import require_login
from core.ui import render_page_header

load_dotenv()
db.init_db()

st.set_page_config(page_title="Generate Test", page_icon="📝", layout="wide")
profile = require_login()
render_page_header(
    "📝 Generate a Practice Question Paper",
    "Create a fresh, balanced practice paper for any chapter — tuned to difficulty, "
    "skill mix, and topics that need extra focus.",
)

grade = profile["grade"]
subjects = db.list_subjects()
subjects = [s for s in subjects if db.list_chapters(s["id"], grade=grade)]
if not subjects:
    st.warning(f"No chapters yet for Grade {grade}. Upload material first on the **📤 Upload Material** page.")
    st.stop()

subject_names = [s["name"] for s in subjects]

last_chapter_id = st.session_state.get("last_chapter_id")
default_subj_idx = 0
if last_chapter_id:
    for i, s in enumerate(subjects):
        if any(c["id"] == last_chapter_id for c in db.list_chapters(s["id"], grade=grade)):
            default_subj_idx = i
            break

subj_choice = st.selectbox("Subject", subject_names, index=default_subj_idx)
subject_id = next(s["id"] for s in subjects if s["name"] == subj_choice)

chapters = db.list_chapters(subject_id, grade=grade)
if not chapters:
    st.warning(f"No chapters uploaded yet for {subj_choice} (Grade {grade}).")
    st.stop()

default_chap_idx = 0
if last_chapter_id:
    for i, c in enumerate(chapters):
        if c["id"] == last_chapter_id:
            default_chap_idx = i
            break

chapter_labels = [f"{c['name']} (uploaded {c['created_at'][:10]})" for c in chapters]
chap_idx = st.selectbox("Chapter / Topic", range(len(chapters)), format_func=lambda i: chapter_labels[i], index=default_chap_idx)
chapter = chapters[chap_idx]
analysis = json.loads(chapter["summary"])

with st.expander("What the AI knows about this chapter"):
    st.write(f"**Difficulty:** {analysis.get('difficulty')}")
    st.write("**Topics:** " + ", ".join(analysis.get("topics", [])))
    st.write(analysis.get("summary", ""))

st.info(
    "📐 **For Maths**, questions will be a mix of: quick **multiple-choice** checks "
    "(graded instantly), and **'show your work' problems** where your son types his "
    "step-by-step working in the answer box — the AI tutor checks the method and "
    "gives partial credit, just like a teacher marking a notebook."
)

col1, col2 = st.columns(2)
with col1:
    num_questions = st.slider("Number of questions", 5, 20, 10)
with col2:
    difficulty = st.select_slider("Overall difficulty", ["easy", "medium", "hard"], value="medium")

st.markdown("**Question mix (skill categories)**")
st.caption(
    "Adjust the relative weight of each skill category. These don't need to add up to "
    "100 — they're relative proportions, and the AI will distribute the questions "
    "above accordingly."
)

skill_weights = {}
cat_items = list(ai_engine.SKILL_CATEGORIES.items())
cols = st.columns(2)
for i, (cat, default_w) in enumerate(cat_items):
    with cols[i % 2]:
        skill_weights[cat] = st.slider(cat, 0, 30, default_w, key=f"weight_{cat}")

with st.expander("Preview question distribution"):
    counts = ai_engine.distribute_questions(num_questions, skill_weights)
    for cat, n in counts.items():
        st.write(f"- {cat}: {n} question(s)")

st.markdown("**🎯 Focus topics (optional)**")
topic_performance = db.get_topic_performance(subject_id, grade=grade)
weak_topics = []
if topic_performance:
    df = {}
    for r in topic_performance:
        t = r["topic"]
        df.setdefault(t, [0, 0])
        df[t][0] += r["awarded"]
        df[t][1] += r["max_marks"]
    weak_topics = [t for t, (aw, mx) in df.items() if mx and (100 * aw / mx) < 60]

all_topics = analysis.get("topics", [])
if weak_topics:
    st.caption(
        "Based on past attempts, your son is weakest in: **" + ", ".join(weak_topics) + "**. "
        "These are pre-selected below — the new paper will have more questions on these topics."
    )
focus_topics = st.multiselect(
    "Give extra questions on these topics (leave empty for a balanced paper)",
    options=all_topics,
    default=[t for t in weak_topics if t in all_topics],
)

if st.button("✨ Generate Paper", type="primary"):
    existing_papers = db.list_papers(chapter["id"])
    next_num = len(existing_papers) + 1
    default_title = f"{chapter['name']} — Practice Paper {next_num}"

    paper = None
    used_offline = False
    with st.spinner("Creating the question paper..."):
        try:
            paper = ai_engine.generate_paper(
                subject=subj_choice,
                chapter_name=chapter["name"],
                summary=analysis.get("summary", ""),
                topics=all_topics,
                sample_question_styles=analysis.get("sample_question_styles", []),
                num_questions=num_questions,
                difficulty=difficulty,
                skill_category_weights=skill_weights,
                focus_topics=focus_topics,
            )
        except Exception:
            if question_bank.chapter_supported(chapter["name"]):
                paper = question_bank.generate_offline_paper(
                    chapter_name=chapter["name"],
                    num_questions=num_questions,
                    skill_category_weights=skill_weights,
                    focus_topics=focus_topics,
                    title=default_title,
                )
                used_offline = True
            else:
                st.error(
                    "Couldn't generate a paper with AI right now (the OpenAI API key may "
                    "be out of quota), and there's no offline question bank for this "
                    "chapter yet. Please try again once AI access is restored."
                )

    if paper:
        paper.setdefault("title", default_title)
        paper_id = db.save_paper(chapter["id"], paper["title"], paper["questions"])
        st.success(f"✅ Created paper: **{paper['title']}** ({len(paper['questions'])} questions)")
        if used_offline:
            st.info(
                "ℹ️ Created using the **offline question bank** (AI generation is "
                "currently unavailable). Numbers are freshly randomized, so this is a "
                "brand-new paper — generate again any time for another one."
            )
        st.session_state["active_paper_id"] = paper_id
        st.info("Go to **✍️ Take Test** to attempt this paper now.")

st.divider()
st.subheader("Previously generated papers for this chapter")
papers = db.list_papers(chapter["id"])
for p in papers:
    q = json.loads(p["questions_json"])
    st.write(f"- **{p['title']}** — {len(q)} questions, created {p['created_at']}")
