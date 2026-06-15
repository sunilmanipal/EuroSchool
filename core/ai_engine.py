"""All OpenAI calls: analyzing uploaded material, generating papers, grading answers."""
import json
import os

from openai import OpenAI

_client = None


def client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client


TEXT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")
VISION_MODEL = os.environ.get("OPENAI_VISION_MODEL", "gpt-4o")

CLASS_LEVEL = "Class 7 (CBSE/ICSE curriculum, Euro School Whitefield, Bengaluru)"

# Skill/cognitive-level categories used to compose a well-rounded paper.
# Values are DEFAULT relative weights (they need not sum to 100 — they are
# normalized at generation time).
SKILL_CATEGORIES = {
    "Knowledge": 20,
    "Understanding & Comprehension": 15,
    "Application Based": 20,
    "Critical Thinking": 20,
    "Higher Order Thinking Skills (HOTS)": 20,
    "Mental Ability / Reasoning": 10,
    "Case Study Based": 15,
    "Competency Based": 15,
    "Assertion-Reasoning / Source / Value Based": 10,
    "Creative & Open-Ended": 10,
}


def distribute_questions(num_questions, weights):
    """Turn category weights into integer question counts that sum to
    num_questions, biggest remainders first."""
    total_weight = sum(weights.values()) or 1
    raw = {cat: (w / total_weight) * num_questions for cat, w in weights.items()}
    counts = {cat: int(v) for cat, v in raw.items()}
    remainder = num_questions - sum(counts.values())
    # give the leftover slots to the categories with the largest fractional part
    order = sorted(raw.items(), key=lambda kv: kv[1] - int(kv[1]), reverse=True)
    for cat, _ in order[:remainder]:
        counts[cat] += 1
    # drop zero-count categories
    return {cat: c for cat, c in counts.items() if c > 0}


def _chat_json(model, messages, temperature=0.4):
    resp = client().chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)


def analyze_material(images_b64, subject, chapter_name):
    """Look at scanned textbook/exercise pages and summarize topics + style."""
    content = [
        {
            "type": "text",
            "text": (
                f"You are an expert {subject} curriculum analyst for {CLASS_LEVEL}. "
                f"The attached pages are from the chapter/topic '{chapter_name}'. "
                "Carefully read all text, including any maths notation, diagrams, tables "
                "and exercise questions.\n\n"
                "Return a JSON object with:\n"
                '- "topics": a list of specific sub-topics/concepts covered (e.g. '
                '"Addition of integers", "Properties of integers under multiplication")\n'
                '- "summary": a concise summary (150-250 words) of the concepts, formulas, '
                "and rules taught\n"
                '- "sample_question_styles": a list of 3-6 short descriptions of the exact '
                "style/format of exercise questions found (e.g. 'fill in the blanks with "
                "the correct sign', 'word problems involving profit and loss')\n"
                '- "difficulty": one of "easy", "medium", "hard" reflecting the overall '
                "level of this material for the class"
            ),
        }
    ]
    for img in images_b64:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{img}"},
            }
        )

    return _chat_json(
        VISION_MODEL,
        [
            {
                "role": "system",
                "content": "You are a meticulous teacher and curriculum analyst.",
            },
            {"role": "user", "content": content},
        ],
        temperature=0.2,
    )


QUESTION_SCHEMA_NOTE = """
Each question object must have exactly these fields:
- "topic": short sub-topic name (string)
- "type": one of "mcq", "numeric", "short", "long"
- "skill_category": one of the skill categories listed above (string, exact match)
- "question": the question text (string). For maths, write expressions in plain text
  (e.g. "(-7) + 12 - (-5)").
- "options": for "mcq" only, a list of exactly 4 strings (the choices, without A/B/C/D labels).
  Omit or use an empty list for other types.
- "correct_answer": the correct answer / model answer (string). For mcq, this must be one
  of the strings in "options" (exact match).
- "max_marks": integer marks for this question (1-5)
- "explanation": a short step-by-step solution or explanation a student can learn from
"""


