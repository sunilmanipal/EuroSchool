"""One-off seed script: loads the 'Chapter 1 - Integers' (Maths, Class 7)
content — analysis, lesson and a practice paper — hand-prepared from the
uploaded RS Aggarwal worksheet (DocScanner 14-Jun-2026 08-26 PM.pdf).

Use this when the OpenAI API is unavailable (e.g. quota exhausted) so the
app still has real content to demo the Learn / Generate Test / Take Test /
Analytics flow end-to-end. Run with:

    ./venv/bin/python scripts/seed_integers_chapter.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import db

SUBJECT = "Maths"
CHAPTER_NAME = "Chapter 1 - Integers"
SOURCE_FILE = "DocScanner 14-Jun-2026 08-26 PM.pdf"

TOPICS = [
    "Addition and Subtraction of Integers",
    "Properties of Addition and Subtraction of Integers",
    "Multiplication of Integers and its Properties",
    "Division of Integers and its Properties",
    "Simplification of Expressions (BODMAS) and Real-life Applications",
]

ANALYSIS = {
    "topics": TOPICS,
    "summary": (
        "This chapter covers the four basic operations on integers (positive and "
        "negative whole numbers, and zero) and the properties they follow. Students "
        "learn the sign rules for addition, subtraction, multiplication and division "
        "(e.g. same signs give a positive result for multiplication/division, "
        "different signs give a negative result). They study closure, commutative, "
        "associative, distributive, identity and inverse properties for addition and "
        "multiplication, and learn that integers are NOT closed under division and "
        "that division is neither commutative nor associative. The chapter also "
        "covers simplifying expressions with multiple operations using the correct "
        "order of operations (BODMAS), and applying integers to real-life situations "
        "such as temperature, money/profit-loss, sea level/depth, and floors of a "
        "building (basements as negative numbers)."
    ),
    "sample_question_styles": [
        "Direct computation: evaluate expressions like (-8) + 12 - (-5)",
        "State / verify a named property (closure, commutative, associative, "
        "distributive, identity, inverse) using given numbers",
        "True/False or 'is the student correct?' style questions that require "
        "justification with a counter-example",
        "Word problems using integers for temperature, money, depth/height, or floors",
        "Simplify multi-step expressions using BODMAS",
    ],
    "difficulty": "medium",
}

LESSON = {
    "topics": [
        {
            "topic": "Addition and Subtraction of Integers",
            "explanation": (
                "Integers are positive numbers, negative numbers, and zero. To add two "
                "integers with the SAME sign, add their values and keep that sign "
                "(e.g. (-7)+(-5)=-12). To add two integers with DIFFERENT signs, "
                "subtract the smaller value (ignore signs) from the larger, and give "
                "the answer the sign of the number with the bigger value. Subtracting "
                "an integer is the same as adding its opposite: a - b = a + (-b). So "
                "5 - (-3) becomes 5 + 3 = 8."
            ),
            "worked_examples": [
                "(-7) + (-5): same sign (both negative) → add 7+5=12, keep the negative sign → -12",
                "(-8) + 12 - (-5): First, (-8)+12 = 4 (different signs: 12-8=4, takes the sign of 12). "
                "Then 4 - (-5) = 4 + 5 = 9. Final answer: 9",
                "15 - 20: rewrite as 15 + (-20) = -5 (different signs: 20-15=5, takes the sign of -20)",
            ],
            "common_mistakes": [
                "Forgetting that subtracting a negative means adding the positive "
                "(writing 5 - (-3) = 2 instead of 5 + 3 = 8)",
                "When adding numbers with different signs, adding the values instead "
                "of subtracting them",
                "Losing track of the sign when there are several negative numbers in a row",
            ],
            "quick_check": [
                {"question": "Find: (-9) + 4", "answer": "-5", "hint": "Different signs — subtract the smaller value from the larger, and keep the sign of the bigger number"},
                {"question": "Find: 6 - (-11)", "answer": "17", "hint": "Subtracting a negative number is the same as adding the positive"},
                {"question": "Find: (-15) + (-8)", "answer": "-23", "hint": "Same sign — add the values and keep that sign"},
            ],
        },
        {
            "topic": "Properties of Addition and Subtraction of Integers",
            "explanation": (
                "Addition of integers follows these properties: Closure — adding any "
                "two integers always gives an integer. Commutative — a + b = b + a "
                "(order doesn't matter). Associative — (a+b)+c = a+(b+c) (grouping "
                "doesn't matter). Additive identity — a + 0 = a, so 0 is the additive "
                "identity. Additive inverse — every integer a has an opposite -a such "
                "that a + (-a) = 0. IMPORTANT: subtraction of integers is NOT "
                "commutative and NOT associative — changing the order or grouping "
                "changes the answer."
            ),
            "worked_examples": [
                "Commutative: (-4) + 9 = 5 and 9 + (-4) = 5 — same result either way",
                "Associative: [2 + (-5)] + 7 = -3+7 = 4 and 2 + [(-5)+7] = 2+2 = 4 — both equal 4",
                "Additive inverse: the additive inverse of -8 is 8, because (-8) + 8 = 0",
            ],
            "common_mistakes": [
                "Assuming subtraction is commutative, e.g. thinking 7-3 equals 3-7 (4 ≠ -4)",
                "Confusing 'additive inverse' (-a, which gives 0 when added) with "
                "'reciprocal' (1/a, which gives 1 when multiplied)",
                "Writing a + 0 = 0 instead of a (forgetting 0 is the IDENTITY, it "
                "doesn't change the number)",
            ],
            "quick_check": [
                {"question": "Is subtraction of integers commutative? Give an example to support your answer.", "answer": "No. For example, 8 - 3 = 5 but 3 - 8 = -5, which are different values.", "hint": "Try swapping the order of two different numbers in a subtraction and compare"},
                {"question": "Write the additive inverse of -17.", "answer": "17", "hint": "It's the number that gives 0 when added to -17"},
                {"question": "Verify the associative property of addition using -2, 6 and -9.", "answer": "[(-2)+6]+(-9) = 4+(-9) = -5, and (-2)+[6+(-9)] = (-2)+(-3) = -5. Both equal -5, so the property holds.", "hint": "Group the first two numbers together first, then group the last two, and compare the results"},
            ],
        },
        {
            "topic": "Multiplication of Integers and its Properties",
            "explanation": (
                "Sign rules for multiplication: (+)×(+)=+, (-)×(-)=+, and (+)×(-) or "
                "(-)×(+) = -. In short: SAME signs give a POSITIVE product, DIFFERENT "
                "signs give a NEGATIVE product. Properties: Closure — the product of "
                "two integers is always an integer. Commutative — a×b = b×a. "
                "Associative — (a×b)×c = a×(b×c). Distributive — a×(b+c) = a×b + a×c. "
                "Multiplicative identity — a×1 = a. Property of zero — a×0 = 0 for "
                "any integer a."
            ),
            "worked_examples": [
                "(-6) × 7 = -42 (different signs → negative)",
                "(-9) × (-5) = 45 (same signs → positive)",
                "Distributive property: (-4)×[5+(-3)] = (-4)×2 = -8, and "
                "(-4)×5 + (-4)×(-3) = -20+12 = -8 — both equal -8",
            ],
            "common_mistakes": [
                "Getting the sign rule backwards, e.g. thinking (-)×(-) gives a negative answer",
                "Forgetting the property of zero and over-complicating expressions like 25 × 0",
                "Mixing up the distributive property (a×(b+c)) with the associative property ((a×b)×c)",
            ],
            "quick_check": [
                {"question": "Find the product: (-12) × (-3)", "answer": "36", "hint": "Same signs (both negative) → positive product"},
                {"question": "Find the product: 15 × (-4)", "answer": "-60", "hint": "Different signs → negative product"},
                {"question": "Use the distributive property to find: 8 × (10 + (-2))", "answer": "8×10 + 8×(-2) = 80 + (-16) = 64", "hint": "Multiply 8 by each term inside the brackets separately, then add the results"},
            ],
        },
        {
            "topic": "Division of Integers and its Properties",
            "explanation": (
                "Division follows the same sign rules as multiplication: SAME signs "
                "give a POSITIVE quotient, DIFFERENT signs give a NEGATIVE quotient. "
                "BUT integers are NOT closed under division — dividing one integer by "
                "another doesn't always give an integer (e.g. 7÷2 = 3.5). Division is "
                "also NOT commutative (a÷b ≠ b÷a in general) and NOT associative. "
                "Dividing by 1 leaves a number unchanged (a÷1=a), dividing by -1 gives "
                "its opposite (a÷(-1)=-a), and division by 0 is NOT defined."
            ),
            "worked_examples": [
                "(-36) ÷ 9 = -4 (different signs → negative)",
                "(-45) ÷ (-5) = 9 (same signs → positive)",
                "Why integers aren't closed under division: 7 ÷ 2 = 3.5, which is not "
                "an integer — so the result of dividing two integers isn't always an integer",
            ],
            "common_mistakes": [
                "Assuming division of integers always gives an exact integer answer",
                "Believing a÷b = b÷a (division is NOT commutative)",
                "Writing a÷0 = 0 instead of recognising that division by 0 is undefined",
            ],
            "quick_check": [
                {"question": "Find: (-72) ÷ 8", "answer": "-9", "hint": "Different signs → negative quotient"},
                {"question": "Is 10 ÷ (-2) the same as (-2) ÷ 10? Explain.", "answer": "No. 10÷(-2) = -5, but (-2)÷10 = -0.2. They are different, so division of integers is not commutative.", "hint": "Calculate both and compare the results"},
                {"question": "Give one example to show that integers are not closed under division.", "answer": "For example, 5 ÷ 2 = 2.5, which is not an integer. So the set of integers is not closed under division.", "hint": "Find two integers whose division does not give a whole number"},
            ],
        },
        {
            "topic": "Simplification of Expressions (BODMAS) and Real-life Applications",
            "explanation": (
                "When an expression has more than one operation, follow the order of "
                "operations — BODMAS: Brackets, Of (powers), Division, Multiplication, "
                "Addition, Subtraction. Simplify inside brackets first, then do all "
                "division/multiplication (left to right), and finally all "
                "addition/subtraction (left to right). Integers are very useful for "
                "real-life situations involving two opposite directions: profit (+) "
                "and loss (-), above (+) and below (-) sea level, temperature rise (+) "
                "and fall (-), deposit (+) and withdrawal (-)."
            ),
            "worked_examples": [
                "7 - (-3)×2 + (-12)÷4: do × and ÷ first → (-3)×2=-6 and (-12)÷4=-3. "
                "Then 7-(-6)+(-3) = 7+6-3 = 10",
                "(-2) × [9 + (-4)] - 6: brackets first → 9+(-4)=5. Then (-2)×5=-10. "
                "Then -10-6 = -16",
                "A lift goes down 3 floors from floor 5, then up 7 floors: "
                "5 + (-3) + 7 = 9, so it ends at floor 9",
            ],
            "common_mistakes": [
                "Working strictly left-to-right and ignoring BODMAS order (e.g. doing "
                "addition before multiplication)",
                "Forgetting to simplify inside brackets first",
                "Sign errors when combining several results together at the end",
            ],
            "quick_check": [
                {"question": "Simplify: 10 + (-4) × 3", "answer": "-2", "hint": "Do the multiplication first: (-4)×3=-12, then 10+(-12)"},
                {"question": "Simplify: [(-18) ÷ 3] + (-2) × 5", "answer": "-16", "hint": "Do the division and multiplication first (-6 and -10), then add them"},
                {"question": "A submarine is at -120 m. It rises 45 m and then dives 30 m. What is its final position?", "answer": "-105 m (i.e. 105 m below sea level)", "hint": "Start at -120, add 45 for rising, then subtract 30 for diving"},
            ],
        },
    ]
}

PAPER_TITLE = "Integers — Practice Paper 1"

QUESTIONS = [
    {
        "type": "mcq",
        "topic": "Properties of Addition and Subtraction of Integers",
        "skill_category": "Knowledge",
        "question": "What is the additive identity for integers?",
        "options": ["0", "1", "-1", "It does not exist"],
        "correct_answer": "0",
        "max_marks": 1,
        "explanation": "Adding 0 to any integer does not change its value: a + 0 = a. So 0 is the additive identity.",
    },
    {
        "type": "mcq",
        "topic": "Properties of Addition and Subtraction of Integers",
        "skill_category": "Knowledge",
        "question": "Which equation correctly shows the commutative property of addition for integers a and b?",
        "options": ["a + b = b + a", "a + b = a - b", "a - b = b - a", "a x b = b + a"],
        "correct_answer": "a + b = b + a",
        "max_marks": 1,
        "explanation": "The commutative property states that changing the order of the numbers being added does not change the sum.",
    },
    {
        "type": "short",
        "topic": "Division of Integers and its Properties",
        "skill_category": "Understanding & Comprehension",
        "question": "Explain, with one example, why the set of integers is not closed under division.",
        "options": [],
        "correct_answer": "Integers are not closed under division because dividing one integer by another does not always give an integer. For example, 7 divided by 2 = 3.5, which is not an integer.",
        "max_marks": 2,
        "explanation": "Closure means an operation on two members of a set always produces a member of the same set. Since some integer divisions give fractions/decimals, integers are not closed under division.",
    },
    {
        "type": "numeric",
        "topic": "Addition and Subtraction of Integers",
        "skill_category": "Application Based",
        "question": "Evaluate, showing your steps: (-8) + 12 - (-5)",
        "options": [],
        "correct_answer": "9",
        "max_marks": 1,
        "explanation": "(-8)+12 = 4 (different signs, 12-8=4, sign of 12). Then 4-(-5) = 4+5 = 9.",
    },
    {
        "type": "numeric",
        "topic": "Simplification of Expressions (BODMAS) and Real-life Applications",
        "skill_category": "Application Based",
        "question": "Simplify using the correct order of operations (BODMAS), showing each step: 7 - (-3) x 2 + (-12) / 4",
        "options": [],
        "correct_answer": "10",
        "max_marks": 2,
        "explanation": "First do x and /: (-3)x2=-6, (-12)/4=-3. Then 7-(-6)+(-3) = 7+6-3 = 10.",
    },
    {
        "type": "mcq",
        "topic": "Multiplication of Integers and its Properties",
        "skill_category": "Critical Thinking",
        "question": "Which property of integers is illustrated by (-4) x [5 + (-3)] = (-4) x 5 + (-4) x (-3)?",
        "options": ["Distributive property", "Associative property", "Commutative property", "Closure property"],
        "correct_answer": "Distributive property",
        "max_marks": 1,
        "explanation": "The distributive property states a x (b+c) = a x b + a x c, which is exactly the pattern shown.",
    },
    {
        "type": "short",
        "topic": "Division of Integers and its Properties",
        "skill_category": "Critical Thinking",
        "question": "A student says: '(-15) / 3 = -5 and 3 / (-15) = -5, so division of integers is commutative.' Is the student correct? Show the correct calculations to justify your answer.",
        "options": [],
        "correct_answer": "No, the student is incorrect. (-15)/3 = -5, but 3/(-15) = -1/5 = -0.2, which is not equal to -5. Since the two results are different, division of integers is not commutative.",
        "max_marks": 2,
        "explanation": "The commutative property requires a/b = b/a for all values, which fails here, showing division is not commutative.",
    },
    {
        "type": "numeric",
        "topic": "Simplification of Expressions (BODMAS) and Real-life Applications",
        "skill_category": "Higher Order Thinking Skills (HOTS)",
        "question": "The temperature at the top of a hill was -8 degrees C at 6 a.m. It rose by 3 degrees C every hour for the next 5 hours. What was the temperature at 11 a.m.? Show your working.",
        "options": [],
        "correct_answer": "7 degrees C",
        "max_marks": 2,
        "explanation": "Rise over 5 hours = 5 x 3 = 15 degrees C. Final temperature = -8 + 15 = 7 degrees C.",
    },
    {
        "type": "long",
        "topic": "Addition and Subtraction of Integers",
        "skill_category": "Higher Order Thinking Skills (HOTS)",
        "question": "A submarine was at a depth of 450 m below sea level. It rose 180 m, and then dived another 250 m. Show each step of the calculation and state the submarine's final position relative to sea level (above or below, and by how much).",
        "options": [],
        "correct_answer": "Start: -450 m. After rising 180 m: -450+180 = -270 m. After diving 250 m more: -270-250 = -520 m. Final position: 520 m below sea level.",
        "max_marks": 3,
        "explanation": "Below sea level is represented as negative; rising is +180, diving is -250. Add step by step to get -520, i.e. 520 m below sea level.",
    },
    {
        "type": "mcq",
        "topic": "Properties of Addition and Subtraction of Integers",
        "skill_category": "Mental Ability / Reasoning",
        "question": "Find the missing number in the pattern: 8, 4, 0, -4, ___, -12",
        "options": ["-8", "8", "-6", "-2"],
        "correct_answer": "-8",
        "max_marks": 1,
        "explanation": "Each term decreases by 4: 8, 4, 0, -4, -8, -12.",
    },
    {
        "type": "long",
        "topic": "Multiplication of Integers and its Properties",
        "skill_category": "Case Study Based",
        "question": (
            "Case Study: Riya runs a small lemonade stall. Over 5 days, her daily "
            "profit/loss (in Rs) was: Monday: +120, Tuesday: -40, Wednesday: +90, "
            "Thursday: -150, Friday: +60.\n"
            "(a) Find Riya's total profit or loss for the week (5 days).\n"
            "(b) On the next 3 days (Sat, Sun, Mon) it rained, and she had the same "
            "loss as Tuesday each day (-40 per day). Find her new total including "
            "these 3 days.\n"
            "(c) Was she overall in profit or loss after these 8 days? Show all working."
        ),
        "options": [],
        "correct_answer": (
            "(a) Total for 5 days = 120+(-40)+90+(-150)+60 = 80. "
            "(b) 3 days of -40 = 3 x (-40) = -120. New total = 80+(-120) = -40. "
            "(c) Since the total is -40, she is overall in a loss of Rs 40 after 8 days."
        ),
        "max_marks": 4,
        "explanation": "Add all the signed values to find the running total; multiplication is used for repeated equal losses; the final sign of the total tells us profit (+) or loss (-).",
    },
    {
        "type": "short",
        "topic": "Addition and Subtraction of Integers",
        "skill_category": "Competency Based",
        "question": (
            "In a building, the ground floor is numbered 0, floors above ground are "
            "positive (1, 2, 3...) and basement floors below ground are negative "
            "(-1, -2, -3...). Raj starts at floor 2, takes a lift down 5 floors, then "
            "up 1 floor. Which floor does he end up on? Describe whether it is above "
            "or below ground."
        ),
        "options": [],
        "correct_answer": "2 + (-5) + 1 = -2. He ends up on basement floor 2 (B2), which is below ground level.",
        "max_marks": 2,
        "explanation": "Represent downward movement as negative and upward as positive, then add step by step.",
    },
    {
        "type": "mcq",
        "topic": "Multiplication of Integers and its Properties",
        "skill_category": "Assertion-Reasoning / Source / Value Based",
        "question": (
            "Assertion (A): The product of two negative integers is always positive. "
            "Reason (R): Multiplication of integers is distributive over addition. "
            "Choose the correct option:"
        ),
        "options": [
            "Both A and R are true, and R is the correct explanation of A.",
            "Both A and R are true, but R is NOT the correct explanation of A.",
            "A is true, but R is false.",
            "A is false, but R is true.",
        ],
        "correct_answer": "Both A and R are true, but R is NOT the correct explanation of A.",
        "max_marks": 1,
        "explanation": "A is true by the sign rule for multiplication ((-)x(-)=+). R is also a true property, but it is about how multiplication interacts with addition, not why two negatives multiply to a positive — so R does not explain A.",
    },
    {
        "type": "long",
        "topic": "Addition and Subtraction of Integers",
        "skill_category": "Creative & Open-Ended",
        "question": (
            "Create your own real-life word problem that uses addition and/or "
            "subtraction of integers, where at least one number involved is negative "
            "(for example, related to money, temperature, height, or sea level). "
            "Then solve your problem, showing your working."
        ),
        "options": [],
        "correct_answer": (
            "Open-ended — any well-formed real-life problem involving at least one "
            "negative integer, with a correct step-by-step solution matching the "
            "scenario described, should be awarded full marks. Look for: a clear "
            "scenario, correct use of positive/negative to represent opposite "
            "situations, and an accurate final calculation."
        ),
        "max_marks": 3,
        "explanation": "This checks whether the student can apply integer addition/subtraction creatively to a context of their choosing, and whether they can solve their own problem correctly.",
    },
]

for i, q in enumerate(QUESTIONS):
    q["q_index"] = i

if __name__ == "__main__":
    db.init_db()
    subject_id = db.get_or_create_subject(SUBJECT)
    chapter_id = db.add_chapter(subject_id, CHAPTER_NAME, json.dumps(ANALYSIS), SOURCE_FILE)
    db.save_lesson(chapter_id, json.dumps(LESSON))
    paper_id = db.save_paper(chapter_id, PAPER_TITLE, QUESTIONS)

    total_marks = sum(q["max_marks"] for q in QUESTIONS)
    print(f"Subject id: {subject_id}")
    print(f"Chapter id: {chapter_id} — '{CHAPTER_NAME}'")
    print(f"Lesson saved with {len(LESSON['topics'])} topics")
    print(f"Paper id: {paper_id} — '{PAPER_TITLE}' ({len(QUESTIONS)} questions, {total_marks} marks)")
