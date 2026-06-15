"""Offline (no-AI) question generator for chapters where we've hand-built a
template bank — currently 'Chapter 1 - Integers' (Maths, Class 7).

Each call to `generate_offline_paper` produces a fresh, randomized paper:
numbers in the templates are re-rolled every time, so the same skill
category can produce many different-looking questions across papers. This
lets the app create unlimited practice papers without calling the OpenAI
API, and can be weighted towards topics the student is weak in.
"""
import random

from core.ai_engine import SKILL_CATEGORIES, distribute_questions


def _s(n):
    """Format a number for display inside an expression, wrapping negatives
    in brackets the way the textbook does, e.g. -8 -> '(-8)'."""
    return f"({n})" if n < 0 else str(n)


def _nz(rng, lo, hi):
    """A random non-zero integer in [lo, hi]."""
    while True:
        n = rng.randint(lo, hi)
        if n != 0:
            return n


# --------------------------------------------------------------------------
# Knowledge
# --------------------------------------------------------------------------
def g_knowledge_identity(rng):
    return {
        "type": "mcq",
        "topic": "Properties of Addition and Subtraction of Integers",
        "question": "What is the additive identity for integers?",
        "options": ["0", "1", "-1", "It does not exist"],
        "correct_answer": "0",
        "max_marks": 1,
        "explanation": "Adding 0 to any integer does not change its value: a + 0 = a. So 0 is the additive identity.",
    }


g_knowledge_identity.topic = "Properties of Addition and Subtraction of Integers"


def g_knowledge_sign_rule(rng):
    pairs = [
        ("two negative integers", "positive"),
        ("two positive integers", "positive"),
        ("a positive integer and a negative integer", "negative"),
    ]
    desc, correct = rng.choice(pairs)
    return {
        "type": "mcq",
        "topic": "Multiplication of Integers and its Properties",
        "question": f"When you multiply {desc}, the product is always ____.",
        "options": ["positive", "negative", "zero", "cannot be determined"],
        "correct_answer": correct,
        "max_marks": 1,
        "explanation": "Same signs give a positive product; different signs give a negative product.",
    }


g_knowledge_sign_rule.topic = "Multiplication of Integers and its Properties"


# --------------------------------------------------------------------------
# Understanding & Comprehension
# --------------------------------------------------------------------------
def g_understand_sub_commute(rng):
    a = rng.randint(6, 18)
    b = rng.randint(1, a - 1)
    return {
        "type": "short",
        "topic": "Properties of Addition and Subtraction of Integers",
        "question": (
            f"Is {a} - {b} the same as {b} - {a}? Calculate both and explain whether "
            "subtraction of integers is commutative."
        ),
        "options": [],
        "correct_answer": (
            f"{a} - {b} = {a - b} and {b} - {a} = {b - a}. These are different, so "
            "subtraction of integers is NOT commutative."
        ),
        "max_marks": 2,
        "explanation": "The commutative property requires a-b = b-a for all values, which fails here.",
    }


g_understand_sub_commute.topic = "Properties of Addition and Subtraction of Integers"


def g_understand_division_closure(rng):
    a = rng.choice([5, 7, 9, 11, 13, 15])
    b = 2
    return {
        "type": "short",
        "topic": "Division of Integers and its Properties",
        "question": (
            f"Is {a} / {b} an integer? Use your answer to explain why integers are not "
            "closed under division."
        ),
        "options": [],
        "correct_answer": (
            f"{a} / {b} = {a / b}, which is not an integer. So dividing two integers "
            "does not always give an integer, meaning integers are not closed under "
            "division."
        ),
        "max_marks": 2,
        "explanation": "Closure means an operation always produces a result in the same set; some integer divisions give decimals/fractions.",
    }


g_understand_division_closure.topic = "Division of Integers and its Properties"


# --------------------------------------------------------------------------
# Application Based
# --------------------------------------------------------------------------
def g_app_addsub(rng):
    a, b, c = (rng.randint(-15, 15) for _ in range(3))
    correct = a + b - c
    return {
        "type": "numeric",
        "topic": "Addition and Subtraction of Integers",
        "question": f"Evaluate, showing your steps: {_s(a)} + {_s(b)} - {_s(c)}",
        "options": [],
        "correct_answer": str(correct),
        "max_marks": 1,
        "explanation": f"{_s(a)}+{_s(b)} = {a + b}. Then {a + b} - {_s(c)} = {correct}.",
    }


