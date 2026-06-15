"""One-off update: turns the 'Quick check yourself' items in the Integers
lesson into interactive multiple-choice questions with step-by-step
explanations (used by pages/2_Learn.py for the new interactive quiz UI with
hints-on-wrong-answer and voice read-aloud).

Run with:
    ./venv/bin/python scripts/update_integers_quickcheck.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import db

SUBJECT = "Maths"
CHAPTER_NAME = "Chapter 1 - Integers"

# Keyed by topic name -> list of 4 quick-check items, each with
# question, options (4 choices), answer, hint, and a step-by-step explanation.
QUICK_CHECKS = {
    "Addition and Subtraction of Integers": [
        {
            "question": "Find: (-9) + 4",
            "options": ["-5", "5", "-13", "13"],
            "answer": "-5",
            "hint": "Different signs — subtract the smaller value from the larger, and keep the sign of the number with the bigger value (9)",
            "explanation": (
                "Step 1: The numbers have different signs (one negative, one positive). "
                "Step 2: Subtract the smaller value from the larger: 9 - 4 = 5. "
                "Step 3: Give the answer the sign of the number with the bigger value — "
                "since 9 is bigger and it is negative, the answer is negative. "
                "Final answer: -5."
            ),
        },
        {
            "question": "Find: 6 - (-11)",
            "options": ["17", "-5", "5", "-17"],
            "answer": "17",
            "hint": "Subtracting a negative number is the same as adding the positive — turn it into 6 + 11",
            "explanation": (
                "Step 1: Subtracting a negative number is the same as adding a positive "
                "number, so rewrite 6 - (-11) as 6 + 11. "
                "Step 2: Add 6 + 11 = 17. Final answer: 17."
            ),
        },
        {
            "question": "Find: (-15) + (-8)",
            "options": ["-23", "23", "-7", "7"],
            "answer": "-23",
            "hint": "Same sign (both negative) — add the values and keep the negative sign",
            "explanation": (
                "Step 1: Both numbers have the same sign (both negative). "
                "Step 2: Add their values: 15 + 8 = 23. "
                "Step 3: Keep the negative sign. Final answer: -23."
            ),
        },
        {
            "question": "Find: (-20) - 7",
            "options": ["-27", "-13", "13", "27"],
            "answer": "-27",
            "hint": "Rewrite as (-20) + (-7) — same sign, so add and keep the negative",
            "explanation": (
                "Step 1: Rewrite the subtraction as adding the opposite: (-20) - 7 "
                "becomes (-20) + (-7). "
                "Step 2: Both numbers are negative (same sign), so add 20 + 7 = 27. "
                "Step 3: Keep the negative sign. Final answer: -27."
            ),
        },
    ],
    "Properties of Addition and Subtraction of Integers": [
        {
            "question": "Which statement about subtraction of integers is TRUE?",
            "options": [
                "Subtraction is commutative, so a - b = b - a",
                "Subtraction is NOT commutative — a - b is usually not equal to b - a",
                "Subtraction always gives zero",
                "Subtraction is the same as multiplication",
            ],
            "answer": "Subtraction is NOT commutative — a - b is usually not equal to b - a",
            "hint": "Try a real example: pick two numbers, subtract them one way, then the other way, and compare.",
            "explanation": (
                "Step 1: Pick two numbers, say 8 and 3. "
                "Step 2: Calculate 8 - 3 = 5. "
                "Step 3: Now calculate 3 - 8 = -5. "
                "Step 4: Compare: 5 is not equal to -5, so swapping the order CHANGES "
                "the answer. This proves subtraction of integers is NOT commutative."
            ),
        },
        {
            "question": "What is the additive inverse of -17?",
            "options": ["17", "-17", "0", "1"],
            "answer": "17",
            "hint": "The additive inverse is the number that, when ADDED to -17, gives 0.",
            "explanation": (
                "Step 1: We need a number that, when added to -17, equals 0. "
                "Step 2: -17 + 17 = 0. "
                "Step 3: So the additive inverse of -17 is 17."
            ),
        },
        {
            "question": "What is [(-2) + 6] + (-9)?",
            "options": ["-5", "5", "-17", "17"],
            "answer": "-5",
            "hint": "Work inside the brackets first: (-2)+6, then add the last number.",
            "explanation": (
                "Step 1: Work out the brackets first: (-2) + 6 = 4. "
                "Step 2: Now add the last number: 4 + (-9) = -5. "
                "(If you instead grouped it as (-2) + [6 + (-9)], you'd get "
                "(-2) + (-3) = -5 too — same answer either way, showing the "
                "associative property.)"
            ),
        },
        {
            "question": "True or False: (-5) + 0 = -5",
            "options": ["True", "False"],
            "answer": "True",
            "hint": "What does adding 0 do to any number?",
            "explanation": (
                "Step 1: Adding 0 to any integer never changes its value — this is "
                "called the additive identity property. "
                "Step 2: So (-5) + 0 = -5. The statement is TRUE."
            ),
        },
    ],
    "Multiplication of Integers and its Properties": [
        {
            "question": "Find the product: (-12) x (-3)",
            "options": ["36", "-36", "15", "-15"],
            "answer": "36",
            "hint": "Same signs (both negative) — what sign will the answer have?",
            "explanation": (
                "Step 1: Both numbers are negative — same signs — so the product will "
                "be POSITIVE. Step 2: Multiply the values: 12 x 3 = 36. "
                "Final answer: 36."
            ),
        },
        {
            "question": "Find the product: 15 x (-4)",
            "options": ["-60", "60", "-11", "11"],
            "answer": "-60",
            "hint": "Different signs — what sign will the answer have?",
            "explanation": (
                "Step 1: One number is positive and one is negative — different signs "
                "— so the product will be NEGATIVE. Step 2: Multiply the values: "
                "15 x 4 = 60. Final answer: -60."
            ),
        },
        {
            "question": "Use the distributive property to find: 8 x (10 + (-2))",
            "options": ["64", "80", "-64", "16"],
            "answer": "64",
            "hint": "Multiply 8 by each term inside the brackets separately, then add the results.",
            "explanation": (
                "Step 1: Distribute: 8 x (10 + (-2)) = (8 x 10) + (8 x (-2)). "
                "Step 2: Calculate each part: 8 x 10 = 80, and 8 x (-2) = -16. "
                "Step 3: Add them: 80 + (-16) = 64. Final answer: 64."
            ),
        },
        {
            "question": "Find: (-1) x (-1) x (-1) x (-1) x (-5)",
            "options": ["-5", "5", "-1", "1"],
            "answer": "-5",
            "hint": "Count ALL the negative signs in the whole expression — is the count odd or even?",
            "explanation": (
                "Step 1: Count the negative numbers: there are five negative numbers "
                "in total. Step 2: Five is an ODD number, so the final answer will be "
                "NEGATIVE. Step 3: Multiply the values (ignoring signs): "
                "1x1x1x1x5 = 5. Step 4: Apply the negative sign. Final answer: -5."
            ),
        },
    ],
    "Division of Integers and its Properties": [
        {
            "question": "Find: (-72) / 8",
            "options": ["-9", "9", "-8", "8"],
            "answer": "-9",
            "hint": "Different signs — what sign will the answer have?",
            "explanation": (
                "Step 1: One number is negative and one is positive — different signs "
                "— so the quotient will be NEGATIVE. Step 2: Divide the values: "
                "72 / 8 = 9. Final answer: -9."
            ),
        },
        {
            "question": "What is 10 / (-2)?",
            "options": ["-5", "5", "-0.2", "0.2"],
            "answer": "-5",
            "hint": "Different signs — what sign will the answer have? Then divide the values.",
            "explanation": (
                "Step 1: Different signs, so the quotient is NEGATIVE. Step 2: "
                "10 / 2 = 5. Final answer: -5. (Note: if you flip the order to "
                "(-2)/10, you'd get -0.2 — a totally different answer! This shows "
                "division is NOT commutative.)"
            ),
        },
        {
            "question": "Which of these divisions does NOT give a whole number (integer)?",
            "options": ["8 / 2", "9 / 3", "5 / 2", "12 / 4"],
            "answer": "5 / 2",
            "hint": "Try dividing each pair — which one leaves a remainder / gives a decimal?",
            "explanation": (
                "Step 1: Check each option: 8/2=4 (integer), 9/3=3 (integer), "
                "5/2=2.5 (NOT an integer), 12/4=3 (integer). Step 2: Only 5/2 gives a "
                "decimal answer. This shows that dividing two integers does not "
                "always give an integer — integers are NOT closed under division."
            ),
        },
        {
            "question": "What is (-15) / (-1)?",
            "options": ["15", "-15", "1", "-1"],
            "answer": "15",
            "hint": "Same signs — what sign will the answer have? Then think about what dividing by -1 does.",
            "explanation": (
                "Step 1: Both numbers are negative — same signs — so the quotient is "
                "POSITIVE. Step 2: 15 / 1 = 15. Final answer: 15. (Dividing by -1 "
                "always flips the sign of a number.)"
            ),
        },
    ],
    "Simplification of Expressions (BODMAS) and Real-life Applications": [
        {
            "question": "Simplify: 10 + (-4) x 3",
            "options": ["-2", "18", "-22", "2"],
            "answer": "-2",
            "hint": "BODMAS says multiplication comes before addition — do (-4) x 3 first.",
            "explanation": (
                "Step 1: According to BODMAS, do multiplication before addition: "
                "(-4) x 3 = -12. Step 2: Now add: 10 + (-12) = -2. Final answer: -2."
            ),
        },
        {
            "question": "Simplify: [(-18) / 3] + (-2) x 5",
            "options": ["-16", "-4", "16", "4"],
            "answer": "-16",
            "hint": "Do the division and multiplication first (left to right), then add the results.",
            "explanation": (
                "Step 1: Do division and multiplication first: (-18)/3 = -6, and "
                "(-2)x5 = -10. Step 2: Now add the results: (-6) + (-10) = -16. "
                "Final answer: -16."
            ),
        },
        {
            "question": "A submarine is at -120 m. It rises 45 m and then dives 30 m. What is its final position?",
            "options": ["-105 m", "105 m", "-75 m", "-150 m"],
            "answer": "-105 m",
            "hint": "Start at -120, add 45 for rising (moving up = positive change), then subtract 30 for diving (moving down = negative change).",
            "explanation": (
                "Step 1: Start at -120 m. Step 2: Rising 45 m means adding 45: "
                "-120 + 45 = -75 m. Step 3: Diving 30 m more means subtracting 30 (or "
                "adding -30): -75 + (-30) = -105 m. Final answer: -105 m, i.e. 105 m "
                "below sea level."
            ),
        },
        {
            "question": "Simplify: (5-8) x (-2) + 4",
            "options": ["10", "-10", "2", "-2"],
            "answer": "10",
            "hint": "Brackets first: work out (5-8), then multiply, then add.",
            "explanation": (
                "Step 1: Brackets first: 5 - 8 = -3. Step 2: Multiply: "
                "(-3) x (-2) = 6. Step 3: Add: 6 + 4 = 10. Final answer: 10."
            ),
        },
    ],
}

if __name__ == "__main__":
    db.init_db()
    subject_id = db.get_or_create_subject(SUBJECT)
    chapter = db.get_chapter_by_name(subject_id, CHAPTER_NAME)
    if not chapter:
        raise SystemExit(f"Chapter '{CHAPTER_NAME}' not found for subject '{SUBJECT}'.")

    lesson = json.loads(chapter["lesson_json"])
    for topic in lesson["topics"]:
        name = topic["topic"]
        if name in QUICK_CHECKS:
            topic["quick_check"] = QUICK_CHECKS[name]

    db.save_lesson(chapter["id"], json.dumps(lesson))
    print(f"Updated quick-check questions for chapter id {chapter['id']} ({CHAPTER_NAME}).")
