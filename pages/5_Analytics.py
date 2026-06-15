import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

from core import db
from core.auth_ui import require_login
from core.ui import render_page_header

load_dotenv()
db.init_db()

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")
profile = require_login()
render_page_header("📊 Performance Analytics", "Track topic-wise mastery, score trends, and predicted exam scores.")

grade = profile["grade"]
subjects = db.list_subjects()
subjects = [s for s in subjects if db.list_chapters(s["id"], grade=grade)]
if not subjects:
    st.warning(f"No chapters yet for Grade {grade}. Upload material first on the **📤 Upload Material** page.")
    st.stop()

subject_names = [s["name"] for s in subjects]
subj_choice = st.selectbox("Subject", subject_names)
subject_id = next(s["id"] for s in subjects if s["name"] == subj_choice)

attempts = db.get_attempts_for_subject(subject_id, grade=grade)
topic_rows = db.get_topic_performance(subject_id, grade=grade)
skill_rows = db.get_skill_category_performance(subject_id, grade=grade)

if not attempts:
    st.info("No tests taken yet for this subject. Take a test first.")
    st.stop()

# ---------------------------------------------------------------- overview
df_attempts = pd.DataFrame(attempts)
overall_avg = df_attempts["percentage"].mean()
recent_avg = df_attempts.tail(3)["percentage"].mean()

c1, c2, c3 = st.columns(3)
c1.metric("Tests taken", len(attempts))
c2.metric("Overall average", f"{overall_avg:.1f}%")
c3.metric("Predicted next score", f"{recent_avg:.1f}%", help="Based on the average of the last 3 attempts")

# ---------------------------------------------------------------- trend
st.subheader("Score trend over time")
df_trend = df_attempts.copy()
df_trend["attempt"] = range(1, len(df_trend) + 1)
fig_trend = px.line(
    df_trend, x="attempt", y="percentage", markers=True,
    labels={"attempt": "Attempt #", "percentage": "Score (%)"},
    hover_data=["chapter_name", "title", "created_at"],
)
fig_trend.update_yaxes(range=[0, 100])
st.plotly_chart(fig_trend, use_container_width=True)

# ---------------------------------------------------------------- topic mastery
st.subheader("Topic-wise mastery")
if topic_rows:
    df_topics = pd.DataFrame(topic_rows)
    grouped = df_topics.groupby("topic").agg(
        awarded=("awarded", "sum"), max_marks=("max_marks", "sum")
    ).reset_index()
    grouped["mastery"] = (100 * grouped["awarded"] / grouped["max_marks"]).round(1)
    grouped = grouped.sort_values("mastery")

    fig_bar = px.bar(
        grouped, x="mastery", y="topic", orientation="h",
        labels={"mastery": "Mastery (%)", "topic": "Topic"},
        color="mastery", color_continuous_scale="RdYlGn", range_color=[0, 100],
    )
    fig_bar.update_xaxes(range=[0, 100])
    st.plotly_chart(fig_bar, use_container_width=True)

    weak = grouped[grouped["mastery"] < 60]
    if not weak.empty:
        st.warning(
            "**Weak topics to focus on:** " + ", ".join(weak["topic"].tolist())
        )
    strong = grouped[grouped["mastery"] >= 85]
    if not strong.empty:
        st.success("**Strong topics:** " + ", ".join(strong["topic"].tolist()))
else:
    st.caption("No topic-level data yet.")

# ---------------------------------------------------------------- skill category mastery
st.subheader("Performance by question type (skill category)")
st.caption(
    "How your son performs across different kinds of thinking — knowledge recall, "
    "application, critical thinking, HOTS, case studies, etc."
)
if skill_rows:
    df_skills = pd.DataFrame(skill_rows)
    grouped_skills = df_skills.groupby("skill_category").agg(
        awarded=("awarded", "sum"), max_marks=("max_marks", "sum")
    ).reset_index()
    grouped_skills["mastery"] = (100 * grouped_skills["awarded"] / grouped_skills["max_marks"]).round(1)
    grouped_skills = grouped_skills.sort_values("mastery")

    fig_skills = px.bar(
        grouped_skills, x="mastery", y="skill_category", orientation="h",
        labels={"mastery": "Mastery (%)", "skill_category": "Skill category"},
        color="mastery", color_continuous_scale="RdYlGn", range_color=[0, 100],
    )
    fig_skills.update_xaxes(range=[0, 100])
    st.plotly_chart(fig_skills, use_container_width=True)

    weak_skills = grouped_skills[grouped_skills["mastery"] < 60]
    if not weak_skills.empty:
        st.warning(
            "**Skill areas to build up:** " + ", ".join(weak_skills["skill_category"].tolist())
        )
else:
    st.caption("No skill-category data yet.")

# ---------------------------------------------------------------- history table
st.subheader("Test history")
hist = df_attempts[["created_at", "chapter_name", "title", "total_score", "max_score", "percentage"]]
hist = hist.rename(columns={
    "created_at": "Date", "chapter_name": "Chapter", "title": "Paper",
    "total_score": "Score", "max_score": "Max", "percentage": "Percentage",
})
st.dataframe(hist.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)