g_app_addsub.topic = "Addition and Subtraction of Integers"


def g_app_bodmas(rng):
    a = rng.randint(2, 9)
    b = _nz(rng, -9, 9)
    c = rng.randint(2, 9)
    e = rng.choice([2, 3, 4])
    f = e * rng.randint(-5, 5)
    term2 = b * c
    term3 = f // e
    correct = a - term2 + term3
    return {
        "type": "numeric",
        "topic": "Simplification of Expressions (BODMAS) and Real-life Applications",
        "question": f"Simplify using BODMAS, showing each step: {a} - {_s(b)} x {c} + {_s(f)} / {e}",
        "options": [],
        "correct_answer": str(correct),
        "max_marks": 2,
        "explanation": (
            f"First do x and /: {_s(b)} x {c} = {term2}, and {_s(f)} / {e} = {term3}. "
            f"Then {a} - ({term2}) + ({term3}) = {correct}."
        ),
    }


g_app_bodmas.topic = "Simplification of Expressions (BODMAS) and Real-life Applications"


# --------------------------------------------------------------------------
# Critical Thinking
# --------------------------------------------------------------------------
def g_critical_property_id(rng):
    a, b, c = (rng.randint(-9, 9) or 1 for _ in range(3))
    kind = rng.choice(["commutative", "associative", "distributive"])
    if kind == "commutative":
        question = f"Which property of integers is illustrated by: {_s(a)} x {_s(b)} = {_s(b)} x {_s(a)}?"
        correct = "Commutative property"
    elif kind == "associative":
        question = f"Which property of integers is illustrated by: ({_s(a)} x {_s(b)}) x {_s(c)} = {_s(a)} x ({_s(b)} x {_s(c)})?"
        correct = "Associative property"
    else:
        question = f"Which property of integers is illustrated by: {_s(a)} x ({_s(b)} + {_s(c)}) = {_s(a)} x {_s(b)} + {_s(a)} x {_s(c)}?"
        correct = "Distributive property"
    return {
        "type": "mcq",
        "topic": "Multiplication of Integers and its Properties",
        "question": question,
        "options": ["Commutative property", "Associative property", "Distributive property", "Closure property"],
        "correct_answer": correct,
        "max_marks": 1,
        "explanation": "Look for what changed: only the ORDER (commutative), only the GROUPING/brackets (associative), or a sum being 'shared out' by multiplication (distributive).",
    }


g_critical_property_id.topic = "Multiplication of Integers and its Properties"


def g_critical_division_order(rng):
    a = rng.randint(10, 24)
    b = rng.randint(2, 6)
    return {
        "type": "short",
        "topic": "Division of Integers and its Properties",
        "question": (
            f"A student claims that {a} / {_s(-b)} gives the same result as "
            f"{_s(-b)} / {a}. Check this claim by calculating both, and state whether "
            "division of integers is commutative."
        ),
        "options": [],
        "correct_answer": (
            f"{a} / {_s(-b)} = {-(a // b) if a % b == 0 else round(a / -b, 2)}, but "
            f"{_s(-b)} / {a} = {round(-b / a, 2)}. These are different, so division of "
            "integers is NOT commutative."
        ),
        "max_marks": 2,
        "explanation": "Commutativity would require a/b = b/a for all values, which does not hold for division.",
    }


g_critical_division_order.topic = "Division of Integers and its Properties"


# --------------------------------------------------------------------------
# Higher Order Thinking Skills (HOTS)
# --------------------------------------------------------------------------
def g_hots_temperature(rng):
    start = rng.randint(-10, 5)
    rate = rng.randint(2, 5)
    hours = rng.randint(3, 6)
    correct = start + rate * hours
    return {
        "type": "numeric",
        "topic": "Simplification of Expressions (BODMAS) and Real-life Applications",
        "question": (
            f"The temperature at sunrise was {start} degrees C. It rose by {rate} "
            f"degrees C every hour for the next {hours} hours. What was the "
            f"temperature after {hours} hours? Show your working."
        ),
        "options": [],
        "correct_answer": str(correct),
        "max_marks": 2,
        "explanation": f"Total rise = {hours} x {rate} = {rate * hours}. Final temperature = {start} + {rate * hours} = {correct}.",
    }


