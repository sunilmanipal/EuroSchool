import streamlit as st
from dotenv import load_dotenv

from core import db

load_dotenv()
db.init_db()

st.set_page_config(page_title="StudyBuddy — Exam Prep Dashboard", page_icon="📚", layout="wide")

st.title("📚 StudyBuddy — AI Exam Prep Dashboard")
st.caption("Class 7 · Euro School Whitefield")

st.markdown(
    "Welcome! This dashboard helps your son prepare for exams across **any subject** — "
    "Maths, Science, Social Studies, English, Hindi, Kannada, ICT and more."
)

st.divider()
st.markdown("## 🚀 How it works")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("### 1️⃣ 📤 Upload")
    st.write("Upload a chapter/exercise PDF. The AI reads it and learns the topics & style.")
    st.page_link("pages/1_Upload_Material.py", label="Upload Material", use_container_width=True)
with c2:
    st.markdown("### 2️⃣ 🎓 Learn")
    st.write("AI tutor explains each topic with examples, tips, and answers doubts in chat.")
    st.page_link("pages/2_Learn.py", label="Learn", use_container_width=True)
with c3:
    st.markdown("### 3️⃣ 📝✍️ Practice")
    st.write("AI generates a fresh exam paper, balanced across question types. Take it in-browser.")
    st.page_link("pages/3_Generate_Test.py", label="Generate Test", use_container_width=True)
    st.page_link("pages/4_Take_Test.py", label="Take Test", use_container_width=True)
with c4:
    st.markdown("### 4️⃣ 📊 Analyze")
    st.write("See topic-wise mastery, weak areas, score trends, and a predicted exam score.")
    st.page_link("pages/5_Analytics.py", label="Analytics", use_container_width=True)

st.divider()

subjects = db.list_subjects()

if not subjects:
    st.info("👆 No subjects yet. Click **Upload Material** above to add your first chapter.")
else:
    st.markdown("## 📈 Subject Overview")
    cols = st.columns(len(subjects) if len(subjects) <= 4 else 4)
    for i, subj in enumerate(subjects):
        chapters = db.list_chapters(subj["id"])
        attempts = db.get_attempts_for_subject(subj["id"])
        avg = round(sum(a["percentage"] for a in attempts) / len(attempts), 1) if attempts else None
        with cols[i % 4]:
            st.metric(
                label=subj["name"],
                value=f"{avg}%" if avg is not None else "—",
                delta=f"{len(chapters)} chapter(s), {len(attempts)} test(s)",
                delta_color="off",
            )

    st.divider()
    st.subheader("🗒️ Recent activity")
    rows = []
    for subj in subjects:
        for a in db.get_attempts_for_subject(subj["id"]):
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
