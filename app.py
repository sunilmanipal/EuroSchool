import streamlit as st
from dotenv import load_dotenv

from core import db
from core.auth_ui import require_login
from core.ui import inject_css, render_hero

load_dotenv()
db.init_db()

st.set_page_config(page_title="StudyBuddy — Exam Prep Dashboard", page_icon="📚", layout="wide")
inject_css()

profile = require_login()

render_hero(
    "📚 StudyBuddy — AI Exam Prep Dashboard",
    f"Welcome back, <strong>{profile['name']}</strong>! Your personal AI tutor for "
    "Maths, Science, Social Studies, English, Hindi, Kannada, ICT and more.",
    badge=f"🎓 Grade {profile['grade']} · Euro School Whitefield",
)

st.markdown("## 🚀 How it works")

c1, c2, c3, c4 = st.columns(4)
steps = [
    (c1, "1", "📤", "Upload", "Upload a chapter/exercise PDF. The AI reads it and learns the topics & style.",
     [("Upload Material", "pages/1_Upload_Material.py")]),
    (c2, "2", "🎓", "Learn", "AI tutor explains each topic with examples, tips, and answers doubts in chat.",
     [("Learn", "pages/2_Learn.py")]),
    (c3, "3", "📝", "Practice", "AI generates a fresh exam paper, balanced across question types. Take it in-browser.",
     [("Generate Test", "pages/3_Generate_Test.py"), ("Take Test", "pages/4_Take_Test.py")]),
    (c4, "4", "📊", "Analyze", "See topic-wise mastery, weak areas, score trends, and a predicted exam score.",
     [("Analytics", "pages/5_Analytics.py")]),
]

for col, num, icon, title, desc, links in steps:
    with col:
        st.markdown(
            f"""
            <div class="sb-card">
                <div class="sb-card-icon">{icon}</div>
                <h4><span class="sb-step-num">{num}</span>{title}</h4>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        for label, target in links:
            st.page_link(target, label=label, use_container_width=True)

st.write("")
st.divider()

grade = profile["grade"]
subjects = db.list_subjects()
subjects = [s for s in subjects if db.list_chapters(s["id"], grade=grade)]

if not subjects:
    st.info(
        f"👆 No chapters yet for **Grade {grade}**. Click **Upload Material** above to add the first chapter."
    )
else:
    st.markdown(f"## 📈 Subject Overview — Grade {grade}")
    cols = st.columns(len(subjects) if len(subjects) <= 4 else 4)
    for i, subj in enumerate(subjects):
        chapters = db.list_chapters(subj["id"], grade=grade)
        attempts = db.get_attempts_for_subject(subj["id"], grade=grade)
        avg = round(sum(a["percentage"] for a in attempts) / len(attempts), 1) if attempts else None
        with cols[i % 4]:
            st.metric(
                label=subj["name"],
                value=f"{avg}%" if avg is not None else "—",
                delta=f"{len(chapters)} chapter(s), {len(attempts)} test(s)",
                delta_color="off",
            )
            if avg is not None:
                st.progress(min(avg / 100, 1.0))

    st.write("")
    st.subheader("🗒️ Recent activity")
    rows = []
    for subj in subjects:
        for a in db.get_attempts_for_subject(subj["id"], grade=grade):
            rows.append(
                {
                    "Subject": subj["name"],
                    "Chapter": a["chapter_name"],
                    "Paper": a["title"],
                    "Score": f"{a['total_score']:.1f} / {a['max_score']:.1f}",
                    "Percentage": f"{a['percentage']}%",
                    "Date": a["created_at"],
                }
            )
    if rows:
        rows = sorted(rows, key=lambda r: r["Date"], reverse=True)[:10]
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.caption("No tests taken yet.")