g_hots_temperature.topic = "Simplification of Expressions (BODMAS) and Real-life Applications"


def g_hots_submarine(rng):
    depth = rng.randint(300, 600)
    rise = rng.randint(50, 200)
    dive = rng.randint(50, 250)
    correct = -depth + rise - dive
    position = (
        f"{abs(correct)} m below sea level" if correct < 0
        else (f"{correct} m above sea level" if correct > 0 else "exactly at sea level")
    )
    return {
        "type": "long",
        "topic": "Addition and Subtraction of Integers",
        "question": (
            f"A submarine was at a depth of {depth} m below sea level. It rose {rise} "
            f"m, then dived another {dive} m. Show each step of the calculation and "
            "state the submarine's final position relative to sea level."
        ),
        "options": [],
        "correct_answer": (
            f"Start: -{depth} m. After rising {rise} m: -{depth}+{rise} = {-depth + rise} m. "
            f"After diving {dive} m more: {-depth + rise} - {dive} = {correct} m. "
            f"Final position: {position}."
        ),
        "max_marks": 3,
        "explanation": "Below sea level is negative; rising is +, diving is -. Add the changes step by step.",
    }


g_hots_submarine.topic = "Addition and Subtraction of Integers"


# --------------------------------------------------------------------------
# Mental Ability / Reasoning
# --------------------------------------------------------------------------
def g_mental_pattern(rng):
    start = rng.randint(-10, 10)
    step = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5])
    seq = [start + step * i for i in range(5)]
    missing_idx = rng.randint(1, 3)
    correct = seq[missing_idx]
    display = [str(x) if i != missing_idx else "___" for i, x in enumerate(seq)]
    options = {str(correct), str(correct + step), str(correct - step), str(correct + (2 if step > 0 else -2))}
    options = list(options)[:4]
    while len(options) < 4:
        candidate = str(correct + rng.randint(-9, 9))
        if candidate not in options:
            options.append(candidate)
    rng.shuffle(options)
    return {
        "type": "mcq",
        "topic": "Properties of Addition and Subtraction of Integers",
        "question": f"Find the missing number in the pattern: {', '.join(display)}",
        "options": options,
        "correct_answer": str(correct),
        "max_marks": 1,
        "explanation": f"Each term {'increases' if step > 0 else 'decreases'} by {abs(step)}.",
    }


g_mental_pattern.topic = "Properties of Addition and Subtraction of Integers"


def g_mental_negatives_count(rng):
    n_negatives = rng.choice([1, 2, 3, 4])
    n_positives = rng.choice([1, 2])
    factors = [-rng.randint(1, 5) for _ in range(n_negatives)] + [rng.randint(1, 5) for _ in range(n_positives)]
    rng.shuffle(factors)
    product = 1
    for f in factors:
        product *= f
    expr = " x ".join(_s(f) for f in factors)
    parity = "even" if n_negatives % 2 == 0 else "odd"
    sign = "positive" if n_negatives % 2 == 0 else "negative"
    return {
        "type": "numeric",
        "topic": "Multiplication of Integers and its Properties",
        "question": f"Find the value of: {expr}",
        "options": [],
        "correct_answer": str(product),
        "max_marks": 1,
        "explanation": f"Count the negative signs ({n_negatives}). An {parity} number of negatives means the product is {sign}.",
    }


g_mental_negatives_count.topic = "Multiplication of Integers and its Properties"


