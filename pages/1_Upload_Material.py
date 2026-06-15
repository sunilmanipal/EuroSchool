import json
import re

import streamlit as st
from dotenv import load_dotenv

from core import ai_engine, db, pdf_utils
from core.auth import GRADES
from core.auth_ui import require_login
from core.ui import render_page_header

load_dotenv()
db.init_db()

st.set_page_config(page_title="Upload Material", page_icon="📤", layout="wide")
profile = require_login()
render_page_header(
    "📤 Upload Study Material",
    "Step 1 of the workflow: upload a chapter from a textbook, worksheet or notes. "
    "The AI will read it and figure out the topics and question style — then you can "
    "go to <strong>Learn</strong> or <strong>Generate Test</strong>.",
)

DEFAULT_SUBJECTS = [
    "Maths", "Science", "Social Studies", "English", "Hindi", "Kannada", "ICT",
]

st.markdown("### 1️⃣ What is this material?")
col1, col2, col3 = st.columns(3)
with col1:
    subject_choice = st.selectbox("Subject", DEFAULT_SUBJECTS + ["Other (type below)"])
    if subject_choice == "Other (type below)":
        subject_name = st.text_input("Enter subject name")
    else:
        subject_name = subject_choice

with col2:
    chapter_name = st.text_input(
        "Chapter / Topic name",
        placeholder="e.g. Chapter 1 - Integers",
        help="Give this material a short name. This is REQUIRED before you can analyze it.",
    )

with col3:
    grade = st.selectbox(
        "Grade / Standard",
        GRADES,
        index=GRADES.index(profile["grade"]),
        help="Which grade is this material for?",
    )

st.markdown("### 2️⃣ Upload the PDF")
uploaded = st.file_uploader("Upload a PDF (chapter pages, exercise sheet, notes, etc.)", type=["pdf"])

if uploaded:
    # Suggest a chapter name from the filename if the user hasn't typed one yet
    if not chapter_name:
        suggestion = re.sub(r"[_\-]+", " ", uploaded.name.rsplit(".", 1)[0]).strip()
        st.info(
            f"💡 You haven't entered a Chapter / Topic name yet (required). "
            f"For example, you could use: **\"{suggestion}\"** — type it in the box above."
        )

    file_bytes = uploaded.read()
    total_pages = pdf_utils.pdf_page_count(file_bytes)
    st.caption(f"✅ File uploaded — this PDF has {total_pages} page(s).")

    st.markdown("### 3️⃣ Choose pages & analyze")
    max_analyze = min(total_pages, 20)
    if total_pages > 1:
        page_range = st.slider(
            "Pages to analyze (for large books, pick just the relevant chapter pages — "
            "max 20 pages at a time)",
            min_value=1, max_value=total_pages,
            value=(1, max_analyze),
        )
    else:
        page_range = (1, 1)

    ready = bool(subject_name and chapter_name)
    if not ready:
        st.warning("⬆️ Please fill in **Subject** and **Chapter / Topic name** above to continue.")

    if st.button("🔍 Analyze Material", type="primary", disabled=not ready, use_container_width=True):
        with st.spinner("AI is reading the material and identifying topics... this can take a minute."):
            doc_bytes = file_bytes
            start, end = page_range
            # Render only the selected page range
            import fitz
            doc = fitz.open(stream=doc_bytes, filetype="pdf")
            sub = fitz.open()
            for p in range(start - 1, end):
                sub.insert_pdf(doc, from_page=p, to_page=p)
            sub_bytes = sub.tobytes()
            sub.close()
            doc.close()

            images = pdf_utils.pdf_to_images_b64(sub_bytes, dpi=150, max_pages=20)
            analysis = ai_engine.analyze_material(images, subject_name, chapter_name)

        st.success("✅ Done! Here's what the AI found:")
        st.write(f"**Difficulty:** {analysis.get('difficulty', 'n/a')}")
        st.write("**Topics covered:**")
        st.write(", ".join(analysis.get("topics", [])))
        st.write("**Summary:**")
        st.write(analysis.get("summary", ""))
        st.write("**Question styles seen in textbook:**")
        for s in analysis.get("sample_question_styles", []):
            st.write(f"- {s}")

        subject_id = db.get_or_create_subject(subject_name)
        chapter_id = db.add_chapter(
            subject_id, chapter_name, json.dumps(analysis), uploaded.name, grade=grade
        )
        st.session_state["last_chapter_id"] = chapter_id

        st.markdown("### 🎉 What's next?")
        next_col1, next_col2 = st.columns(2)
        with next_col1:
            st.page_link("pages/2_Learn.py", label="🎓 Go to Learn — read the lesson for this chapter", use_container_width=True)
        with next_col2:
            st.page_link("pages/3_Generate_Test.py", label="📝 Go to Generate Test — create a practice paper", use_container_width=True)

st.divider()
st.subheader(f"📚 Previously uploaded chapters — Grade {profile['grade']}")
subjects = db.list_subjects()
any_chapters = False
for subj in subjects:
    chapters = db.list_chapters(subj["id"], grade=profile["grade"])
    if chapters:
        any_chapters = True
        st.markdown(f"**{subj['name']}**")
        for c in chapters:
            st.write(f"- {c['name']} (uploaded {c['created_at']}, file: {c['source_file']})")

if not any_chapters:
    st.caption(f"Nothing uploaded yet for Grade {profile['grade']} — use the form above to add your first chapter.")
