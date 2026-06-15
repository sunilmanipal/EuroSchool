"""One-off update: replaces the 'Chapter 1 - Integers' lesson with a richer,
more detailed version aimed at a 13-year-old — longer explanations with
real-life analogies, more worked examples, and a 'deep dive' section per
topic for extra help when a student is struggling.

Run with:
    ./venv/bin/python scripts/update_integers_lesson.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import db

SUBJECT = "Maths"
CHAPTER_NAME = "Chapter 1 - Integers"

LESSON = {
    "topics": [
        {
            "topic": "Addition and Subtraction of Integers",
            "explanation": (
                "Think of integers as positions on a number line that stretches in both "
                "directions from 0 — positive numbers go to the right, negative numbers go "
                "to the left. Adding a positive number means moving RIGHT (forward), and "
                "adding a negative number means moving LEFT (backward). For example, "
                "starting at 3 and adding (-5) means moving 5 steps left, landing on -2.\n\n"
                "Another great way to think about it: imagine money. A positive number is "
                "money you HAVE, and a negative number is money you OWE (a debt). If you "
                "have Rs 50 and you owe Rs 80, your 'net worth' is 50 + (-80) = -30, meaning "
                "you actually owe Rs 30 overall.\n\n"
                "Rules to remember:\n"
                "- SAME signs (both positive or both negative): ADD the numbers and KEEP "
                "the sign. E.g. (-7)+(-5) = -(7+5) = -12\n"
                "- DIFFERENT signs: SUBTRACT the smaller value from the larger value, and "
                "the answer takes the sign of the BIGGER number. E.g. (-9)+4: 9 is bigger, "
                "so the answer is negative: -(9-4) = -5\n\n"
                "For SUBTRACTION, the golden rule is: subtracting a number is the SAME as "
                "adding its opposite. a - b = a + (-b). So 5 - (-3) becomes 5 + 3 = 8 "
                "(taking away a debt of 3 is like getting a gift of 3!). This 'flip the "
                "sign and add' trick works every single time, no matter how big or "
                "complicated the numbers are."
            ),
            "worked_examples": [
                "(-7) + (-5): Both numbers are negative (same sign). Add 7 + 5 = 12, then "
                "keep the negative sign. Answer: -12. (Think: you owe Rs 7, then you owe "
                "another Rs 5 — now you owe Rs 12 in total.)",
                "(-8) + 12 - (-5): Work left to right. Step 1: (-8) + 12 -> different "
                "signs, 12 is bigger, so answer = +(12-8) = 4. Step 2: 4 - (-5) -> "
                "'subtracting a negative' becomes 'adding a positive', so 4 + 5 = 9. "
                "Final answer: 9",
                "15 - 20: Rewrite as 15 + (-20). Different signs, 20 is bigger, so "
                "answer = -(20-15) = -5. (Think: you have Rs 15 but spend Rs 20 — you end "
                "up Rs 5 short, i.e. -5.)",
                "(-12) - (-12): Subtracting a negative becomes adding a positive: "
                "(-12) + 12 = 0. (Owing Rs 12 and then having that debt cancelled means "
                "you're back to zero!)",
            ],
            "common_mistakes": [
                "Forgetting that subtracting a negative means adding the positive "
                "(writing 5 - (-3) = 2 instead of 5 + 3 = 8). Tip: always rewrite "
                "'- (-x)' as '+ x' BEFORE doing anything else.",
                "When adding numbers with different signs, ADDING the values instead of "
                "SUBTRACTING them. Remember: different signs -> subtract; same signs -> add.",
                "Losing track of the sign when there are several negative numbers in a "
                "row — work ONE step at a time and write down the running total after "
                "each step instead of doing it all in your head.",
            ],
            "quick_check": [
                {"question": "Find: (-9) + 4", "answer": "-5", "hint": "Different signs — subtract the smaller value from the larger, and keep the sign of the number with the bigger value (9)"},
                {"question": "Find: 6 - (-11)", "answer": "17", "hint": "Subtracting a negative number is the same as adding the positive — turn it into 6 + 11"},
                {"question": "Find: (-15) + (-8)", "answer": "-23", "hint": "Same sign (both negative) — add the values and keep the negative sign"},
                {"question": "Find: (-20) - 7", "answer": "-27", "hint": "Rewrite as (-20) + (-7) — same sign, so add and keep the negative"},
            ],
            "deep_dive": {
                "explanation": (
                    "Still finding this tricky? Try the NUMBER LINE METHOD: draw a "
                    "horizontal line and mark 0 in the middle, with positive numbers to "
                    "the right and negative numbers to the left. To add a number, start "
                    "at your first number and: if you're ADDING A POSITIVE, hop that many "
                    "steps to the RIGHT; if you're ADDING A NEGATIVE, hop that many steps "
                    "to the LEFT. For subtraction, first flip the sign of the second "
                    "number (turn - into +, or + into -), then do the same hopping. "
                    "Physically drawing this out for the first 10-15 problems really "
                    "helps the rules 'stick' so you stop needing the line."
                ),
                "extra_examples": [
                    "Use the number line for (-4) + 7: Start at -4. Adding +7 means hop 7 "
                    "steps RIGHT: -4 -> -3 -> -2 -> -1 -> 0 -> 1 -> 2 -> 3. You land on 3.",
                    "Use the number line for 2 - 6: Rewrite as 2 + (-6). Start at 2, hop 6 "
                    "steps LEFT: 2 -> 1 -> 0 -> -1 -> -2 -> -3 -> -4. You land on -4.",
                    "Money trick for (-25) + (-10) + 30: Add up all the 'owe' amounts "
                    "first: (-25)+(-10) = -35 (you owe Rs 35). Then add what you have: "
                    "-35+30 = -5 (you still owe Rs 5 overall).",
                ],
            },
        },
        {
            "topic": "Properties of Addition and Subtraction of Integers",
            "explanation": (
                "Properties are like 'rules of the game' that ALWAYS work for addition of "
                "integers, no matter which numbers you pick. Knowing them helps you check "
                "your work and rearrange tricky sums to make them easier.\n\n"
                "1. CLOSURE: Adding any two integers always gives another integer — you "
                "never 'fall out' of the integer family. E.g. 5 + (-9) = -4, still an "
                "integer.\n\n"
                "2. COMMUTATIVE: The order doesn't matter — a + b = b + a. E.g. (-4)+9 = 5 "
                "and 9+(-4) = 5. This is super useful: if a sum looks hard one way, try "
                "flipping the order!\n\n"
                "3. ASSOCIATIVE: When adding three or more numbers, the GROUPING doesn't "
                "matter — (a+b)+c = a+(b+c). This means you can add numbers in whatever "
                "order is easiest, e.g. group the negatives together first.\n\n"
                "4. ADDITIVE IDENTITY: Adding 0 to any number doesn't change it — a+0 = a. "
                "Zero is like a 'do nothing' button.\n\n"
                "5. ADDITIVE INVERSE: Every integer has an 'opposite' that cancels it out "
                "to zero — a + (-a) = 0. E.g. the additive inverse of -8 is 8, because "
                "(-8)+8=0. Think of it as paying off a debt exactly.\n\n"
                "IMPORTANT WARNING: SUBTRACTION does NOT follow the commutative or "
                "associative properties! 8-3 = 5 but 3-8 = -5 (different!). And "
                "(10-4)-2 = 4 but 10-(4-2) = 8 (different!). Order and grouping MATTER "
                "for subtraction."
            ),
            "worked_examples": [
                "Commutative check: (-4)+9 = 5, and 9+(-4) = 5. Same answer either way — "
                "addition is commutative.",
                "Associative check: [2+(-5)]+7: first 2+(-5)=-3, then -3+7=4. And "
                "2+[(-5)+7]: first (-5)+7=2, then 2+2=4. Both groupings give 4.",
                "Additive inverse: What number added to -8 gives 0? Since (-8)+8=0, the "
                "additive inverse of -8 is 8. (Owing Rs 8 and then receiving exactly Rs 8 "
                "brings your balance to Rs 0.)",
                "Why subtraction breaks the rules: 8-3=5 but 3-8=-5. These are NOT the "
                "same, so subtraction is NOT commutative.",
            ],
            "common_mistakes": [
                "Assuming subtraction is commutative — always TEST with real numbers if "
                "unsure.",
                "Confusing 'additive inverse' (the number that gives 0 when ADDED) with "
                "'reciprocal' (the number that gives 1 when MULTIPLIED) — these are "
                "different ideas from different chapters.",
                "Writing a+0=0 instead of a — remember 0 is the 'do nothing' number, the "
                "answer stays the SAME as 'a'.",
            ],
            "quick_check": [
                {"question": "Is subtraction of integers commutative? Give an example to support your answer.", "answer": "No. For example, 8 - 3 = 5 but 3 - 8 = -5, which are different values.", "hint": "Try swapping the order of two different numbers in a subtraction and compare"},
                {"question": "Write the additive inverse of -17.", "answer": "17", "hint": "What number added to -17 gives 0?"},
                {"question": "Verify the associative property of addition using -2, 6 and -9.", "answer": "[(-2)+6]+(-9) = 4+(-9) = -5, and (-2)+[6+(-9)] = (-2)+(-3) = -5. Both equal -5, so the property holds.", "hint": "Group the first two numbers together first, then group the last two, and compare the results"},
                {"question": "True or False: (-5) + 0 = -5", "answer": "True", "hint": "0 is the additive identity — it never changes the value it's added to"},
            ],
            "deep_dive": {
                "explanation": (
                    "A good way to REMEMBER these properties for a test is to link each "
                    "one to a short phrase: Closure = 'stays in the family', Commutative "
                    "= 'order doesn't matter — like a handshake, both ways are the same', "
                    "Associative = 'grouping doesn't matter — like splitting a group of "
                    "friends into two smaller groups, the total number of friends is the "
                    "same', Identity = '0 does nothing', Inverse = 'opposites cancel out, "
                    "like a debt being paid off exactly'. When a question asks you to "
                    "'name the property', look for these clue words: did the ORDER "
                    "change (commutative)? Did the GROUPING/brackets change "
                    "(associative)? Is 0 involved (identity)? Are the two numbers "
                    "opposites that sum to 0 (inverse)?"
                ),
                "extra_examples": [
                    "Identify the property: (-13) + 13 = 0 -> This is the ADDITIVE "
                    "INVERSE property, because -13 and 13 are opposites that sum to 0.",
                    "Identify the property: 7 + (-2) = (-2) + 7 -> This is the "
                    "COMMUTATIVE property, because only the ORDER changed.",
                    "Identify the property: [4+(-6)]+9 = 4+[(-6)+9] -> This is the "
                    "ASSOCIATIVE property, because only the GROUPING (brackets) changed.",
                ],
            },
        },
        {
            "topic": "Multiplication of Integers and its Properties",
            "explanation": (
                "Multiplication is repeated addition. (-3) x 4 means 'add -3 four times': "
                "(-3)+(-3)+(-3)+(-3) = -12. This helps explain WHY a positive times a "
                "negative gives a negative!\n\n"
                "For (-3) x (-4) — a negative times a negative — think of it as 'taking "
                "away a debt, 4 times', which INCREASES your money. If you owe Rs 3 and "
                "that debt is removed 4 times, you gain Rs 12. That's why two negatives "
                "multiply to a POSITIVE.\n\n"
                "SIGN RULES (memorize these!):\n"
                "- (+) x (+) = (+)\n"
                "- (-) x (-) = (+)   [SAME signs -> POSITIVE]\n"
                "- (+) x (-) = (-)\n"
                "- (-) x (+) = (-)   [DIFFERENT signs -> NEGATIVE]\n\n"
                "A quick trick: COUNT the number of negative signs in the whole "
                "multiplication. If there's an EVEN number of negatives, the answer is "
                "POSITIVE. If there's an ODD number of negatives, the answer is "
                "NEGATIVE. E.g. (-2) x (-3) x (-1) has THREE negatives (odd) -> the "
                "answer is negative: -6.\n\n"
                "PROPERTIES (similar to addition, but for x):\n"
                "- Closure: integer x integer = integer\n"
                "- Commutative: a x b = b x a (order doesn't matter)\n"
                "- Associative: (a x b) x c = a x (b x c) (grouping doesn't matter)\n"
                "- Distributive: a x (b+c) = a x b + a x c — VERY useful for breaking big "
                "multiplications into easier pieces\n"
                "- Multiplicative identity: a x 1 = a (multiplying by 1 changes nothing)\n"
                "- Property of zero: a x 0 = 0, ALWAYS — no matter how big or complicated "
                "'a' is"
            ),
            "worked_examples": [
                "(-6) x 7: different signs -> negative. 6x7=42, so answer = -42. "
                "(Think: 7 groups of -6 = -42.)",
                "(-9) x (-5): same signs (both negative) -> positive. 9x5=45, so "
                "answer = 45.",
                "Distributive property: (-4) x [5+(-3)]. Method 1 (brackets first): "
                "5+(-3)=2, then (-4)x2=-8. Method 2 (distribute): (-4)x5 + (-4)x(-3) = "
                "-20+12 = -8. Both methods give -8!",
                "Counting negatives trick: (-2) x (-3) x (-1) x 5. There are THREE "
                "negative numbers (odd count) -> answer is negative. 2x3x1x5=30, so "
                "answer = -30.",
            ],
            "common_mistakes": [
                "Getting the sign rule backwards — e.g. thinking (-)x(-) gives a "
                "negative. Remember: SAME signs always give POSITIVE for multiplication.",
                "Forgetting the property of zero and doing unnecessary work, e.g. trying "
                "to 'simplify' 999 x (-87) x 0 the long way instead of instantly "
                "writing 0.",
                "Mixing up distributive (a x (b+c)) with associative ((axb)xc) — "
                "distributive ALWAYS involves a + or - sign INSIDE the brackets being "
                "'shared out'.",
            ],
            "quick_check": [
                {"question": "Find the product: (-12) x (-3)", "answer": "36", "hint": "Same signs (both negative) -> positive"},
                {"question": "Find the product: 15 x (-4)", "answer": "-60", "hint": "Different signs -> negative"},
                {"question": "Use the distributive property to find: 8 x (10 + (-2))", "answer": "8x10 + 8x(-2) = 80 + (-16) = 64", "hint": "Multiply 8 by each term inside the brackets separately, then add the results"},
                {"question": "Find: (-1) x (-1) x (-1) x (-1) x (-5)", "answer": "-5", "hint": "Count ALL the negative signs in the whole expression (there are 5) — an odd count means the answer is negative"},
            ],
            "deep_dive": {
                "explanation": (
                    "If sign rules feel confusing, use this physical model: POSITIVE "
                    "numbers mean 'ADDING groups of something', NEGATIVE numbers mean "
                    "'REMOVING groups of something'. (+3) x (+4) = adding 3 groups of "
                    "+4 = +12. (+3) x (-4) = adding 3 groups of -4 (i.e. 3 debts of 4) = "
                    "-12. (-3) x (+4) = removing 3 groups of +4 (taking away 3 lots of 4 "
                    "good things) = -12. (-3) x (-4) = removing 3 groups of -4 "
                    "(cancelling 3 debts — that's GOOD for you!) = +12. Practising this "
                    "'adding/removing groups' story for 5-6 problems usually makes the "
                    "sign rules feel natural instead of something to memorize."
                ),
                "extra_examples": [
                    "(+5) x (-2): adding 5 groups of a debt of 2 = a total debt of 10 = -10",
                    "(-5) x (+2): removing 5 groups of +2 (taking away 5 lots of 2 good "
                    "things) = -10",
                    "(-5) x (-2): removing 5 groups of a debt of 2 (cancelling 5 debts of "
                    "2) = +10 — your situation improves by 10!",
                ],
            },
        },
        {
            "topic": "Division of Integers and its Properties",
            "explanation": (
                "Division 'undoes' multiplication, so it follows the SAME sign rules: "
                "SAME signs -> POSITIVE quotient, DIFFERENT signs -> NEGATIVE quotient.\n"
                "- (+) / (+) = (+)\n"
                "- (-) / (-) = (+)\n"
                "- (+) / (-) = (-)\n"
                "- (-) / (+) = (-)\n\n"
                "BUT division has some special, important exceptions that multiplication "
                "doesn't have:\n\n"
                "1. NOT CLOSED: dividing two integers doesn't always give an integer. "
                "7 / 2 = 3.5 — not a whole number! So 'the set of integers' is NOT "
                "closed under division (unlike addition, subtraction and "
                "multiplication, which always stay 'in the family').\n\n"
                "2. NOT COMMUTATIVE: a/b is usually NOT the same as b/a. 10/2=5 but "
                "2/10=0.2 — totally different!\n\n"
                "3. NOT ASSOCIATIVE: grouping matters and changes the answer.\n\n"
                "4. DIVISION BY 1: a/1=a (unchanged). DIVISION BY -1: a/(-1)=-a (flips "
                "the sign).\n\n"
                "5. DIVISION BY ZERO IS NOT DEFINED: You can NEVER divide by 0 — it's "
                "not a maths error to be 'fixed', it simply has no answer. (Why? Because "
                "there's no number that, multiplied by 0, gives you back the original "
                "non-zero number.)"
            ),
            "worked_examples": [
                "(-36) / 9: different signs -> negative. 36/9=4, so answer = -4.",
                "(-45) / (-5): same signs -> positive. 45/5=9, so answer = 9.",
                "Why integers aren't closed: 7/2 = 3.5. Since 3.5 isn't an integer, this "
                "shows the result of dividing two integers isn't always an integer.",
                "Not commutative check: 10/(-2)=-5, but (-2)/10=-0.2. These are "
                "different, proving division isn't commutative.",
            ],
            "common_mistakes": [
                "Assuming division of integers always gives a whole number answer.",
                "Believing a/b = b/a (division is NOT commutative — always check the "
                "ORDER given in the question).",
                "Writing a/0=0 — division by zero is UNDEFINED, not zero. Never write a "
                "numeric answer for /0.",
            ],
            "quick_check": [
                {"question": "Find: (-72) / 8", "answer": "-9", "hint": "Different signs -> negative quotient"},
                {"question": "Is 10 / (-2) the same as (-2) / 10? Explain.", "answer": "No. 10/(-2) = -5, but (-2)/10 = -0.2. They are different, so division of integers is not commutative.", "hint": "Calculate both and compare the results"},
                {"question": "Give one example to show that integers are not closed under division.", "answer": "For example, 5 / 2 = 2.5, which is not an integer. So the set of integers is not closed under division.", "hint": "Find two integers whose division does not give a whole number"},
                {"question": "What is (-15) / (-1)?", "answer": "15", "hint": "Dividing by -1 flips the sign — a negative becomes positive"},
            ],
            "deep_dive": {
                "explanation": (
                    "Whenever you see a division problem, do it in TWO steps: STEP 1 — "
                    "work out the SIGN using the rule (same signs = positive, different "
                    "signs = negative). STEP 2 — divide the NUMBERS ignoring the signs, "
                    "then attach the sign from Step 1. Separating 'sign thinking' from "
                    "'number thinking' reduces careless mistakes. Also, before dividing, "
                    "ALWAYS check: is the divisor (the number you're dividing BY) zero? "
                    "If yes — STOP, the expression is undefined, and you should say so "
                    "rather than guessing an answer."
                ),
                "extra_examples": [
                    "(-100) / 25: Step 1, signs are different -> negative. Step 2, "
                    "100/25=4. Final answer: -4",
                    "(-81) / (-9): Step 1, signs are the same -> positive. Step 2, "
                    "81/9=9. Final answer: 9",
                    "5 / 0: Step 1 (check the divisor) — the divisor is 0, so STOP. "
                    "This expression is UNDEFINED — there is no answer.",
                ],
            },
        },
        {
            "topic": "Simplification of Expressions (BODMAS) and Real-life Applications",
            "explanation": (
                "When a maths expression has MULTIPLE operations (+, -, x, / and "
                "brackets all mixed together), you can't just go left to right — you "
                "must follow a strict ORDER called BODMAS:\n"
                "B - Brackets first (work out anything inside ( ), [ ], { })\n"
                "O - 'Of' / Orders (powers and roots, e.g. squares)\n"
                "D - Division\n"
                "M - Multiplication\n"
                "A - Addition\n"
                "S - Subtraction\n\n"
                "Important: Division and Multiplication have EQUAL priority — do them "
                "left to right in the order they appear. The same goes for Addition and "
                "Subtraction — equal priority, left to right.\n\n"
                "REAL-LIFE USES OF INTEGERS — this is where maths becomes USEFUL:\n"
                "- TEMPERATURE: above 0 degrees C is positive, below 0 degrees C "
                "(freezing) is negative. A rise is +, a fall is -.\n"
                "- MONEY: profit/income/deposit is +, loss/expense/withdrawal is -.\n"
                "- HEIGHT & DEPTH: above sea level is +, below sea level (depth) is -.\n"
                "- LIFTS/BUILDINGS: floors above ground are +, basement floors are -.\n\n"
                "In word problems, the FIRST and most important step is to translate the "
                "words into signed numbers (decide what's + and what's -), and THEN do "
                "the calculation using everything you've learned about integers."
            ),
            "worked_examples": [
                "10 + (-4) x 3: Multiplication first: (-4)x3=-12. Then 10+(-12)=-2. "
                "Final answer: -2",
                "7 - (-3) x 2 + (-12) / 4: Do x and / first (left to right): "
                "(-3)x2=-6, and (-12)/4=-3. Now we have 7-(-6)+(-3). Do + and - left to "
                "right: 7-(-6)=7+6=13, then 13+(-3)=10. Final answer: 10",
                "(-2) x [9+(-4)] - 6: Brackets first: 9+(-4)=5. Then (-2)x5=-10. Then "
                "-10-6=-16. Final answer: -16",
                "Real-life: A submarine is at -120 m (120 m below sea level). It rises "
                "45 m, then dives 30 m. Translate: -120 + 45 + (-30). Step 1: "
                "-120+45=-75. Step 2: -75+(-30)=-105. Final position: -105 m, i.e. 105 "
                "m below sea level.",
            ],
            "common_mistakes": [
                "Working strictly left-to-right and ignoring BODMAS order — e.g. doing "
                "10+(-4) first in the first example above, which gives the WRONG answer "
                "of 6x3=18 instead of -2.",
                "Forgetting to simplify INSIDE brackets completely before doing "
                "anything outside them.",
                "In word problems, picking the wrong sign for a quantity (e.g. writing "
                "a 'rise' as negative) — always re-read the problem and decide + or - "
                "BEFORE calculating.",
            ],
            "quick_check": [
                {"question": "Simplify: 10 + (-4) x 3", "answer": "-2", "hint": "Do the multiplication first: (-4)x3=-12, then 10+(-12)"},
                {"question": "Simplify: [(-18) / 3] + (-2) x 5", "answer": "-16", "hint": "Do the division and multiplication first (-6 and -10), then add them"},
                {"question": "A submarine is at -120 m. It rises 45 m and then dives 30 m. What is its final position?", "answer": "-105 m (i.e. 105 m below sea level)", "hint": "Start at -120, add 45 for rising, then subtract 30 for diving"},
                {"question": "Simplify: (5-8) x (-2) + 4", "answer": "10", "hint": "Brackets first: 5-8=-3, then (-3)x(-2)=6, then 6+4"},
            ],
            "deep_dive": {
                "explanation": (
                    "For BODMAS questions, it helps to do ONE operation per line, "
                    "rewriting the WHOLE expression each time so nothing gets lost. For "
                    "word problems, make a small table: 'What happened?' -> 'Sign "
                    "(+/-)' -> 'Number'. List every event from the problem in the "
                    "table, then add a final row that says 'Total = sum of all signed "
                    "numbers'. This turns a scary paragraph into a simple addition sum."
                ),
                "extra_examples": [
                    "Step-by-step rewriting: 20 - 3 x (4-1) + 6/2 -> Step 1 (brackets): "
                    "20 - 3x3 + 6/2 -> Step 2 (x and /): 20 - 9 + 3 -> Step 3 (left to "
                    "right + and -): 11 + 3 = 14",
                    "Word problem table — 'Anita had Rs 200. She spent Rs 350 on a "
                    "gift, then received Rs 120 as pocket money, then spent Rs 80 on "
                    "snacks.' Signed numbers: +200, -350, +120, -80. Total = "
                    "200+(-350)+120+(-80) = -110, meaning Anita is Rs 110 in debt "
                    "overall.",
                    "Word problem table — 'A lift starts at floor 3 (ground=0). It "
                    "goes down 5, down 2 more, then up 4.' Signed numbers: 3, -5, -2, "
                    "+4. Total = 3+(-5)+(-2)+4 = 0, so the lift ends at the ground "
                    "floor.",
                ],
            },
        },
    ]
}

if __name__ == "__main__":
    db.init_db()
    subject_id = db.get_or_create_subject(SUBJECT)
    chapter = db.get_chapter_by_name(subject_id, CHAPTER_NAME)
    if not chapter:
        raise SystemExit(f"Chapter '{CHAPTER_NAME}' not found for subject '{SUBJECT}' — run seed_integers_chapter.py first.")

    db.save_lesson(chapter["id"], json.dumps(LESSON))
    print(f"Updated lesson for chapter id {chapter['id']} ({CHAPTER_NAME}) with {len(LESSON['topics'])} topics, "
          f"each including a 'deep_dive' extra-help section.")