# --------------------------------------------------------------------------
# Case Study Based
# --------------------------------------------------------------------------
def g_case_profit_loss(rng):
    names = ["Meera", "Riya", "Arjun", "Kabir", "Sara"]
    name = rng.choice(names)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    values = [rng.choice([1, -1]) * rng.randint(20, 150) for _ in range(5)]
    total5 = sum(values)
    extra_days = rng.randint(2, 3)
    extra_value = rng.choice([1, -1]) * rng.randint(20, 80)
    new_total = total5 + extra_days * extra_value
    desc = "; ".join(f"{d}: {v:+d}" for d, v in zip(days, values))
    if new_total > 0:
        outcome = f"a profit of Rs {new_total}"
    elif new_total < 0:
        outcome = f"a loss of Rs {abs(new_total)}"
    else:
        outcome = "neither profit nor loss (break-even)"
    return {
        "type": "long",
        "topic": "Multiplication of Integers and its Properties",
        "question": (
            f"Case Study: {name} runs a small stall. Over 5 days, the daily "
            f"profit/loss (in Rs) was — {desc}.\n"
            f"(a) Find the total profit or loss for these 5 days.\n"
            f"(b) On the next {extra_days} days, {name} had the same result of "
            f"{extra_value:+d} each day. Find the new total including these days.\n"
            f"(c) Was {name} overall in profit or loss after all these days? Show all working."
        ),
        "options": [],
        "correct_answer": (
            f"(a) Total for 5 days = {' + '.join(str(v) for v in values)} = {total5}. "
            f"(b) {extra_days} days of {extra_value:+d} = {extra_days} x ({extra_value}) "
            f"= {extra_days * extra_value}. New total = {total5} + ({extra_days * extra_value}) "
            f"= {new_total}. (c) Since the total is {new_total}, {name} is overall in {outcome}."
        ),
        "max_marks": 4,
        "explanation": "Add all the signed values for the running total; multiplication helps with repeated equal amounts; the sign of the final total tells profit (+) or loss (-).",
    }


g_case_profit_loss.topic = "Multiplication of Integers and its Properties"


# --------------------------------------------------------------------------
# Competency Based
# --------------------------------------------------------------------------
def g_competency_floors(rng):
    names = ["Aryan", "Diya", "Vihaan", "Anaya", "Ishaan"]
    name = rng.choice(names)
    start = rng.randint(0, 5)
    move1 = _nz(rng, -6, 6)
    move2 = _nz(rng, -4, 4)
    final = start + move1 + move2
    if final > 0:
        location = f"floor {final} (above ground)"
    elif final < 0:
        location = f"basement floor {abs(final)} (below ground)"
    else:
        location = "the ground floor"
    return {
        "type": "short",
        "topic": "Addition and Subtraction of Integers",
        "question": (
            f"In a building, the ground floor is numbered 0, floors above ground are "
            f"positive and basement floors below ground are negative. {name} starts "
            f"at floor {start}, takes a lift {'up' if move1 > 0 else 'down'} "
            f"{abs(move1)} floor(s), then {'up' if move2 > 0 else 'down'} "
            f"{abs(move2)} floor(s). Which floor does {name} end up on? State whether "
            "it is above or below ground."
        ),
        "options": [],
        "correct_answer": (
            f"{start} {'+' if move1 >= 0 else '-'} {abs(move1)} {'+' if move2 >= 0 else '-'} "
            f"{abs(move2)} = {final}. {name} ends up on {location}."
        ),
        "max_marks": 2,
        "explanation": "Represent downward movement as negative and upward as positive, then add step by step.",
    }


g_competency_floors.topic = "Addition and Subtraction of Integers"


# --------------------------------------------------------------------------
# Assertion-Reasoning / Source / Value Based
# --------------------------------------------------------------------------
_AR_OPTIONS = [
    "Both A and R are true, and R is the correct explanation of A.",
    "Both A and R are true, but R is NOT the correct explanation of A.",
    "A is true, but R is false.",
    "A is false, but R is true.",
]

_AR_TEMPLATES = [
    {
        "a": "The product of two negative integers is always positive.",
        "r": "Multiplication of integers is distributive over addition.",
        "correct": _AR_OPTIONS[1],
    },
    {
        "a": "Division of integers is always closed, i.e. the result of dividing two integers is always an integer.",
        "r": "7 divided by 2 equals 3.5, which is not an integer.",
        "correct": _AR_OPTIONS[3],
    },
]


def g_assertion_reasoning(rng):
    t = rng.choice(_AR_TEMPLATES)
    return {
        "type": "mcq",
        "topic": "Properties of Addition and Subtraction of Integers",
        "question": (
            f"Assertion (A): {t['a']} Reason (R): {t['r']} Choose the correct option:"
        ),
        "options": list(_AR_OPTIONS),
        "correct_answer": t["correct"],
        "max_marks": 1,
        "explanation": "Check whether A and R are each true on their own, and then whether R actually EXPLAINS why A is true.",
    }


g_assertion_reasoning.topic = "Properties of Addition and Subtraction of Integers"


