"""One-off update: turns the 'Quick check yourself' items in the Integers
lesson into interactive multiple-choice questions with step-by-step
explanations (used by pages/2_Learn.py for the new interactive quiz UI with
hints-on-wrong-answer and voice read-aloud).

The question bank below covers EVERY exercise in the uploaded chapter
(Exercise 1A, 1B, 1C, 1D, properties of addition/subtraction/multiplication/
division, BODMAS simplification and real-life word problems) — not just a
handful of samples — so a student gets thorough practice on each sub-topic.

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

# Keyed by topic name -> list of quick-check items, each with
# question, options (multiple choices), answer, hint, and a step-by-step
# explanation.
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
        {
            "question": "Find: 7 + (-12)",
            "options": ["-5", "5", "-19", "19"],
            "answer": "-5",
            "hint": "Different signs — subtract the smaller value from the larger and keep the sign of the bigger number (12)",
            "explanation": (
                "Step 1: The numbers have different signs. "
                "Step 2: Subtract the smaller value from the larger: 12 - 7 = 5. "
                "Step 3: 12 is bigger and negative, so the answer is negative. "
                "Final answer: -5."
            ),
        },
        {
            "question": "Find: (-23) + 15",
            "options": ["-8", "8", "-38", "38"],
            "answer": "-8",
            "hint": "Different signs — subtract the smaller value from the larger and keep the sign of the bigger number (23)",
            "explanation": (
                "Step 1: Different signs. "
                "Step 2: 23 - 15 = 8. "
                "Step 3: 23 is bigger and negative, so the answer is negative. "
                "Final answer: -8."
            ),
        },
        {
            "question": "Find: 34 - 50",
            "options": ["-16", "16", "-84", "84"],
            "answer": "-16",
            "hint": "Rewrite as 34 + (-50) — different signs, subtract the smaller from the larger and keep the sign of the bigger number",
            "explanation": (
                "Step 1: Rewrite as 34 + (-50). "
                "Step 2: 50 - 34 = 16. "
                "Step 3: 50 is bigger and negative, so the answer is negative. "
                "Final answer: -16."
            ),
        },
        {
            "question": "Find: (-18) - (-25)",
            "options": ["7", "-7", "43", "-43"],
            "answer": "7",
            "hint": "Subtracting a negative is the same as adding the positive — rewrite as (-18) + 25",
            "explanation": (
                "Step 1: Subtracting a negative number means adding its positive: "
                "(-18) - (-25) = (-18) + 25. "
                "Step 2: Different signs, so subtract: 25 - 18 = 7. "
                "Step 3: 25 is bigger and positive, so the answer is positive. "
                "Final answer: 7."
            ),
        },
        {
            "question": "What is (-45) + 45?",
            "options": ["0", "90", "-90", "45"],
            "answer": "0",
            "hint": "These two numbers are additive inverses of each other — what do they add up to?",
            "explanation": (
                "Step 1: -45 and 45 are additive inverses (same value, opposite signs). "
                "Step 2: Any number plus its additive inverse equals 0. Final answer: 0."
            ),
        },
        {
            "question": "Find the absolute value of -56.",
            "options": ["56", "-56", "0", "1"],
            "answer": "56",
            "hint": "The absolute value is the distance from zero on the number line — always positive (or zero)",
            "explanation": (
                "Step 1: The absolute value of a number is its distance from 0, ignoring "
                "the sign. Step 2: |-56| = 56. Final answer: 56."
            ),
        },
        {
            "question": "A bird is flying 8 m above the ground (+8 m). It then dives down 15 m. What is its new height relative to the ground?",
            "options": ["-7 m", "7 m", "-23 m", "23 m"],
            "answer": "-7 m",
            "hint": "Start at +8 and subtract 15 for diving down",
            "explanation": (
                "Step 1: Start at +8 m. Step 2: Diving down 15 m means subtracting 15: "
                "8 - 15 = -7. Step 3: A negative height means 7 m below ground level. "
                "Final answer: -7 m."
            ),
        },
        {
            "question": "Find: (-7) + (-7) + (-7)",
            "options": ["-21", "21", "-14", "14"],
            "answer": "-21",
            "hint": "Adding the same negative number three times is the same as multiplying it by 3",
            "explanation": (
                "Step 1: (-7) + (-7) + (-7) = 3 x (-7). "
                "Step 2: 3 x 7 = 21, and the result is negative. Final answer: -21."
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
        {
            "question": "True or False: The sum of two integers is always an integer (closure property of addition).",
            "options": ["True", "False"],
            "answer": "True",
            "hint": "Try a few examples — positive+positive, negative+negative, mixed. Is the result ever NOT an integer?",
            "explanation": (
                "Step 1: Try a few examples: 5+3=8, (-5)+(-3)=-8, 5+(-3)=2 — all are "
                "integers. Step 2: This is always true. Integers are CLOSED under "
                "addition. The statement is TRUE."
            ),
        },
        {
            "question": "Fill in the blank using the commutative property: 5 + 3 = ___ + 5",
            "options": ["3", "5", "8", "0"],
            "answer": "3",
            "hint": "The commutative property says a + b = b + a — just swap the order.",
            "explanation": (
                "Step 1: The commutative property of addition says a + b = b + a. "
                "Step 2: So 5 + 3 = 3 + 5. The blank is 3."
            ),
        },
        {
            "question": "Using the associative property, find the value of [(-18) + 4] + 6 (this should equal (-18) + [4 + 6]).",
            "options": ["-8", "8", "-28", "28"],
            "answer": "-8",
            "hint": "Work out the brackets first: [(-18)+4] = -14, then add 6.",
            "explanation": (
                "Step 1: [(-18)+4]+6 = (-14)+6 = -8. "
                "Step 2: Check the other grouping: (-18)+[4+6] = (-18)+10 = -8. "
                "Step 3: Both groupings give -8, showing the associative property. "
                "Final answer: -8."
            ),
        },
        {
            "question": "Is the statement '(18 - 6) = 18 - (6 - 3)' TRUE or FALSE?",
            "options": ["True", "False"],
            "answer": "False",
            "hint": "Work out both sides separately and compare.",
            "explanation": (
                "Step 1: Left side: 18 - 6 = 12. "
                "Step 2: Right side: 18 - (6-3) = 18 - 3 = 15. "
                "Step 3: 12 is not equal to 15, so the statement is FALSE. "
                "(This shows subtraction is not associative.)"
            ),
        },
        {
            "question": "What number must be added to -34 so that the result is still -34?",
            "options": ["0", "34", "-34", "1"],
            "answer": "0",
            "hint": "This is the additive identity property — what value never changes a number when added to it?",
            "explanation": (
                "Step 1: Adding 0 to any integer keeps it unchanged — this is the "
                "additive identity property. Step 2: -34 + 0 = -34. Final answer: 0."
            ),
        },
        {
            "question": "True or False: Subtraction of integers is associative, e.g. (8-5)-2 = 8-(5-2).",
            "options": ["True", "False"],
            "answer": "False",
            "hint": "Work out both sides and compare — do they give the same value?",
            "explanation": (
                "Step 1: Left side: (8-5)-2 = 3-2 = 1. "
                "Step 2: Right side: 8-(5-2) = 8-3 = 5. "
                "Step 3: 1 is not equal to 5, so subtraction is NOT associative. "
                "The statement is FALSE."
            ),
        },
        {
            "question": "Find: -(-(-8))",
            "options": ["-8", "8", "0", "16"],
            "answer": "-8",
            "hint": "Work from the inside out — each '-' sign flips the sign of the number.",
            "explanation": (
                "Step 1: Start with -8. Step 2: Apply the innermost negative: "
                "-(-8) = 8. Step 3: Apply the outer negative: -(8) = -8. "
                "Step 4: Three negative signs (odd count) means the final sign flips "
                "once overall. Final answer: -8."
            ),
        },
        {
            "question": "Find: 89 + 36 + 11 (hint: regroup to make the sum easier)",
            "options": ["136", "126", "146", "116"],
            "answer": "136",
            "hint": "Use the associative property — group 89 and 11 together first since they make a round number.",
            "explanation": (
                "Step 1: Regroup using the associative property: "
                "89 + 36 + 11 = (89 + 11) + 36. Step 2: 89 + 11 = 100. "
                "Step 3: 100 + 36 = 136. Final answer: 136."
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
        {
            "question": "Find the product: (-7) x (-3)",
            "options": ["21", "-21", "10", "-10"],
            "answer": "21",
            "hint": "Same signs (both negative) — the product is positive.",
            "explanation": (
                "Step 1: Both numbers are negative — same signs — so the product is "
                "POSITIVE. Step 2: 7 x 3 = 21. Final answer: 21."
            ),
        },
        {
            "question": "Find the product: (-1861) x 0",
            "options": ["0", "-1861", "1861", "1"],
            "answer": "0",
            "hint": "What happens when any integer is multiplied by zero?",
            "explanation": (
                "Step 1: Any number multiplied by 0 gives 0 (Property of Zero). "
                "Final answer: 0."
            ),
        },
        {
            "question": "Find the product: (-8) x (-5)",
            "options": ["40", "-40", "13", "-13"],
            "answer": "40",
            "hint": "Same signs — the product is positive.",
            "explanation": (
                "Step 1: Both numbers are negative — same signs — product is "
                "POSITIVE. Step 2: 8 x 5 = 40. Final answer: 40."
            ),
        },
        {
            "question": "Find the product: (-11) x (-9)",
            "options": ["99", "-99", "20", "-20"],
            "answer": "99",
            "hint": "Same signs — the product is positive.",
            "explanation": (
                "Step 1: Both negative — same signs — product is POSITIVE. "
                "Step 2: 11 x 9 = 99. Final answer: 99."
            ),
        },
        {
            "question": "Find the product: (+21) x (-100)",
            "options": ["-2100", "2100", "-121", "121"],
            "answer": "-2100",
            "hint": "Different signs — the product is negative.",
            "explanation": (
                "Step 1: One positive, one negative — different signs — product is "
                "NEGATIVE. Step 2: 21 x 100 = 2100. Final answer: -2100."
            ),
        },
        {
            "question": "Find the product: (-18) x (-15)",
            "options": ["270", "-270", "33", "-33"],
            "answer": "270",
            "hint": "Same signs — the product is positive.",
            "explanation": (
                "Step 1: Both negative — same signs — product is POSITIVE. "
                "Step 2: 18 x 15 = 270. Final answer: 270."
            ),
        },
        {
            "question": "Find the product: 0 x (+2341)",
            "options": ["0", "2341", "-2341", "1"],
            "answer": "0",
            "hint": "Zero times any number is always...",
            "explanation": (
                "Step 1: Property of Zero — any integer multiplied by 0 gives 0. "
                "Final answer: 0."
            ),
        },
        {
            "question": "Find the product: (+27) x (+13)",
            "options": ["351", "40", "-351", "313"],
            "answer": "351",
            "hint": "Same signs (both positive) — the product is positive. Multiply the values.",
            "explanation": (
                "Step 1: Both numbers positive — same signs — product is POSITIVE. "
                "Step 2: 27 x 13 = 351. Final answer: 351."
            ),
        },
        {
            "question": "(-3) x (+5) = (+5) x (-3). Which property of multiplication does this show?",
            "options": [
                "Commutative property of multiplication",
                "Associative property of multiplication",
                "Distributive property",
                "Multiplicative identity",
            ],
            "answer": "Commutative property of multiplication",
            "hint": "Notice the order of the two numbers has been swapped — the answer doesn't change.",
            "explanation": (
                "Step 1: Both sides give the same product (-15), just with the "
                "numbers in a different order. Step 2: When swapping the order of "
                "multiplication doesn't change the result, that's the COMMUTATIVE "
                "property: a x b = b x a."
            ),
        },
        {
            "question": "Is the product of two integers, e.g. (-8) x (-5), always an integer?",
            "options": [
                "Yes — integers are closed under multiplication",
                "No — it can be a fraction",
                "Only if both numbers are positive",
                "Only if one number is zero",
            ],
            "answer": "Yes — integers are closed under multiplication",
            "hint": "Try a few examples of integer x integer — is the result ever NOT a whole number?",
            "explanation": (
                "Step 1: (-8) x (-5) = 40, which is an integer. Step 2: This is true "
                "for ANY two integers — the product is always an integer. This is "
                "called CLOSURE under multiplication."
            ),
        },
        {
            "question": "Verify the associative property: find (8 x 9) x 5 and 8 x (9 x 5). What value do both give?",
            "options": ["360", "72", "45", "320"],
            "answer": "360",
            "hint": "Work out each grouping separately — (8x9) first, then x5; and (9x5) first, then 8x that.",
            "explanation": (
                "Step 1: (8x9)x5 = 72 x 5 = 360. Step 2: 8x(9x5) = 8 x 45 = 360. "
                "Step 3: Both groupings give 360, showing multiplication is "
                "ASSOCIATIVE."
            ),
        },
        {
            "question": "What is (-23) x 1?",
            "options": ["-23", "23", "0", "1"],
            "answer": "-23",
            "hint": "What does multiplying by 1 do to any number? (Multiplicative identity)",
            "explanation": (
                "Step 1: Multiplying any integer by 1 leaves it unchanged — this is "
                "the MULTIPLICATIVE IDENTITY property. Step 2: (-23) x 1 = -23. "
                "Final answer: -23."
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
        {
            "question": "Find: (+8) ÷ (+2)",
            "options": ["4", "-4", "16", "-16"],
            "answer": "4",
            "hint": "Same signs (both positive) — the quotient is positive.",
            "explanation": (
                "Step 1: Both numbers positive — same signs — quotient is POSITIVE. "
                "Step 2: 8 ÷ 2 = 4. Final answer: 4."
            ),
        },
        {
            "question": "Find: (-24) ÷ (-8)",
            "options": ["3", "-3", "16", "-16"],
            "answer": "3",
            "hint": "Same signs (both negative) — the quotient is positive.",
            "explanation": (
                "Step 1: Both numbers negative — same signs — quotient is POSITIVE. "
                "Step 2: 24 ÷ 8 = 3. Final answer: 3."
            ),
        },
        {
            "question": "Find: (+42) ÷ (-7)",
            "options": ["-6", "6", "-49", "49"],
            "answer": "-6",
            "hint": "Different signs — the quotient is negative.",
            "explanation": (
                "Step 1: Different signs — quotient is NEGATIVE. "
                "Step 2: 42 ÷ 7 = 6. Final answer: -6."
            ),
        },
        {
            "question": "Find: (-36) ÷ (+6)",
            "options": ["-6", "6", "-30", "30"],
            "answer": "-6",
            "hint": "Different signs — the quotient is negative.",
            "explanation": (
                "Step 1: Different signs — quotient is NEGATIVE. "
                "Step 2: 36 ÷ 6 = 6. Final answer: -6."
            ),
        },
        {
            "question": "Find: 0 ÷ (+29)",
            "options": ["0", "29", "-29", "1"],
            "answer": "0",
            "hint": "What do you get when zero is divided by any non-zero number?",
            "explanation": (
                "Step 1: Zero divided by any non-zero integer is always 0. "
                "Final answer: 0."
            ),
        },
        {
            "question": "Find: (+48) ÷ (+12)",
            "options": ["4", "-4", "36", "60"],
            "answer": "4",
            "hint": "Same signs — the quotient is positive. Divide the values.",
            "explanation": (
                "Step 1: Both positive — same signs — quotient is POSITIVE. "
                "Step 2: 48 ÷ 12 = 4. Final answer: 4."
            ),
        },
        {
            "question": "Find: (-52) ÷ (+13)",
            "options": ["-4", "4", "-39", "39"],
            "answer": "-4",
            "hint": "Different signs — the quotient is negative.",
            "explanation": (
                "Step 1: Different signs — quotient is NEGATIVE. "
                "Step 2: 52 ÷ 13 = 4. Final answer: -4."
            ),
        },
        {
            "question": "Find: (-150) ÷ (-10)",
            "options": ["15", "-15", "140", "-140"],
            "answer": "15",
            "hint": "Same signs — the quotient is positive.",
            "explanation": (
                "Step 1: Both negative — same signs — quotient is POSITIVE. "
                "Step 2: 150 ÷ 10 = 15. Final answer: 15."
            ),
        },
        {
            "question": "True or False: Division of integers is commutative, e.g. 8 ÷ 2 = 2 ÷ 8.",
            "options": ["True", "False"],
            "answer": "False",
            "hint": "Work out both sides — do they give the same value?",
            "explanation": (
                "Step 1: 8 ÷ 2 = 4. Step 2: 2 ÷ 8 = 0.25. Step 3: 4 is not equal to "
                "0.25, so division is NOT commutative. The statement is FALSE."
            ),
        },
        {
            "question": "What happens if you try to divide an integer by 0?",
            "options": [
                "It is undefined / not allowed",
                "The answer is always 0",
                "The answer is always 1",
                "The answer is the same integer",
            ],
            "answer": "It is undefined / not allowed",
            "hint": "Is there any number that, when multiplied by 0, gives a non-zero result?",
            "explanation": (
                "Step 1: Division by b means finding a number that, when multiplied "
                "by b, gives the original number. Step 2: No number times 0 can give "
                "a non-zero result, so division by 0 has no answer. It is UNDEFINED "
                "and not allowed."
            ),
        },
        {
            "question": "Find: (-49) ÷ (-49)",
            "options": ["1", "-1", "0", "49"],
            "answer": "1",
            "hint": "What do you get when you divide any non-zero integer by itself?",
            "explanation": (
                "Step 1: Same signs (both negative) — quotient is positive. "
                "Step 2: Any non-zero integer divided by itself equals 1. "
                "Final answer: 1."
            ),
        },
        {
            "question": "Find: (-36) ÷ 1",
            "options": ["-36", "36", "1", "-1"],
            "answer": "-36",
            "hint": "What does dividing by 1 do to a number?",
            "explanation": (
                "Step 1: Dividing any integer by 1 leaves it unchanged. "
                "Step 2: (-36) ÷ 1 = -36. Final answer: -36."
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
        {
            "question": "Simplify: (-21) + [(+16) + (-13)]",
            "options": ["-18", "18", "-50", "50"],
            "answer": "-18",
            "hint": "Work inside the square brackets first: (+16)+(-13), then add to -21.",
            "explanation": (
                "Step 1: Brackets first: (+16)+(-13) = 3. "
                "Step 2: (-21) + 3 = -18. Final answer: -18."
            ),
        },
        {
            "question": "Simplify: -2 + (-8) x 3 - (-10)",
            "options": ["-16", "32", "-30", "8"],
            "answer": "-16",
            "hint": "BODMAS: do the multiplication first, then add/subtract left to right.",
            "explanation": (
                "Step 1: Multiplication first: (-8) x 3 = -24. "
                "Step 2: Now the expression is -2 + (-24) - (-10). "
                "Step 3: -2 + (-24) = -26. Step 4: -26 - (-10) = -26 + 10 = -16. "
                "Final answer: -16."
            ),
        },
        {
            "question": "Simplify: 100 + (-10) x (3 - 5)",
            "options": ["120", "80", "-120", "60"],
            "answer": "120",
            "hint": "Brackets first, then multiplication, then addition.",
            "explanation": (
                "Step 1: Brackets first: 3 - 5 = -2. Step 2: Multiply: "
                "(-10) x (-2) = 20. Step 3: Add: 100 + 20 = 120. Final answer: 120."
            ),
        },
        {
            "question": "Using the distributive property, simplify: (-343) x 22 + (-343) x 78",
            "options": ["-34300", "34300", "-3430", "-343"],
            "answer": "-34300",
            "hint": "Both terms have (-343) in common — factor it out: (-343) x (22 + 78).",
            "explanation": (
                "Step 1: Factor out the common term: "
                "(-343) x 22 + (-343) x 78 = (-343) x (22 + 78). "
                "Step 2: 22 + 78 = 100. Step 3: (-343) x 100 = -34300. "
                "Final answer: -34300."
            ),
        },
        {
            "question": "Mr. Nair had ₹2500 in his bank account. He deposited ₹1250, then withdrew ₹750, then deposited ₹500, then withdrew ₹300. What is his final balance?",
            "options": ["₹3200", "₹2700", "₹4500", "₹1700"],
            "answer": "₹3200",
            "hint": "Deposits add to the balance, withdrawals subtract from it — combine step by step.",
            "explanation": (
                "Step 1: Start with 2500. Step 2: +1250 → 3750. Step 3: -750 → 3000. "
                "Step 4: +500 → 3500. Step 5: -300 → 3200. Final answer: ₹3200."
            ),
        },
        {
            "question": "The temperature at the summit of a mountain is -8°C. The base camp is 15°C warmer. What is the temperature at the base camp?",
            "options": ["7°C", "-23°C", "23°C", "-7°C"],
            "answer": "7°C",
            "hint": "'Warmer' means adding the difference to the summit temperature.",
            "explanation": (
                "Step 1: Start at -8°C. Step 2: '15°C warmer' means add 15: "
                "(-8) + 15 = 7. Final answer: 7°C."
            ),
        },
        {
            "question": "The product of two numbers is 105. If one of the numbers is (-7), what is the other number?",
            "options": ["-15", "15", "-735", "735"],
            "answer": "-15",
            "hint": "If a x b = 105 and a = -7, find b by dividing: b = 105 ÷ (-7).",
            "explanation": (
                "Step 1: We need b such that (-7) x b = 105. "
                "Step 2: b = 105 ÷ (-7). Step 3: Different signs → quotient is "
                "negative: 105 ÷ 7 = 15, so b = -15. Final answer: -15."
            ),
        },
        {
            "question": "A book costs ₹96. Mahesh bought 60 such books, but the accountant billed each book as ₹5 less than the actual cost. What is the total difference (shortfall) in the bill?",
            "options": ["₹300", "₹96", "₹60", "₹5760"],
            "answer": "₹300",
            "hint": "Find the difference per book first, then multiply by the number of books.",
            "explanation": (
                "Step 1: Difference per book = ₹5. Step 2: Total difference = "
                "5 x 60 = 300. Final answer: ₹300 (the bill was ₹300 less than it "
                "should have been)."
            ),
        },
        {
            "question": "Each floor of a 26-storey building is 3 m high. A lift starts at the ground floor and rises at 5 m per second. How many seconds does it take to reach the 26th floor?",
            "options": ["15 seconds", "26 seconds", "75 seconds", "5 seconds"],
            "answer": "15 seconds",
            "hint": "First find the total height to climb (number of floors above ground x height per floor), then divide by the speed.",
            "explanation": (
                "Step 1: Reaching the 26th floor from the ground floor means "
                "climbing 25 floors. Step 2: Total height = 25 x 3 = 75 m. "
                "Step 3: Time = 75 ÷ 5 = 15 seconds. Final answer: 15 seconds."
            ),
        },
        {
            "question": "A diver collects a water sample every 3 m below the surface, starting at the surface (0 m) down to a final depth of 36 m. How many samples did he collect in total?",
            "options": ["13", "12", "36", "9"],
            "answer": "13",
            "hint": "List the depths: 0, 3, 6, ... 36 — how many numbers are in this list?",
            "explanation": (
                "Step 1: Samples are taken at 0, 3, 6, 9, ..., 36 m. "
                "Step 2: Number of samples = (36 ÷ 3) + 1 = 12 + 1 = 13 (the +1 "
                "accounts for the sample at the surface, 0 m). Final answer: 13."
            ),
        },
        {
            "question": "Ranjan started with 60 marbles. In 8 games he gained 5 marbles each time, and in 4 games he lost 4 marbles each time. How many marbles did he end up with?",
            "options": ["84", "100", "44", "68"],
            "answer": "84",
            "hint": "Find the total gained, the total lost, then combine with the starting amount.",
            "explanation": (
                "Step 1: Total gained = 8 x 5 = 40. Step 2: Total lost = 4 x 4 = 16. "
                "Step 3: Final marbles = 60 + 40 - 16 = 84. Final answer: 84."
            ),
        },
        {
            "question": "A submarine descends from the surface at a rate of (-20) m per minute. How far below the surface is it after 7 minutes?",
            "options": ["-140 m", "140 m", "-27 m", "-3 m"],
            "answer": "-140 m",
            "hint": "Multiply the rate per minute by the number of minutes.",
            "explanation": (
                "Step 1: Rate = -20 m/minute (negative means going down). "
                "Step 2: After 7 minutes: (-20) x 7 = -140. Final answer: -140 m, "
                "i.e. 140 m below the surface."
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
