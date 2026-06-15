import json

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

from core import ai_engine, db
from core.auth_ui import require_login

load_dotenv()
db.init_db()

st.set_page_config(page_title="Learn", page_icon="🎓", layout="wide")
profile = require_login()
st.title("🎓 Learn This Chapter")
st.caption(
    "Read through the lesson for each sub-topic before attempting a test — "
    "explanations, worked examples, common mistakes, and quick self-checks."
)


def speak_button(text, key, label="🔊 Read this aloud"):
    """Render a small button that uses the browser's built-in text-to-speech
    (Web Speech API) to read `text` out loud, step by step."""
    safe_text = json.dumps(text)
    safe_key = "".join(c if c.isalnum() else "_" for c in key)
    components.html(
        f"""
        <button id="speak_{safe_key}" style="padding:6px 14px;border-radius:6px;
        border:1px solid #ccc;background:#eef0fb;cursor:pointer;font-size:13px;">
        {label}</button>
        <script>
        document.getElementById("speak_{safe_key}").onclick = function() {{
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance({safe_text});
            u.rate = 0.85;
            window.speechSynthesis.speak(u);
        }};
        </script>
        """,
        height=42,
    )

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

chapter_labels = [f"{c['name']} (uploaded {c['created_at'][:10]})" for c in chapters]
chap_idx = st.selectbox("Chapter / Topic", range(len(chapters)), format_func=lambda i: chapter_labels[i])
chapter = chapters[chap_idx]
analysis = json.loads(chapter["summary"])

with st.expander("What the AI knows about this chapter"):
    st.write(f"**Difficulty:** {analysis.get('difficulty')}")
    st.write("**Topics:** " + ", ".join(analysis.get("topics", [])))
    st.write(analysis.get("summary", ""))

st.divider()

lesson = json.loads(chapter["lesson_json"]) if chapter.get("lesson_json") else None

col1, col2 = st.columns([1, 3])
with col1:
    button_label = "🔁 Regenerate Lesson" if lesson else "📖 Generate Lesson"
    if st.button(button_label, type="primary"):
        with st.spinner("AI tutor is preparing your lesson... this can take a minute."):
            lesson = ai_engine.generate_lesson(
                subject=subj_choice,
                chapter_name=chapter["name"],
                summary=analysis.get("summary", ""),
                topics=analysis.get("topics", []),
            )
            db.save_lesson(chapter["id"], json.dumps(lesson))
        st.success("Lesson ready!")

if not lesson:
    st.info("Click **Generate Lesson** to have the AI tutor explain this chapter, topic by topic.")
    st.stop()

# ---------------------------------------------------------------------------
# Work out which topics need extra focus, based on past test attempts
# ---------------------------------------------------------------------------
topic_performance = db.get_topic_performance(subject_id, grade=grade)
topic_mastery = {}
if topic_performance:
    totals = {}
    for r in topic_performance:
        t = r["topic"]
        totals.setdefault(t, [0, 0])
        totals[t][0] += r["awarded"]
        totals[t][1] += r["max_marks"]
    topic_mastery = {t: round(100 * aw / mx, 1) for t, (aw, mx) in totals.items() if mx}

weak_topics = [t for t, m in topic_mastery.items() if m < 60]
if weak_topics:
    st.warning(
        "**📌 Based on past tests, focus extra time on:** " + ", ".join(weak_topics) + ". "
        "These topics are marked below with extra help, already expanded for you. "
        "Once you've reviewed them, head to **📝 Generate Test** and pick these topics "
        "under 'Focus topics' for extra practice."
    )