# --------------------------------------------------------------------------
# Creative & Open-Ended
# --------------------------------------------------------------------------
def g_creative_word_problem(rng):
    theme = rng.choice([
        "money (profit and loss)",
        "temperature (rise and fall)",
        "height (above and below sea level)",
        "floors of a building (above and below ground)",
    ])
    return {
        "type": "long",
        "topic": "Addition and Subtraction of Integers",
        "question": (
            f"Create your own real-life word problem about {theme} that uses addition "
            "and/or subtraction of integers, where at least one number involved is "
            "negative. Then solve your problem, showing your working."
        ),
        "options": [],
        "correct_answer": (
            "Open-ended — any well-formed real-life problem matching the chosen theme, "
            "involving at least one negative integer, with a correct step-by-step "
            "solution, should be awarded full marks. Look for: a clear scenario, "
            "correct use of positive/negative numbers to represent opposite "
            "situations, and an accurate final calculation."
        ),
        "max_marks": 3,
        "explanation": "This checks whether the student can apply integer addition/subtraction creatively to a context of their choosing, and solve their own problem correctly.",
    }


g_creative_word_problem.topic = "Addition and Subtraction of Integers"


def g_creative_expression(rng):
    return {
        "type": "long",
        "topic": "Simplification of Expressions (BODMAS) and Real-life Applications",
        "question": (
            "Write your own expression using all four operations (+, -, x, /) and at "
            "least two negative numbers and at least one pair of brackets. Then "
            "simplify it step by step using BODMAS, clearly showing each step."
        ),
        "options": [],
        "correct_answer": (
            "Open-ended — any valid expression meeting the requirements (all four "
            "operations, at least two negative numbers, at least one bracket pair), "
            "simplified correctly step by step following BODMAS, should be awarded "
            "full marks."
        ),
        "max_marks": 3,
        "explanation": "This checks whether the student understands BODMAS well enough to construct and correctly solve their own multi-step problem.",
    }


g_creative_expression.topic = "Simplification of Expressions (BODMAS) and Real-life Applications"


# --------------------------------------------------------------------------
# Registry + generation
# --------------------------------------------------------------------------
GENERATORS = {
    "Knowledge": [g_knowledge_identity, g_knowledge_sign_rule],
    "Understanding & Comprehension": [g_understand_sub_commute, g_understand_division_closure],
    "Application Based": [g_app_addsub, g_app_bodmas],
    "Critical Thinking": [g_critical_property_id, g_critical_division_order],
    "Higher Order Thinking Skills (HOTS)": [g_hots_temperature, g_hots_submarine],
    "Mental Ability / Reasoning": [g_mental_pattern, g_mental_negatives_count],
    "Case Study Based": [g_case_profit_loss],
    "Competency Based": [g_competency_floors],
    "Assertion-Reasoning / Source / Value Based": [g_assertion_reasoning],
    "Creative & Open-Ended": [g_creative_word_problem, g_creative_expression],
}

# Chapters for which `GENERATORS` above has templates. Match is done by
# normalized chapter name containing one of these keywords.
SUPPORTED_CHAPTERS = ["integer"]


def chapter_supported(chapter_name):
    name = (chapter_name or "").lower()
    return any(k in name for k in SUPPORTED_CHAPTERS)


def generate_offline_paper(chapter_name, num_questions, skill_category_weights=None,
                            focus_topics=None, title=None, seed=None):
    """Build a fresh, randomized practice paper from the local template bank.

    `focus_topics`, if given, is a list of topic names — generators whose
    topic is in that list are preferred for each skill category, so the
    paper leans towards the student's weak areas.
    """
    weights = skill_category_weights or SKILL_CATEGORIES
    counts = distribute_questions(num_questions, weights)
    rng = random.Random(seed)

    questions = []
    for cat, n in counts.items():
        gens = GENERATORS.get(cat)
        if not gens:
            continue
        for _ in range(n):
            candidates = gens
            if focus_topics:
                matching = [g for g in gens if getattr(g, "topic", None) in focus_topics]
                if matching:
                    candidates = matching
            gen = rng.choice(candidates)
            q = gen(rng)
            q.setdefault("options", [])
            q["skill_category"] = cat
            questions.append(q)

    rng.shuffle(questions)
    for i, q in enumerate(questions):
        q["q_index"] = i

    return {
        "title": title or f"{chapter_name} — Practice Paper (offline)",
        "questions": questions,
    }
