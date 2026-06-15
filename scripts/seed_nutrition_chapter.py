"""One-off seed script: loads 'Chapter 1 - Nutrition in Plants' (Science,
Class 7) content — analysis, a rich lesson (with deep-dives and interactive
quick-checks), and a practice paper.

This gives the app a second fully-worked example chapter (alongside Maths
'Integers'), so the multi-subject / multi-grade flow can be demonstrated
end-to-end without depending on the AI (useful when the OpenAI quota is
exhausted).

Run with:
    ./venv/bin/python scripts/seed_nutrition_chapter.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import db

SUBJECT = "Science"
CHAPTER_NAME = "Chapter 1 - Nutrition in Plants"
SOURCE_FILE = "hand-authored"
GRADE = 7

TOPICS = [
    "Modes of Nutrition: Autotrophic and Heterotrophic",
    "Photosynthesis — How Plants Make Their Own Food",
    "Other Modes of Nutrition: Parasites, Saprotrophs and Insectivorous Plants",
    "Symbiotic Relationships",
    "How Plants Get Nutrients from Soil and How Soil is Replenished",
]

ANALYSIS = {
    "topics": TOPICS,
    "summary": (
        "This chapter explains how living things, especially plants, obtain "
        "and use food (nutrition). It introduces the two big modes of "
        "nutrition — autotrophic (organisms that make their own food, like "
        "green plants) and heterotrophic (organisms that depend on others for "
        "food, like animals, fungi and some plants). The chapter explains "
        "photosynthesis in detail: the raw materials (carbon dioxide, water), "
        "the role of sunlight and chlorophyll, and the products (glucose and "
        "oxygen). It then covers special cases — parasitic plants (e.g. "
        "Cuscuta), saprotrophs (e.g. fungi feeding on dead matter) and "
        "insectivorous plants (e.g. pitcher plant) that supplement their diet "
        "in unusual ways. It explains symbiosis — a relationship where two "
        "different organisms benefit from living together, such as lichens "
        "(algae + fungi) and Rhizobium bacteria in the root nodules of legume "
        "plants (nitrogen fixation). Finally, it covers how plants absorb "
        "water and minerals from soil through roots, and how nutrients removed "
        "from soil by crops are replenished — naturally (decomposition, "
        "nitrogen fixation) and artificially (fertilisers, manure, crop "
        "rotation)."
    ),
    "sample_question_styles": [
        "Define / identify terms (autotroph, heterotroph, photosynthesis, "
        "saprotroph, parasite, symbiosis)",
        "Fill in the blanks describing the process or equation of photosynthesis",
        "Match organisms to their mode of nutrition",
        "Short-answer 'explain why/how' questions (e.g. why Cuscuta has no "
        "leaves, why pitcher plants trap insects)",
        "Diagram-based / labelling style questions described in words",
        "Case-study and application questions about farming, fertilisers, "
        "and soil health",
    ],
    "difficulty": "medium",
}

LESSON = {
    "topics": [
        {
            "topic": "Modes of Nutrition: Autotrophic and Heterotrophic",
            "explanation": (
                "Every living thing needs food for energy, growth and repair — but not "
                "every living thing GETS its food the same way. There are two big "
                "categories, and the easiest way to remember them is to think about "
                "where the 'cooking' happens.\n\n"
                "AUTOTROPHS ('auto' = self, 'troph' = nourishment) are organisms that "
                "make their OWN food. Green plants are the best example — they use "
                "sunlight, water, carbon dioxide and a green pigment called chlorophyll "
                "to literally COOK their own food inside their leaves, through a process "
                "called photosynthesis. Think of a plant as having its own kitchen built "
                "into every green leaf!\n\n"
                "HETEROTROPHS ('hetero' = other) CANNOT make their own food — they must "
                "eat or absorb food made by other organisms. This includes ALL animals "
                "(including us!), fungi (like mushrooms and bread mould), and even some "
                "unusual plants that have lost the ability to photosynthesise properly. "
                "Think of heterotrophs as people who don't cook — they always order food "
                "from someone else's kitchen.\n\n"
                "A simple test: if an organism is green and stays in one place making "
                "food from sunlight, it's almost certainly autotrophic. If it moves "
                "around looking for food, or grows on/in another living or dead thing to "
                "get nutrients, it's heterotrophic."
            ),
            "worked_examples": [
                "A mango tree: green leaves, fixed in one place, makes food using "
                "sunlight -> AUTOTROPH (photosynthesis).",
                "A goat eating grass: cannot make its own food, depends on the grass "
                "(which was made by an autotroph) -> HETEROTROPH.",
                "A mushroom growing on a dead log: has no chlorophyll, absorbs nutrients "
                "from the dead wood -> HETEROTROPH (specifically a saprotroph — "
                "'feeds on dead matter').",
                "Cuscuta (a yellow, thread-like climbing plant with no leaves): even "
                "though it's a 'plant', it has no chlorophyll and wraps around other "
                "plants to suck out their food -> HETEROTROPH (specifically a parasite).",
            ],
            "common_mistakes": [
                "Thinking that ALL plants are autotrophic. A few unusual plants (like "
                "Cuscuta) have lost their chlorophyll and become heterotrophic parasites "
                "— 'plant' and 'autotroph' are NOT exactly the same group.",
                "Confusing 'autotroph' with 'producer' vs 'heterotroph' with 'consumer' "
                "and then forgetting decomposers (fungi, some bacteria) are ALSO "
                "heterotrophs, even though they don't 'eat' in the usual sense.",
                "Writing 'auto' as meaning 'automatic' instead of 'self' — remembering "
                "the Greek root (auto = self, troph = nourish/food) makes the whole "
                "chapter's vocabulary much easier.",
            ],
            "quick_check": [
                {
                    "question": "An organism that makes its own food using sunlight, water and carbon dioxide is called a/an:",
                    "options": ["Autotroph", "Heterotroph", "Parasite", "Saprotroph"],
                    "answer": "Autotroph",
                    "hint": "Break the word into parts: 'auto' means self, 'troph' means food/nourishment.",
                    "explanation": (
                        "Step 1: 'Auto' means 'self' and 'troph' relates to nourishment, "
                        "so 'autotroph' literally means 'self-nourishing'. "
                        "Step 2: Organisms that make their own food (like green plants, "
                        "using sunlight, water and CO2) fit this definition exactly. "
                        "Final answer: Autotroph."
                    ),
                },
                {
                    "question": "Which of these is a HETEROTROPH?",
                    "options": ["A rose plant", "A goat", "Grass", "A neem tree"],
                    "answer": "A goat",
                    "hint": "Which of these organisms cannot make its own food and must eat other living things?",
                    "explanation": (
                        "Step 1: Rose plant, grass, and neem tree are all green plants "
                        "with chlorophyll — they make their own food (autotrophs). "
                        "Step 2: A goat has no chlorophyll and must eat plants to get "
                        "food — it is a heterotroph. Final answer: A goat."
                    ),
                },
                {
                    "question": "Cuscuta is unusual because, even though it is a plant, it is:",
                    "options": [
                        "Autotrophic, like all plants",
                        "Heterotrophic — it has no chlorophyll and depends on other plants",
                        "Able to photosynthesise faster than normal plants",
                        "Found only underwater",
                    ],
                    "answer": "Heterotrophic — it has no chlorophyll and depends on other plants",
                    "hint": "Think about what Cuscuta looks like — does it have green leaves?",
                    "explanation": (
                        "Step 1: Cuscuta is a thin, yellow/orange, thread-like climbing "
                        "plant with no leaves and no chlorophyll. "
                        "Step 2: Without chlorophyll, it cannot photosynthesise, so it "
                        "wraps around a host plant and absorbs ready-made food from it. "
                        "Step 3: This makes it heterotrophic — specifically a parasite. "
                        "Final answer: Heterotrophic — it has no chlorophyll and depends "
                        "on other plants."
                    ),
                },
                {
                    "question": "Which statement correctly describes the relationship between autotrophs and heterotrophs in nature?",
                    "options": [
                        "Heterotrophs make food for autotrophs",
                        "Autotrophs ultimately provide the food that heterotrophs depend on",
                        "Both make their own food independently",
                        "Neither needs the other",
                    ],
                    "answer": "Autotrophs ultimately provide the food that heterotrophs depend on",
                    "hint": "Trace the food back to its original source — where did the goat's grass get ITS food from?",
                    "explanation": (
                        "Step 1: Heterotrophs (like goats, humans, fungi) cannot make "
                        "their own food. "
                        "Step 2: They get food by eating plants (or other animals that "
                        "ate plants), or by absorbing nutrients from dead plant/animal "
                        "matter. "
                        "Step 3: Tracing this chain back, the food always originated "
                        "from an autotroph's photosynthesis. Final answer: Autotrophs "
                        "ultimately provide the food that heterotrophs depend on."
                    ),
                },
            ],
            "deep_dive": {
                "explanation": (
                    "Still mixing up autotroph vs heterotroph? Try sorting EVERY living "
                    "thing you can think of into just two buckets using ONE question: "
                    "'Does this organism have chlorophyll AND make its own food using "
                    "sunlight?' If YES -> autotroph bucket. If NO (it must get food from "
                    "somewhere/something else) -> heterotroph bucket. Within the "
                    "heterotroph bucket, you can further sort by HOW they get food: "
                    "eating other organisms (most animals), absorbing from dead matter "
                    "(saprotrophs like fungi), or stealing from a living host (parasites "
                    "like Cuscuta)."
                ),
                "extra_examples": [
                    "Algae in a pond: green, makes own food via photosynthesis -> "
                    "autotroph (even though it looks like a simple green slime, not a "
                    "'plant' in the usual sense).",
                    "Bread mould (a fungus): grows on old bread, has no chlorophyll, "
                    "absorbs nutrients from the bread -> heterotroph (saprotroph).",
                    "A tapeworm living inside an animal's intestine: absorbs digested "
                    "food directly from its host -> heterotroph (parasite) — note this "
                    "is the SAME strategy as Cuscuta, just in an animal instead of a "
                    "plant.",
                ],
            },
        },
        {
            "topic": "Photosynthesis — How Plants Make Their Own Food",
            "explanation": (
                "Photosynthesis is the process by which green plants make their own "
                "food. The word itself is a big clue: 'photo' means LIGHT, and "
                "'synthesis' means MAKING/PUTTING TOGETHER — so photosynthesis literally "
                "means 'making (food) using light'.\n\n"
                "Think of a leaf as a tiny solar-powered FOOD FACTORY. To run, every "
                "factory needs (1) raw materials, (2) an energy source, and (3) a "
                "machine that does the work. In a leaf:\n"
                "- RAW MATERIALS: carbon dioxide (CO2) from the air (entering through "
                "tiny pores called stomata) and water (H2O) absorbed by the roots and "
                "carried up to the leaves.\n"
                "- ENERGY SOURCE: sunlight.\n"
                "- THE MACHINE: chlorophyll, the green pigment inside cell structures "
                "called chloroplasts. Chlorophyll's job is to TRAP/ABSORB sunlight "
                "energy — this is exactly why leaves look green (chlorophyll reflects "
                "green light while absorbing red and blue light for energy).\n\n"
                "Using the trapped light energy, the factory combines CO2 + H2O to "
                "produce GLUCOSE (a sugar — the plant's food, used for energy and to "
                "build new cells) and OXYGEN (O2) as a 'waste product' that is released "
                "into the air through the stomata — this is the oxygen WE breathe!\n\n"
                "The word equation to remember is:\n"
                "Carbon dioxide + Water --(sunlight + chlorophyll)--> Glucose + Oxygen\n\n"
                "Plants don't use up all the glucose immediately — extra glucose is "
                "stored as STARCH, often in roots, stems, fruits or seeds (this is why "
                "potatoes, rice and wheat are starchy — they're the plant's food "
                "stores!)."
            ),
            "worked_examples": [
                "A potted plant kept in a dark cupboard for 3 days, then tested for "
                "starch in its leaves, shows NO starch -> without light, no "
                "photosynthesis happened, so no glucose was made or stored.",
                "A water plant (like Hydrilla) placed under a funnel in sunlight "
                "releases gas bubbles that collect at the top -> these bubbles are "
                "oxygen, a product of photosynthesis, proving photosynthesis is "
                "happening.",
                "A variegated leaf (part green, part white) tested for starch shows "
                "starch ONLY in the green parts -> proving chlorophyll (only in green "
                "parts) is essential for photosynthesis to occur.",
                "If you cover part of a leaf with black paper for a day and then test "
                "the whole leaf for starch, ONLY the uncovered part shows starch -> "
                "proving sunlight is essential for photosynthesis.",
            ],
            "common_mistakes": [
                "Writing the equation backwards — remember REACTANTS (what goes IN: "
                "CO2 + water) are on the LEFT, and PRODUCTS (what comes OUT: glucose + "
                "oxygen) are on the RIGHT, with sunlight and chlorophyll written ABOVE "
                "the arrow because they are CONDITIONS, not 'ingredients' that get used "
                "up.",
                "Saying plants 'breathe in oxygen and breathe out carbon dioxide' as "
                "their ONLY gas exchange. Plants DO respire (like all living things) and "
                "use a little oxygen for that — but during DAYTIME, photosynthesis "
                "(which takes in CO2 and releases O2) happens at a much larger rate, so "
                "the NET exchange is CO2 in, O2 out.",
                "Forgetting that water for photosynthesis is absorbed by the ROOTS (not "
                "the leaves) and transported upward through the stem — the leaves get "
                "CO2 directly from air through stomata, but water travels a longer "
                "journey from the soil.",
            ],
            "quick_check": [
                {
                    "question": "What are the two raw materials needed for photosynthesis?",
                    "options": [
                        "Oxygen and glucose",
                        "Carbon dioxide and water",
                        "Nitrogen and water",
                        "Glucose and sunlight",
                    ],
                    "answer": "Carbon dioxide and water",
                    "hint": "Think about what goes INTO the 'food factory' before sunlight and chlorophyll act on it.",
                    "explanation": (
                        "Step 1: Photosynthesis combines two simple substances to build "
                        "glucose. "
                        "Step 2: These are carbon dioxide (from air, via stomata) and "
                        "water (from soil, via roots). "
                        "Step 3: Oxygen and glucose are the PRODUCTS (outputs), not raw "
                        "materials. Final answer: Carbon dioxide and water."
                    ),
                },
                {
                    "question": "Why do leaves appear green?",
                    "options": [
                        "Because chlorophyll absorbs green light strongly",
                        "Because chlorophyll reflects green light while absorbing other colours",
                        "Because of the oxygen stored in leaves",
                        "Because green is the only colour present in sunlight",
                    ],
                    "answer": "Because chlorophyll reflects green light while absorbing other colours",
                    "hint": "Our eyes see the colour of light that BOUNCES OFF an object, not the colour it absorbs.",
                    "explanation": (
                        "Step 1: Sunlight contains many colours. "
                        "Step 2: Chlorophyll absorbs red and blue light to use as "
                        "energy for photosynthesis. "
                        "Step 3: It reflects green light back to our eyes, which is why "
                        "we SEE the leaf as green. Final answer: Because chlorophyll "
                        "reflects green light while absorbing other colours."
                    ),
                },
                {
                    "question": "A plant kept in complete darkness for several days will have leaves that test:",
                    "options": [
                        "Positive for starch (more than usual)",
                        "Negative for starch (little to no starch)",
                        "Positive for oxygen gas",
                        "The same as a plant kept in sunlight",
                    ],
                    "answer": "Negative for starch (little to no starch)",
                    "hint": "Starch is STORED glucose — and glucose is only made when photosynthesis happens.",
                    "explanation": (
                        "Step 1: Photosynthesis needs sunlight as its energy source. "
                        "Step 2: Without light, no glucose can be made, and any stored "
                        "starch gets used up over time for the plant's own respiration. "
                        "Step 3: So after several days in darkness, the leaves test "
                        "negative (or very low) for starch. Final answer: Negative for "
                        "starch (little to no starch)."
                    ),
                },
                {
                    "question": "The gas released as a 'by-product' of photosynthesis, which is essential for most living things, is:",
                    "options": ["Carbon dioxide", "Nitrogen", "Oxygen", "Hydrogen"],
                    "answer": "Oxygen",
                    "hint": "This is the gas humans and animals breathe in to survive.",
                    "explanation": (
                        "Step 1: During photosynthesis, water molecules are split apart "
                        "using light energy. "
                        "Step 2: The oxygen from water is released into the air through "
                        "stomata as a by-product. "
                        "Step 3: This oxygen is then used by humans, animals, and the "
                        "plant itself for respiration. Final answer: Oxygen."
                    ),
                },
            ],
            "deep_dive": {
                "explanation": (
                    "If the word equation feels abstract, picture a leaf as a kitchen "
                    "making lemonade: CO2 and water are like the lemon and sugar "
                    "(ingredients), sunlight is like the person's ENERGY to stir and "
                    "mix (it doesn't become part of the lemonade itself, but without it "
                    "nothing happens), and chlorophyll is like the JUG that makes "
                    "mixing possible. The RESULT (lemonade) is glucose, and the "
                    "'leftover ice cube wrapper' you throw away is oxygen — a "
                    "by-product nobody in the kitchen needed, but useful to someone "
                    "outside (us!)."
                ),
                "extra_examples": [
                    "Stomata are like tiny 'doors' on the underside of leaves — they "
                    "open to let CO2 in and O2/water vapour out, and can close to "
                    "prevent water loss when it's very hot or dry.",
                    "Chloroplasts are like 'mini solar panels + factories' inside each "
                    "leaf cell — they contain chlorophyll AND carry out the chemical "
                    "reactions of photosynthesis.",
                    "Glucose made today might be: used immediately for energy (the "
                    "plant 'eating now'), converted to starch and stored in roots/seeds "
                    "(the plant 'saving for later'), or used to build cellulose for new "
                    "cell walls (the plant 'growing').",
                ],
            },
        },
        {
            "topic": "Other Modes of Nutrition: Parasites, Saprotrophs and Insectivorous Plants",
            "explanation": (
                "Not every plant photosynthesises enough (or at all) to meet its needs "
                "— some plants have evolved clever 'side hustles' or even fully switched "
                "strategies to get extra nutrition. There are three special cases worth "
                "knowing well:\n\n"
                "1. PARASITIC PLANTS — these plants attach themselves to a HOST plant "
                "and absorb water, minerals and even ready-made food directly from it, "
                "usually harming the host in the process. The classic example is "
                "CUSCUTA (also called 'dodder' or 'amarbel') — a thin, leafless, "
                "yellowish climbing plant that wraps tightly around a host plant's stem "
                "and sends root-like structures (called haustoria) INTO the host's "
                "tissue to drain its nutrients. Since Cuscuta has no chlorophyll and no "
                "real leaves, it is COMPLETELY dependent on its host.\n\n"
                "2. SAPROTROPHS (or saprophytes) — these organisms feed on DEAD and "
                "DECAYING organic matter (dead plants, animals, fallen leaves) by "
                "secreting digestive substances onto the dead matter and then absorbing "
                "the broken-down nutrients. Common examples are FUNGI like mushrooms, "
                "bread mould, and yeast. Saprotrophs are nature's RECYCLERS — they break "
                "down dead material and return nutrients to the soil, which plants can "
                "then reuse.\n\n"
                "3. INSECTIVOROUS (or carnivorous) PLANTS — these are GREEN plants that "
                "DO photosynthesise normally, but grow in nutrient-poor soil (often "
                "marshy or boggy areas low in nitrogen) and supplement their diet by "
                "trapping and digesting small insects to get extra nitrogen and "
                "minerals. The PITCHER PLANT is the classic example — its leaves are "
                "modified into a jug/pitcher shape with slippery walls and digestive "
                "fluid at the bottom; insects fall in, can't climb out, and are slowly "
                "digested."
            ),
            "worked_examples": [
                "Cuscuta wrapped around a hibiscus plant, with the hibiscus looking "
                "weaker over time -> Cuscuta is a PARASITE, draining nutrients from its "
                "host (the hibiscus).",
                "A mushroom appearing on a rotting log in the rainy season -> a "
                "SAPROTROPH, absorbing nutrients from the dead wood as it decomposes.",
                "A pitcher plant in a marshy area, with its jug-shaped leaves trapping "
                "ants and small insects -> an INSECTIVOROUS plant — it photosynthesises "
                "AND digests insects for extra nitrogen.",
                "Bread turning fuzzy and green/black after being left out -> bread "
                "mould, a SAPROTROPHIC fungus, growing on the 'dead' organic matter "
                "(the bread).",
            ],
            "common_mistakes": [
                "Thinking insectivorous plants 'eat insects INSTEAD of "
                "photosynthesising'. They still photosynthesise normally for their main "
                "energy (glucose) — insects are an EXTRA source of nitrogen/minerals "
                "that their poor soil lacks, not a replacement for photosynthesis.",
                "Confusing 'parasite' (harms a LIVING host) with 'saprotroph' (feeds on "
                "DEAD matter, harms no living organism). Cuscuta harms a living "
                "hibiscus (parasite); a mushroom on a dead log harms nothing living "
                "(saprotroph).",
                "Assuming all fungi are 'bad' because some cause disease — most fungi "
                "are saprotrophic decomposers that are ESSENTIAL for recycling "
                "nutrients back into ecosystems.",
            ],
            "quick_check": [
                {
                    "question": "Cuscuta obtains its nutrition by:",
                    "options": [
                        "Photosynthesising like normal plants",
                        "Trapping and digesting insects",
                        "Attaching to a host plant and absorbing its nutrients",
                        "Absorbing nutrients from dead leaves on the ground",
                    ],
                    "answer": "Attaching to a host plant and absorbing its nutrients",
                    "hint": "Cuscuta has no leaves and no chlorophyll — so it cannot make its own food. What does it do instead?",
                    "explanation": (
                        "Step 1: Cuscuta has no chlorophyll, so it cannot "
                        "photosynthesise. "
                        "Step 2: It wraps around a living host plant and grows "
                        "haustoria (root-like structures) into the host's tissue. "
                        "Step 3: Through these haustoria, it absorbs water, minerals, "
                        "and ready-made food from the host. Final answer: Attaching to "
                        "a host plant and absorbing its nutrients (a parasite)."
                    ),
                },
                {
                    "question": "Mushrooms and bread mould get their nutrition by feeding on:",
                    "options": [
                        "Living host organisms only",
                        "Dead and decaying organic matter",
                        "Sunlight directly",
                        "Soil minerals only, like roots do",
                    ],
                    "answer": "Dead and decaying organic matter",
                    "hint": "These organisms are described as nature's 'recyclers' — what do recyclers work with?",
                    "explanation": (
                        "Step 1: Fungi like mushrooms and bread mould have no "
                        "chlorophyll. "
                        "Step 2: They secrete substances onto dead organic matter "
                        "(like old bread or a fallen log) to break it down. "
                        "Step 3: They then absorb the broken-down nutrients. This mode "
                        "of nutrition is called saprotrophic. Final answer: Dead and "
                        "decaying organic matter."
                    ),
                },
                {
                    "question": "Why does the pitcher plant trap and digest insects, even though it is green and can photosynthesise?",
                    "options": [
                        "It cannot photosynthesise at all and depends fully on insects",
                        "It grows in nitrogen-poor soil and needs extra nitrogen/minerals from insects",
                        "Insects help it absorb more sunlight",
                        "It traps insects only for protection from predators, not for food",
                    ],
                    "answer": "It grows in nitrogen-poor soil and needs extra nitrogen/minerals from insects",
                    "hint": "The pitcher plant photosynthesises fine for its energy needs — so what is it MISSING from its environment?",
                    "explanation": (
                        "Step 1: The pitcher plant has chlorophyll and photosynthesises "
                        "normally, like other green plants, for its energy (glucose). "
                        "Step 2: However, it grows in marshy/boggy soils that are very "
                        "low in nitrogen and other minerals. "
                        "Step 3: By digesting trapped insects, it gets the extra "
                        "nitrogen and minerals its soil cannot provide. Final answer: It "
                        "grows in nitrogen-poor soil and needs extra nitrogen/minerals "
                        "from insects."
                    ),
                },
                {
                    "question": "Which pair correctly matches the organism to its mode of nutrition?",
                    "options": [
                        "Cuscuta — Saprotroph",
                        "Mushroom — Parasite",
                        "Pitcher plant — Insectivorous (and autotrophic)",
                        "Mango tree — Heterotroph",
                    ],
                    "answer": "Pitcher plant — Insectivorous (and autotrophic)",
                    "hint": "Eliminate the obviously wrong pairs first — a mango tree definitely makes its own food.",
                    "explanation": (
                        "Step 1: Cuscuta is a PARASITE (not a saprotroph) — it feeds on "
                        "a living host. "
                        "Step 2: Mushroom is a SAPROTROPH (not a parasite) — it feeds "
                        "on dead matter. "
                        "Step 3: Mango tree is an AUTOTROPH (not a heterotroph) — it "
                        "photosynthesises. "
                        "Step 4: Pitcher plant photosynthesises (autotrophic) AND traps "
                        "insects for extra nutrients (insectivorous) — both labels "
                        "apply. Final answer: Pitcher plant — Insectivorous (and "
                        "autotrophic)."
                    ),
                },
            ],
            "deep_dive": {
                "explanation": (
                    "A handy way to keep these three apart is to ask: 'Is the source of "
                    "extra nutrients ALIVE, DEAD, or SMALL PREY?' If the plant is "
                    "stealing from something ALIVE -> parasite (Cuscuta). If it's "
                    "feeding on something DEAD -> saprotroph (mushroom, bread mould). "
                    "If it's a normal green plant that ALSO traps small living prey for "
                    "extra minerals -> insectivorous (pitcher plant). Notice only the "
                    "insectivorous plant is STILL an autotroph for its main energy — "
                    "the other two are heterotrophs in disguise."
                ),
                "extra_examples": [
                    "Venus flytrap: another insectivorous plant, with hinged leaves "
                    "that snap shut on insects — same reasoning as the pitcher plant "
                    "(extra nitrogen from poor soil).",
                    "Dodder vine on a hedge: you'll often see orange/yellow thread-like "
                    "tangles over garden hedges in some seasons — this is Cuscuta "
                    "acting as a parasite on the hedge plants.",
                    "Yeast used in bread-making: a saprotrophic fungus that feeds on "
                    "sugars in the dough — the bubbles that make bread rise are a "
                    "by-product of yeast 'feeding'.",
                ],
            },
        },
        {
            "topic": "Symbiotic Relationships",
            "explanation": (
                "So far we've seen organisms that either make their own food, steal "
                "from a living host (harming it), or feed on the dead. But sometimes, "
                "TWO DIFFERENT organisms live together in a way that BENEFITS BOTH of "
                "them — this is called SYMBIOSIS (from Greek: 'sym' = together, "
                "'biosis' = living). Think of it as a 'win-win partnership' in nature, "
                "like two classmates who are good at different subjects and help each "
                "other study so BOTH pass the exam.\n\n"
                "Two classic examples in this chapter:\n\n"
                "1. LICHENS — a lichen is actually TWO organisms living together as "
                "one: an ALGA (or cyanobacterium) and a FUNGUS. The alga is "
                "autotrophic — it photosynthesises and makes food (carbohydrates) for "
                "both partners. The fungus cannot make food, but it provides shelter, "
                "retains moisture, and absorbs minerals from the surface it grows on "
                "(rocks, tree bark), giving these minerals to the alga. Neither could "
                "survive as easily alone in such harsh places (bare rocks, tree trunks) "
                "— together, they thrive. Lichens often look like colourful crusty "
                "patches on rocks or tree bark.\n\n"
                "2. RHIZOBIUM IN ROOT NODULES OF LEGUME PLANTS — legume plants (like "
                "peas, beans, gram, and other pulses) have small swellings on their "
                "roots called ROOT NODULES. Inside these nodules live RHIZOBIUM "
                "bacteria. Rhizobium can take nitrogen gas (N2) from the air — which "
                "plants normally CANNOT use directly — and convert it into nitrogen "
                "compounds the plant CAN use (this is called NITROGEN FIXATION). In "
                "return, the legume plant supplies Rhizobium with food (made via "
                "photosynthesis) and a safe home inside the root nodules. This is why "
                "farmers often grow legumes to naturally improve soil nitrogen content."
            ),
            "worked_examples": [
                "A grey-green crusty patch growing on an old stone wall, which is "
                "neither fully plant nor fully fungus -> a LICHEN (alga + fungus "
                "symbiosis).",
                "Pea plant roots, when dug up, show small round swellings -> these are "
                "ROOT NODULES containing Rhizobium bacteria, which fix nitrogen from "
                "air for the plant.",
                "A farmer rotates crops, growing chickpeas (a legume) in a field one "
                "season before growing wheat the next -> this is a real-world "
                "application of Rhizobium's nitrogen-fixing symbiosis to naturally "
                "enrich the soil for the next crop.",
                "Comparing Cuscuta (parasite) and Rhizobium (symbiont): Cuscuta HARMS "
                "its host while benefiting itself; Rhizobium and the legume plant "
                "BOTH benefit -> the key difference between parasitism and symbiosis "
                "is whether BOTH partners gain or only one.",
            ],
            "common_mistakes": [
                "Confusing 'symbiosis' with 'parasitism'. In symbiosis, BOTH organisms "
                "benefit (win-win). In parasitism, only the parasite benefits and the "
                "host is harmed (win-lose). Always ask: 'does the SECOND organism gain "
                "something too?'",
                "Thinking a lichen is a single type of organism (e.g. 'a type of "
                "moss'). A lichen is actually TWO different organisms (an alga/"
                "cyanobacterium AND a fungus) living together as a partnership.",
                "Forgetting WHO does WHAT in the Rhizobium-legume relationship: "
                "Rhizobium fixes nitrogen FOR the plant; the plant gives Rhizobium "
                "food and shelter. Mixing up these roles is a common exam slip.",
            ],
            "quick_check": [
                {
                    "question": "Symbiosis is best described as a relationship where:",
                    "options": [
                        "One organism benefits while harming the other",
                        "One organism feeds on the dead remains of another",
                        "Both organisms living together benefit from each other",
                        "Two organisms compete for the same food source",
                    ],
                    "answer": "Both organisms living together benefit from each other",
                    "hint": "Break down the word: 'sym' = together, 'biosis' = living — and think 'win-win'.",
                    "explanation": (
                        "Step 1: 'Symbiosis' comes from Greek words meaning 'living "
                        "together'. "
                        "Step 2: In a true symbiotic relationship, BOTH partners gain "
                        "something they need (a 'win-win'), unlike parasitism where "
                        "only one side benefits. Final answer: Both organisms living "
                        "together benefit from each other."
                    ),
                },
                {
                    "question": "A lichen is made up of which two organisms living together?",
                    "options": [
                        "A plant and an insect",
                        "An alga (or cyanobacterium) and a fungus",
                        "Two different species of moss",
                        "Rhizobium and a legume root",
                    ],
                    "answer": "An alga (or cyanobacterium) and a fungus",
                    "hint": "One partner can photosynthesise; the other provides shelter and absorbs minerals.",
                    "explanation": (
                        "Step 1: A lichen is a partnership between an alga (or "
                        "cyanobacterium), which photosynthesises and makes food, and a "
                        "fungus, which provides shelter and moisture and absorbs "
                        "minerals. "
                        "Step 2: Together they can survive on bare rocks or tree bark "
                        "where neither could easily live alone. Final answer: An alga "
                        "(or cyanobacterium) and a fungus."
                    ),
                },
                {
                    "question": "Rhizobium bacteria live in the root nodules of legume plants and:",
                    "options": [
                        "Convert nitrogen gas from air into a usable form for the plant",
                        "Absorb sunlight on behalf of the plant",
                        "Protect the plant from insects by producing poison",
                        "Convert glucose into starch for storage",
                    ],
                    "answer": "Convert nitrogen gas from air into a usable form for the plant",
                    "hint": "This process has a special name involving the word 'nitrogen' and 'fixation'.",
                    "explanation": (
                        "Step 1: Plants cannot directly use nitrogen gas (N2) from the "
                        "air, even though air is about 78% nitrogen. "
                        "Step 2: Rhizobium bacteria in root nodules can convert (fix) "
                        "this nitrogen gas into compounds the plant CAN absorb and use. "
                        "Step 3: In return, the plant gives Rhizobium food and shelter. "
                        "Final answer: Convert nitrogen gas from air into a usable form "
                        "for the plant (nitrogen fixation)."
                    ),
                },
                {
                    "question": "How is the Rhizobium-legume relationship DIFFERENT from the Cuscuta-host relationship?",
                    "options": [
                        "There is no real difference — both harm one partner",
                        "In Rhizobium-legume, BOTH partners benefit; in Cuscuta-host, only Cuscuta benefits and the host is harmed",
                        "Rhizobium harms the legume, while Cuscuta helps its host",
                        "Cuscuta is a type of bacteria, like Rhizobium",
                    ],
                    "answer": "In Rhizobium-legume, BOTH partners benefit; in Cuscuta-host, only Cuscuta benefits and the host is harmed",
                    "hint": "Think 'win-win' vs 'win-lose'.",
                    "explanation": (
                        "Step 1: Rhizobium-legume is SYMBIOSIS: Rhizobium gets food and "
                        "shelter, the legume gets usable nitrogen — both gain (win-win). "
                        "Step 2: Cuscuta-host is PARASITISM: Cuscuta gets water, "
                        "minerals and food from the host, while the host is weakened "
                        "and gains nothing (win-lose). Final answer: In "
                        "Rhizobium-legume, BOTH partners benefit; in Cuscuta-host, only "
                        "Cuscuta benefits and the host is harmed."
                    ),
                },
            ],
            "deep_dive": {
                "explanation": (
                    "A useful 'relationship table' to memorise: PARASITISM = one "
                    "living host, one winner, one loser (Cuscuta + hibiscus). "
                    "SAPROTROPHY = no living victim, feeds on the dead (mushroom + dead "
                    "log). SYMBIOSIS = two living partners, BOTH winners (Rhizobium + "
                    "legume, or alga + fungus in a lichen). If you can place an "
                    "organism's relationship into one of these three boxes, you've "
                    "understood the core idea of this whole section."
                ),
                "extra_examples": [
                    "Mycorrhiza: a symbiotic fungus that wraps around plant roots, "
                    "helping the plant absorb more water and minerals, while the fungus "
                    "gets sugars from the plant — similar 'win-win' logic to Rhizobium, "
                    "but with a fungus instead of bacteria.",
                    "Termites and gut microbes: termites eat wood but cannot digest it "
                    "themselves — microbes living in their gut digest the wood for "
                    "them, and in return get a home and food supply — another "
                    "real-world symbiosis example.",
                    "Crop rotation with legumes: after harvesting a legume crop, "
                    "farmers often plough the leftover roots (with their nitrogen-rich "
                    "nodules) back into the soil — this is a direct, practical use of "
                    "the Rhizobium symbiosis to improve soil for the NEXT crop.",
                ],
            },
        },
        {
            "topic": "How Plants Get Nutrients from Soil and How Soil is Replenished",
            "explanation": (
                "Photosynthesis gives a plant ENERGY (glucose), but a plant also needs "
                "smaller amounts of other raw materials called MINERAL NUTRIENTS (such "
                "as nitrogen, phosphorus, potassium, and others) to build proteins, "
                "DNA, and other essential molecules — think of these like the "
                "'vitamins and supplements' a plant needs alongside its main meal.\n\n"
                "Plants absorb water AND dissolved mineral nutrients from the soil "
                "through their ROOTS, especially through tiny hair-like extensions "
                "called ROOT HAIRS, which massively increase the surface area for "
                "absorption (similar to how the small intestine in humans has folds to "
                "absorb more nutrients). This water-and-mineral mixture then travels "
                "UP through the stem to the leaves, where it's used in photosynthesis "
                "and other processes.\n\n"
                "Every time a crop is harvested, it takes some of these soil nutrients "
                "away with it (in the grains, fruits, or whatever is removed from the "
                "field) — over time, if nothing is done, the soil becomes 'tired' or "
                "DEPLETED of nutrients, and crop yields drop. Soil nutrients are "
                "replenished (refilled) in two main ways:\n\n"
                "NATURAL ways: (1) DECOMPOSITION — saprotrophs (fungi, bacteria) break "
                "down dead plants, animals and fallen leaves, releasing nutrients back "
                "into the soil (this is why composting works!). (2) NITROGEN FIXATION "
                "— as we saw with Rhizobium, certain bacteria convert nitrogen gas from "
                "air into soil-usable forms.\n\n"
                "ARTIFICIAL/human-driven ways: (1) MANURE — decomposed organic waste "
                "from animals/plants, added to soil; improves soil structure too. "
                "(2) FERTILISERS — chemically manufactured nutrient mixes (often "
                "labelled with N-P-K for Nitrogen-Phosphorus-Potassium) that quickly "
                "replace specific nutrients. (3) CROP ROTATION — alternating a "
                "nutrient-hungry crop (like wheat) with a legume crop (like gram) that "
                "naturally restores nitrogen via Rhizobium, instead of growing the same "
                "crop repeatedly."
            ),
            "worked_examples": [
                "A farmer notices crop yields dropping after growing wheat in the same "
                "field for many years without adding anything back -> the soil has "
                "become DEPLETED of nutrients that the wheat removed each season.",
                "Kitchen scraps and dry leaves placed in a compost pit, which turn into "
                "dark crumbly material after a few weeks -> DECOMPOSITION by "
                "saprotrophic fungi/bacteria, releasing nutrients back for plants to "
                "reuse (this dark material is compost/manure).",
                "A farmer grows chickpeas (a legume) one season, then wheat the next "
                "season, in the same field -> CROP ROTATION, using Rhizobium's "
                "nitrogen fixation in the chickpea season to naturally restore "
                "nitrogen for the wheat season.",
                "A bag of fertiliser labelled '10-26-26' (N-P-K ratio) added to soil "
                "before sowing -> an ARTIFICIAL method to quickly supply specific "
                "minerals (here, more phosphorus and potassium relative to nitrogen) "
                "that the soil may be lacking.",
            ],
            "common_mistakes": [
                "Thinking plants get ALL their 'food' from soil. Soil provides WATER "
                "and MINERAL NUTRIENTS (like vitamins/supplements) — the actual FOOD "
                "(glucose, providing energy) is made by the plant itself through "
                "photosynthesis using CO2, water and sunlight.",
                "Mixing up 'manure' and 'fertiliser'. Manure is natural/organic "
                "(decomposed plant/animal waste) and also improves soil structure over "
                "time. Fertiliser is usually a chemically manufactured product that "
                "supplies specific nutrients quickly but doesn't improve soil "
                "structure the same way.",
                "Forgetting WHY crop rotation with legumes works — it's not magic, "
                "it's because legumes host Rhizobium bacteria in root nodules, which "
                "fix atmospheric nitrogen into the soil, directly connecting this topic "
                "back to the symbiosis topic.",
            ],
            "quick_check": [
                {
                    "question": "Root hairs help a plant mainly by:",
                    "options": [
                        "Producing chlorophyll for photosynthesis",
                        "Increasing the surface area for absorbing water and minerals from soil",
                        "Trapping insects for extra nutrition",
                        "Releasing oxygen into the soil",
                    ],
                    "answer": "Increasing the surface area for absorbing water and minerals from soil",
                    "hint": "Think about why having MANY tiny hair-like extensions would help with absorption — more surface area means more contact with soil.",
                    "explanation": (
                        "Step 1: Root hairs are thin, hair-like extensions of root "
                        "cells. "
                        "Step 2: By increasing the total surface area in contact with "
                        "soil, they allow the plant to absorb much more water and "
                        "dissolved minerals than a smooth root surface could. Final "
                        "answer: Increasing the surface area for absorbing water and "
                        "minerals from soil."
                    ),
                },
                {
                    "question": "Which of these is a NATURAL way of replenishing soil nutrients?",
                    "options": [
                        "Spraying chemical fertiliser",
                        "Decomposition of dead plants and animals by saprotrophs",
                        "Removing all crop residue from the field",
                        "Growing the same crop every season without a break",
                    ],
                    "answer": "Decomposition of dead plants and animals by saprotrophs",
                    "hint": "Which option does NOT involve humans manufacturing or adding anything artificial?",
                    "explanation": (
                        "Step 1: Chemical fertiliser is an ARTIFICIAL/human-made "
                        "method. "
                        "Step 2: Removing crop residue or repeatedly growing the same "
                        "crop actually DEPLETES soil nutrients, it doesn't replenish "
                        "them. "
                        "Step 3: Decomposition is a NATURAL process where saprotrophs "
                        "break down dead organic matter and release nutrients back into "
                        "the soil. Final answer: Decomposition of dead plants and "
                        "animals by saprotrophs."
                    ),
                },
                {
                    "question": "Why might a farmer practise crop rotation by alternating wheat with a legume like gram?",
                    "options": [
                        "Legumes look better and attract more customers",
                        "Legumes host Rhizobium, which naturally restores nitrogen to the soil for the next crop",
                        "Wheat and gram cannot be grown in the same country",
                        "It has no effect on soil, it's just tradition",
                    ],
                    "answer": "Legumes host Rhizobium, which naturally restores nitrogen to the soil for the next crop",
                    "hint": "Connect this back to the previous topic — which bacteria live in legume root nodules, and what do they do?",
                    "explanation": (
                        "Step 1: Continuously growing wheat removes nitrogen from the "
                        "soil each season. "
                        "Step 2: Legume plants (gram, peas, etc.) have root nodules "
                        "containing Rhizobium bacteria, which fix nitrogen from the air "
                        "into the soil. "
                        "Step 3: Growing a legume between wheat crops naturally "
                        "restocks soil nitrogen, reducing the need for as much "
                        "artificial fertiliser. Final answer: Legumes host Rhizobium, "
                        "which naturally restores nitrogen to the soil for the next "
                        "crop."
                    ),
                },
                {
                    "question": "What is the key difference between MANURE and chemical FERTILISER?",
                    "options": [
                        "There is no difference, they are the same thing",
                        "Manure is decomposed organic matter that also improves soil structure; fertiliser is a manufactured nutrient supplement",
                        "Fertiliser is always better and manure should never be used",
                        "Manure contains no nutrients at all",
                    ],
                    "answer": "Manure is decomposed organic matter that also improves soil structure; fertiliser is a manufactured nutrient supplement",
                    "hint": "One of these is 'natural and organic', the other is 'manufactured and concentrated' — but both add nutrients.",
                    "explanation": (
                        "Step 1: Manure comes from decomposed plant/animal waste — it "
                        "adds nutrients gradually AND improves the soil's texture and "
                        "ability to hold water. "
                        "Step 2: Fertiliser is manufactured to deliver specific "
                        "nutrients (often N-P-K) quickly and in concentrated form, but "
                        "doesn't improve soil structure the way manure does. Final "
                        "answer: Manure is decomposed organic matter that also improves "
                        "soil structure; fertiliser is a manufactured nutrient "
                        "supplement."
                    ),
                },
            ],
            "deep_dive": {
                "explanation": (
                    "Connect ALL FIVE topics of this chapter into one story: A green "
                    "plant (AUTOTROPH) makes its food via PHOTOSYNTHESIS using sunlight, "
                    "CO2 and water — but it ALSO needs minerals from SOIL, absorbed "
                    "through root hairs. Some organisms can't make their own food, so "
                    "they steal from living hosts (PARASITES like Cuscuta) or feed on "
                    "the dead (SAPROTROPHS like fungi) — and saprotrophs, by "
                    "decomposing dead matter, actually help REPLENISH the soil minerals "
                    "the plant needs! Meanwhile, some plants form WIN-WIN partnerships "
                    "(SYMBIOSIS) — like Rhizobium fixing nitrogen for legumes — which is "
                    "ANOTHER way soil gets replenished. Everything in this chapter is "
                    "connected by the same big idea: nutrients cycle between living "
                    "things and their environment."
                ),
                "extra_examples": [
                    "Earthworms: while not covered in detail in this chapter, they help "
                    "decompose organic matter and improve soil aeration — another "
                    "natural helper for soil health, often mentioned alongside "
                    "decomposers.",
                    "A kitchen garden composting vegetable peels: combines "
                    "decomposition (saprotrophic fungi/bacteria break down peels) with "
                    "manure-making (the end compost is added back to soil) — a "
                    "small-scale version of what happens in farms.",
                    "Testing soil before sowing: farmers sometimes get soil tested to "
                    "see which nutrients (N, P, K) are low, then choose a fertiliser "
                    "or crop-rotation plan specifically to fix that deficiency — "
                    "applying this whole topic practically.",
                ],
            },
        },
    ]
}

PAPER_TITLE = "Nutrition in Plants — Practice Paper 1"

QUESTIONS = [
    {
        "type": "mcq",
        "topic": "Modes of Nutrition: Autotrophic and Heterotrophic",
        "skill_category": "Knowledge",
        "question": "Organisms that cannot make their own food and depend on other organisms for nutrition are called:",
        "options": ["Autotrophs", "Heterotrophs", "Producers", "Photosynthesisers"],
        "correct_answer": "Heterotrophs",
        "max_marks": 1,
        "explanation": "'Hetero' means 'other' — heterotrophs depend on other organisms for their food, unlike autotrophs which make their own.",
    },
    {
        "type": "mcq",
        "topic": "Photosynthesis — How Plants Make Their Own Food",
        "skill_category": "Knowledge",
        "question": "The green pigment in leaves that absorbs sunlight for photosynthesis is called:",
        "options": ["Chlorophyll", "Chloroplast", "Cellulose", "Glucose"],
        "correct_answer": "Chlorophyll",
        "max_marks": 1,
        "explanation": "Chlorophyll is the green pigment, found inside chloroplasts, that traps light energy for photosynthesis.",
    },
    {
        "type": "short",
        "topic": "Photosynthesis — How Plants Make Their Own Food",
        "skill_category": "Understanding & Comprehension",
        "question": "Write the word equation for photosynthesis, clearly showing the raw materials, products, and the conditions required.",
        "options": [],
        "correct_answer": "Carbon dioxide + Water --(in presence of sunlight and chlorophyll)--> Glucose + Oxygen",
        "max_marks": 2,
        "explanation": "Reactants (CO2 and water) are written on the left, products (glucose and oxygen) on the right, with sunlight and chlorophyll shown as the conditions above the arrow since they are not consumed as ingredients.",
    },
    {
        "type": "short",
        "topic": "Other Modes of Nutrition: Parasites, Saprotrophs and Insectivorous Plants",
        "skill_category": "Understanding & Comprehension",
        "question": "Explain why Cuscuta has no leaves and no chlorophyll, yet survives perfectly well.",
        "options": [],
        "correct_answer": "Cuscuta is a parasite — it wraps around a host plant and grows haustoria into the host's tissue to absorb water, minerals, and ready-made food directly from the host. Since it gets its food from the host, it does not need leaves or chlorophyll to photosynthesise.",
        "max_marks": 2,
        "explanation": "Because Cuscuta obtains ready-made nutrients from its host, it has lost the structures (leaves, chlorophyll) needed for photosynthesis through evolution.",
    },
    {
        "type": "numeric",
        "topic": "Symbiotic Relationships",
        "skill_category": "Application Based",
        "question": "A farmer's field of gram (a legume) has plants with root nodules. If each plant has 8 nodules and the field has 150 plants, how many root nodules are there in total?",
        "options": [],
        "correct_answer": "1200",
        "max_marks": 1,
        "explanation": "8 nodules per plant x 150 plants = 1200 root nodules in total. Each nodule houses Rhizobium bacteria that fix nitrogen for the plant.",
    },
    {
        "type": "short",
        "topic": "How Plants Get Nutrients from Soil and How Soil is Replenished",
        "skill_category": "Application Based",
        "question": "A farmer has been growing wheat in the same field every season for 10 years and notices the yield is decreasing. Suggest TWO different methods (one natural, one involving a change in farming practice) the farmer could use to restore the soil's fertility, and explain how each works.",
        "options": [],
        "correct_answer": "1) Add manure/compost — decomposed organic matter releases nutrients back into the soil naturally and improves soil structure. 2) Practise crop rotation by growing a legume (e.g. gram or peas) between wheat crops — Rhizobium bacteria in the legume's root nodules fix atmospheric nitrogen, restoring soil nitrogen for the next wheat crop.",
        "max_marks": 2,
        "explanation": "Both manure and legume-based crop rotation restore soil fertility, but through different mechanisms — decomposition releasing stored nutrients vs. nitrogen fixation adding new usable nitrogen.",
    },
    {
        "type": "mcq",
        "topic": "Other Modes of Nutrition: Parasites, Saprotrophs and Insectivorous Plants",
        "skill_category": "Critical Thinking",
        "question": "A student claims: 'The pitcher plant cannot photosynthesise — that's why it has to trap and eat insects, just like an animal.' Which statement best evaluates this claim?",
        "options": [
            "The claim is correct — pitcher plants are fully heterotrophic like animals",
            "The claim is incorrect — pitcher plants photosynthesise normally and trap insects only to get extra nitrogen/minerals from poor soil",
            "The claim is correct, but only for young pitcher plants",
            "The claim is irrelevant — pitcher plants don't really trap insects",
        ],
        "correct_answer": "The claim is incorrect — pitcher plants photosynthesise normally and trap insects only to get extra nitrogen/minerals from poor soil",
        "max_marks": 1,
        "explanation": "Pitcher plants are green and photosynthesise for their main energy needs; trapping insects is a supplementary strategy for getting nitrogen/minerals from nutrient-poor (often marshy) soils.",
    },
    {
        "type": "short",
        "topic": "Symbiotic Relationships",
        "skill_category": "Critical Thinking",
        "question": "A student says: 'Cuscuta and Rhizobium are both examples of two organisms living together, so both are examples of symbiosis.' Is the student correct? Justify your answer with reference to who benefits in each relationship.",
        "options": [],
        "correct_answer": "No, the student is incorrect. In symbiosis (e.g. Rhizobium-legume), BOTH organisms benefit. In the Cuscuta-host relationship, only Cuscuta benefits while the host plant is harmed (loses water, minerals, and food) — this is parasitism, not symbiosis. Simply living together is not enough; the key difference is whether both partners gain.",
        "max_marks": 2,
        "explanation": "This question tests whether students can distinguish symbiosis from parasitism based on mutual benefit vs one-sided benefit, not just physical closeness.",
    },
    {
        "type": "long",
        "topic": "Photosynthesis — How Plants Make Their Own Food",
        "skill_category": "Higher Order Thinking Skills (HOTS)",
        "question": "A student takes two identical potted plants, A and B. Plant A is kept in sunlight; Plant B is kept inside a dark cupboard for 4 days, with everything else (water, soil, temperature) kept the same. After 4 days, a leaf from each plant is tested for starch using iodine solution. Predict and explain the result for each plant, and state what this experiment proves.",
        "options": [],
        "correct_answer": "Plant A's leaf will turn blue-black with iodine (positive for starch), because it received sunlight and could carry out photosynthesis, producing glucose that gets stored as starch. Plant B's leaf will NOT turn blue-black (negative for starch), because without sunlight, photosynthesis could not occur, so no new starch was made (and any existing starch would be used up for respiration). This experiment proves that sunlight is necessary for photosynthesis (and therefore for starch production) in green plants.",
        "max_marks": 3,
        "explanation": "This is a controlled experiment where light is the only variable changed — the difference in starch test results isolates light as the necessary factor for photosynthesis.",
    },
    {
        "type": "mcq",
        "topic": "Modes of Nutrition: Autotrophic and Heterotrophic",
        "skill_category": "Mental Ability / Reasoning",
        "question": "Sort these into the correct group — which ONE of the following is the ODD ONE OUT, based on mode of nutrition?",
        "options": ["Mango tree", "Grass", "Mushroom", "Wheat plant"],
        "correct_answer": "Mushroom",
        "max_marks": 1,
        "explanation": "Mango tree, grass, and wheat plant are all green, autotrophic plants that photosynthesise. Mushroom is a fungus — a heterotroph (saprotroph) that absorbs nutrients from dead matter, making it the odd one out.",
    },
    {
        "type": "long",
        "topic": "How Plants Get Nutrients from Soil and How Soil is Replenished",
        "skill_category": "Case Study Based",
        "question": (
            "Case Study: A farmer has a 1-acre field. For the past 6 years, he has "
            "grown only maize (a non-legume crop) every season, and has not added any "
            "manure or fertiliser. He notices the maize plants are smaller and yellower "
            "than before, and yields have dropped by 40%.\n"
            "(a) Suggest a likely reason for the yellowing and smaller plants, linking "
            "it to soil nutrients.\n"
            "(b) Suggest ONE natural (biological) method and ONE artificial method the "
            "farmer could use, going forward, to restore soil fertility.\n"
            "(c) Explain how the biological method you suggested actually works at the "
            "level of bacteria/fungi."
        ),
        "options": [],
        "correct_answer": (
            "(a) Growing the same crop (maize) repeatedly without replenishing "
            "nutrients has depleted the soil, especially nitrogen — nitrogen "
            "deficiency commonly causes yellowing (poor chlorophyll formation) and "
            "stunted growth. "
            "(b) Natural method: crop rotation with a legume (e.g. growing gram or "
            "peas for one season). Artificial method: applying a nitrogen-rich "
            "chemical fertiliser (e.g. urea or an N-P-K mix). "
            "(c) Legume roots have nodules containing Rhizobium bacteria, which "
            "convert (fix) atmospheric nitrogen gas into nitrogen compounds the plant "
            "can absorb; when the legume crop is later ploughed back into the soil or "
            "harvested, this fixed nitrogen remains available in the soil for the next "
            "crop (maize)."
        ),
        "max_marks": 4,
        "explanation": "This case study connects nutrient depletion (cause), remediation methods (natural vs artificial), and the underlying biology (Rhizobium nitrogen fixation) across multiple topics in the chapter.",
    },
    {
        "type": "mcq",
        "topic": "Symbiotic Relationships",
        "skill_category": "Assertion-Reasoning / Source / Value Based",
        "question": (
            "Assertion (A): A lichen can survive on bare rocks where neither an alga "
            "nor a fungus could easily survive alone. "
            "Reason (R): In a lichen, the alga provides food made through "
            "photosynthesis, while the fungus provides shelter, moisture retention, "
            "and minerals absorbed from the rock surface. "
            "Choose the correct option:"
        ),
        "options": [
            "Both A and R are true, and R is the correct explanation of A.",
            "Both A and R are true, but R is NOT the correct explanation of A.",
            "A is true, but R is false.",
            "A is false, but R is true.",
        ],
        "correct_answer": "Both A and R are true, and R is the correct explanation of A.",
        "max_marks": 1,
        "explanation": "A is true — lichens survive in harsh habitats. R correctly explains WHY: the mutual benefit (food from alga, shelter/minerals from fungus) is exactly what allows survival in conditions neither partner could handle alone.",
    },
    {
        "type": "short",
        "topic": "Modes of Nutrition: Autotrophic and Heterotrophic",
        "skill_category": "Competency Based",
        "question": (
            "Your school is setting up a small terrace garden with limited sunlight on "
            "one side (mostly shaded) and good sunlight on the other side. A "
            "classmate suggests planting the same green, leafy vegetables on both "
            "sides. Using what you know about autotrophic nutrition, explain whether "
            "this is a good idea, and what you would suggest instead for the shaded "
            "side."
        ),
        "options": [],
        "correct_answer": (
            "This may not be a good idea, because green leafy vegetables are "
            "autotrophs that depend on sunlight for photosynthesis to make their food "
            "— in the shaded area, they would photosynthesise less, grow poorly, and "
            "produce less food/starch. For the shaded side, I would suggest plants "
            "that tolerate low light better (e.g. certain ferns, mint, or other "
            "shade-tolerant plants), or improve light availability (reflective "
            "surfaces, grow lights) if leafy vegetables must be grown there."
        ),
        "max_marks": 2,
        "explanation": "This applies the core dependency of autotrophic nutrition on sunlight to a practical, real-world planning decision.",
    },
    {
        "type": "long",
        "topic": "Other Modes of Nutrition: Parasites, Saprotrophs and Insectivorous Plants",
        "skill_category": "Creative & Open-Ended",
        "question": (
            "Imagine you discover a new plant species in a swamp. It is green, has "
            "normal leaves, but you also notice small sticky hair-like structures on "
            "its leaves that occasionally have tiny trapped insects on them. Write a "
            "short explanation (as if for a nature magazine) of what mode(s) of "
            "nutrition this plant likely uses, and why it might have evolved this way, "
            "based on what you've learned about insectivorous plants and soil "
            "nutrients."
        ),
        "options": [],
        "correct_answer": (
            "Open-ended — a strong answer should identify that the plant is likely "
            "AUTOTROPHIC (it is green with normal leaves, so it photosynthesises for "
            "its main energy) AND additionally INSECTIVOROUS (the sticky "
            "insect-trapping structures suggest it supplements its diet with insects). "
            "It should explain that swamps/marshy areas often have nutrient-poor "
            "(especially nitrogen-poor) soil, so trapping insects would help the plant "
            "obtain extra nitrogen and minerals — similar reasoning to the pitcher "
            "plant. Award full marks for a well-reasoned, scientifically grounded "
            "explanation, even if the exact wording differs."
        ),
        "max_marks": 3,
        "explanation": "This checks whether students can transfer the reasoning behind insectivorous plants (autotrophic + supplementary insect-trapping in poor soils) to a novel, unfamiliar example.",
    },
]

for i, q in enumerate(QUESTIONS):
    q["q_index"] = i

if __name__ == "__main__":
    db.init_db()
    subject_id = db.get_or_create_subject(SUBJECT)
    chapter_id = db.add_chapter(subject_id, CHAPTER_NAME, json.dumps(ANALYSIS), SOURCE_FILE, grade=GRADE)
    db.save_lesson(chapter_id, json.dumps(LESSON))
    db.save_paper(chapter_id, PAPER_TITLE, QUESTIONS)
    print(f"Seeded chapter id {chapter_id} ({CHAPTER_NAME}) with lesson and paper.")