def generate_paper(subject, chapter_name, summary, topics, sample_question_styles,
                    num_questions=10, difficulty="medium", skill_category_weights=None,
                    focus_topics=None):
    weights = skill_category_weights or SKILL_CATEGORIES
    category_counts = distribute_questions(num_questions, weights)
    distribution_text = "\n".join(f"- {cat}: {n} question(s)" for cat, n in category_counts.items())

    focus_text = ""
    if focus_topics:
        focus_text = (
            "\nThe student has struggled with these sub-topics in past tests: "
            f"{', '.join(focus_topics)}. Give these sub-topics noticeably MORE "
            "questions than the others (while still touching on the remaining "
            "sub-topics), so this paper gives the student extra practice where "
            "they need it most.\n"
        )

    prompt = (
        f"You are an experienced {subject} teacher setting a practice question paper for "
        f"{CLASS_LEVEL}, on the chapter/topic '{chapter_name}'.\n\n"
        f"Concepts and rules covered (from the student's textbook):\n{summary}\n\n"
        f"Sub-topics: {', '.join(topics)}\n\n"
        f"Typical exercise styles in the textbook: {', '.join(sample_question_styles)}\n\n"
        f"Create a NEW practice paper of exactly {num_questions} questions at '{difficulty}' "
        "overall difficulty, closely modeled on the textbook's style but with different "
        "numbers/wording so it is not a copy. Cover a good spread across the sub-topics "
        f"listed.\n{focus_text}\n"
        "For subjects like Maths, prefer a mix of 'mcq' (quick concept checks) and 'numeric' "
        "or 'short' (the student computes/writes the answer). For Science, Social Studies, "
        "Languages (Hindi/Kannada/English) and ICT, use a mix of 'mcq', 'short' (1-2 sentence "
        "answers) and 'long' (3-5 sentence / paragraph answers).\n\n"
        "The paper must be balanced across these question 'skill categories' (this is what "
        "makes a paper truly exam-ready — covering recall, understanding, application, "
        "reasoning, case-studies, competency and creative thinking). Use EXACTLY this "
        f"distribution of skill categories across the {num_questions} questions:\n"
        f"{distribution_text}\n\n"
        "Guidance per category:\n"
        "- Knowledge: direct recall of facts/definitions/formulas\n"
        "- Understanding & Comprehension: explain/interpret a concept or short passage\n"
        "- Application Based: apply a concept to a new/practical situation\n"
        "- Critical Thinking: analyze, compare, justify, evaluate\n"
        "- Higher Order Thinking Skills (HOTS): multi-step reasoning, non-routine problems\n"
        "- Mental Ability / Reasoning: logical/numerical reasoning, patterns, puzzles\n"
        "- Case Study Based: a short scenario/case followed by related questions\n"
        "- Competency Based: real-world, skill-application questions (as per NEP/CBSE competency framework)\n"
        "- Assertion-Reasoning / Source / Value Based: assertion+reason mcq, or a short "
        "source/quote/data extract with questions, or a values/ethics based question\n"
        "- Creative & Open-Ended: questions with no single fixed answer, encouraging the "
        "student's own ideas/expression (graded on reasoning quality, not exactness)\n\n"
        f"{QUESTION_SCHEMA_NOTE}\n"
        'Return JSON: {"title": "<paper title>", "questions": [ ... ]}'
    )

    data = _chat_json(
        TEXT_MODEL,
        [
            {"role": "system", "content": "You are an experienced school teacher and exam setter."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    for i, q in enumerate(data.get("questions", [])):
        q["q_index"] = i
        q.setdefault("options", [])
        q.setdefault("max_marks", 1)
        q.setdefault("skill_category", "")
    return data


def _fallback_grade_subjective_answer(question, student_answer):
    """Simple offline grader used when the AI grading call fails (e.g. no
    API quota). Does a normalized text/number match against the model
    answer so the app remains usable, with a note that full AI feedback
    is unavailable."""
    max_marks = question.get("max_marks", 1)
    given = (student_answer or "").strip()
    correct = (question.get("correct_answer") or "").strip()

    if not given:
        return {
            "awarded": 0,
            "feedback": (
                f"No answer written. The model answer was: {correct} "
                "(AI feedback is unavailable right now — offline check only)."
            ),
        }

    def normalize(text):
        return "".join(text.lower().split())

    if normalize(correct) and normalize(correct) in normalize(given):
        return {
            "awarded": max_marks,
            "feedback": (
                "Looks correct based on a basic offline check (your answer contains "
                f"the model answer '{correct}'). Detailed AI feedback on your method "
                "isn't available right now — check the explanation below to compare "
                "your steps."
            ),
        }

    return {
        "awarded": 0,
        "feedback": (
            f"Couldn't confirm a match with the model answer ('{correct}') using a "
            "basic offline check. AI grading (which checks your working/method and "
            "gives partial credit) is unavailable right now — please compare your "
            "answer with the explanation below, and re-grade this paper once AI "
            "grading is back online."
        ),
    }


def grade_subjective_answer(subject, question, student_answer):
    """Grade a non-mcq answer using the AI as a strict-but-fair teacher.

    Falls back to a basic offline check if the OpenAI call fails (e.g. the
    API key has no quota), so the app stays usable."""
    try:
        return _grade_subjective_answer_ai(subject, question, student_answer)
    except Exception:
        return _fallback_grade_subjective_answer(question, student_answer)


def _grade_subjective_answer_ai(subject, question, student_answer):
    prompt = (
        f"You are grading a {subject} answer written by a student in {CLASS_LEVEL}.\n\n"
        f"Question: {question['question']}\n"
        f"Model/reference answer: {question.get('correct_answer', '')}\n"
        f"Reference step-by-step solution (for checking the student's working/method): "
        f"{question.get('explanation', '')}\n"
        f"Maximum marks: {question.get('max_marks', 1)}\n\n"
        f"Student's answer: {student_answer if student_answer.strip() else '(left blank)'}\n\n"
        "The student may have shown their working step-by-step before the final answer — "
        "check the METHOD/STEPS against the reference solution, not just the final number. "
        "Grade fairly, giving partial credit for partially correct reasoning, correct method "
        "with a small arithmetic slip, or working shown even if the final answer differs "
        "slightly in form (e.g. equivalent fractions, different but valid wording). Be "
        "encouraging but honest.\n\n"
        'Return JSON: {"awarded": <number, can be fractional, 0 if blank>, '
        '"feedback": "<2-3 sentence constructive feedback, mention what was correct and how '
        'to improve>"}'
    )
    return _chat_json(
        TEXT_MODEL,
        [
            {"role": "system", "content": "You are a fair, encouraging school teacher grading student work."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )


def generate_lesson(subject, chapter_name, summary, topics):
    """Generate a structured 'lesson' that teaches the chapter topic-by-topic:
    plain-language explanation, worked examples, common mistakes/tips, and a
    few quick self-check questions (with answers) per topic."""
    prompt = (
        f"You are a patient, encouraging {subject} teacher for {CLASS_LEVEL}, preparing a "
        f"self-study lesson for the chapter/topic '{chapter_name}' so a student can learn it "
        "from scratch before attempting a test.\n\n"
        f"Concepts and rules covered (from the student's textbook):\n{summary}\n\n"
        f"Sub-topics: {', '.join(topics)}\n\n"
        "For EACH sub-topic, produce:\n"
        "- \"topic\": the sub-topic name (must match one of the sub-topics above)\n"
        "- \"explanation\": a clear, simple explanation of the concept (3-6 sentences, "
        "friendly tone, like explaining to a Class 7 student)\n"
        "- \"worked_examples\": a list of 2-3 fully worked example problems with "
        "step-by-step solutions (as strings)\n"
        "- \"common_mistakes\": a list of 2-3 common mistakes students make and how to avoid "
        "them\n"
        "- \"quick_check\": a list of 3 short self-check questions, each an object with "
        "\"question\", \"answer\" and \"hint\" fields, so the student can test themselves "
        "before the real test\n\n"
        'Return JSON: {"topics": [ {...}, ... ]}'
    )

    return _chat_json(
        TEXT_MODEL,
        [
            {"role": "system", "content": "You are a patient, encouraging school teacher who explains concepts simply and clearly."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
    )


def tutor_chat(subject, chapter_name, summary, history, question):
    """Answer a student's doubt about the chapter, in the context of a running
    chat. `history` is a list of {"role": "user"/"assistant", "content": str}."""
    system_prompt = (
        f"You are a friendly, patient AI tutor helping a {CLASS_LEVEL} student with the "
        f"{subject} chapter '{chapter_name}'. Here is a summary of what this chapter covers:\n"
        f"{summary}\n\n"
        "Answer the student's questions clearly and simply, with examples where helpful. "
        "If the question is unrelated to this chapter, gently answer it anyway but keep it "
        "age-appropriate and educational. Keep answers concise (a few short paragraphs, use "
        "bullet points or numbered steps for working through problems)."
    )
    messages = [{"role": "system", "content": system_prompt}] + history + [
        {"role": "user", "content": question}
    ]
    resp = client().chat.completions.create(
        model=TEXT_MODEL,
        messages=messages,
        temperature=0.5,
    )
    return resp.choices[0].message.content


def grade_mcq_answer(question, student_answer):
    correct = (question.get("correct_answer") or "").strip().lower()
    given = (student_answer or "").strip().lower()
    max_marks = question.get("max_marks", 1)
    if given and given == correct:
        return {"awarded": max_marks, "feedback": "Correct!"}
    if not given:
        return {"awarded": 0, "feedback": f"No answer selected. The correct answer was: {question.get('correct_answer')}"}
    return {"awarded": 0, "feedback": f"Not quite. The correct answer was: {question.get('correct_answer')}"}