for t in lesson.get("topics", []):
    topic_name = t.get("topic", "")
    is_weak = topic_name in weak_topics
    mastery = topic_mastery.get(topic_name)

    header = f"📌 {topic_name}"
    if mastery is not None:
        header += f"  ·  mastery: {mastery}%"
    if is_weak:
        header += "  ·  🔶 needs more practice"
    st.subheader(header)
    st.write(t.get("explanation", ""))
    speak_button(t.get("explanation", ""), key=f"explain_{chapter['id']}_{topic_name}")

    examples = t.get("worked_examples", [])
    if examples:
        st.markdown("**Worked examples:**")
        for ex in examples:
            st.markdown(f"> {ex}")

    mistakes = t.get("common_mistakes", [])
    if mistakes:
        st.markdown("**⚠️ Common mistakes to avoid:**")
        for m in mistakes:
            st.write(f"- {m}")

    quick_check = t.get("quick_check", [])
    if quick_check:
        st.markdown("**✏️ Quick check yourself:**")
        st.caption(
            "Pick an answer and click Check. If you're wrong, you'll get a hint "
            "first (not the answer) so you can try again — after a second try, "
            "we'll walk you through the full solution step by step (and you can "
            "have it read aloud)."
        )
        for j, qc in enumerate(quick_check):
            qkey = f"qc_{chapter['id']}_{topic_name}_{j}"
            attempts_key = f"{qkey}_attempts"
            solved_key = f"{qkey}_solved"
            st.session_state.setdefault(attempts_key, 0)
            st.session_state.setdefault(solved_key, False)

            with st.container(border=True):
                st.write(f"**{j+1}. {qc.get('question', '')}**")
                options = qc.get("options") or []
                choice = st.radio(
                    "Choose your answer:", options, index=None,
                    key=f"{qkey}_choice", horizontal=len(options) <= 2,
                )

                if st.button("✅ Check answer", key=f"{qkey}_btn"):
                    correct = str(qc.get("answer", "")).strip().lower()
                    given = str(choice).strip().lower() if choice is not None else ""
                    if given and given == correct:
                        st.session_state[solved_key] = True
                    else:
                        st.session_state[solved_key] = False
                        st.session_state[attempts_key] += 1

                if st.session_state[solved_key]:
                    st.success("✅ Correct! Great job.")
                    with st.expander("See the full step-by-step explanation"):
                        st.write(qc.get("explanation", ""))
                        speak_button(qc.get("explanation", ""), key=f"{qkey}_exp_done")
                elif st.session_state[attempts_key] == 1:
                    st.warning(f"🤔 Not quite — here's a hint: {qc.get('hint', '')}")
                    speak_button(f"Hint: {qc.get('hint', '')}", key=f"{qkey}_hint")
                elif st.session_state[attempts_key] >= 2:
                    st.error("Let's work through it together, step by step:")
                    st.write(qc.get("explanation", ""))
                    st.caption(f"Correct answer: {qc.get('answer', '')}")
                    speak_button(qc.get("explanation", ""), key=f"{qkey}_exp_full")

    deep_dive = t.get("deep_dive")
    if deep_dive:
        with st.expander("🔎 Still confused? Extra help & examples", expanded=is_weak):
            st.write(deep_dive.get("explanation", ""))
            for ex in deep_dive.get("extra_examples", []):
                st.markdown(f"> {ex}")

    st.divider()

# ---------------------------------------------------------------------------
# Ask the AI tutor a doubt
# ---------------------------------------------------------------------------
st.subheader("💬 Ask the AI Tutor a Doubt")
st.caption(f"Ask anything about '{chapter['name']}' — the tutor will explain it simply.")

chat_key = f"tutor_chat_{chapter['id']}"
if chat_key not in st.session_state:
    st.session_state[chat_key] = []

for msg in st.session_state[chat_key]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Type your question here...")
if question:
    st.session_state[chat_key].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ai_engine.tutor_chat(
                subject=subj_choice,
                chapter_name=chapter["name"],
                summary=analysis.get("summary", ""),
                history=st.session_state[chat_key][:-1],
                question=question,
            )
            st.write(answer)
    st.session_state[chat_key].append({"role": "assistant", "content": answer})
