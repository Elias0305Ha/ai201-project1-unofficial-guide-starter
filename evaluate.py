from embed import build_database
from generate import answer_question

# Your 6 evaluation questions + the expected answers from planning.md
EVAL = [
    {
        "question": "What heating problems do students report at Cedar Pointe?",
        "expected": "Older units don't get above ~62F in January no matter the thermostat; maintenance calls it 'normal for the older units.'",
    },
    {
        "question": "Which apartment is the cheapest, and what's the catch?",
        "expected": "Riverside Commons (~$450/mo, utilities included). Catch: older building (had roaches) and the lot floods in spring.",
    },
    {
        "question": "I have a car - which places have bad parking?",
        "expected": "Stonebrook Flats (small lot, aggressive towing). Cedar Pointe by contrast has free/easy parking but is far from campus.",
    },
    {
        "question": "How can I protect my security deposit?",
        "expected": "Take timestamped move-in photos, photograph existing damage, email them to yourself. MN law requires return within 21 days with itemized deductions.",
    },
    {
        "question": "Which apartments are good for students with pets?",
        "expected": "Birchwood Student Living (dog park, pet friendly, bus stop), but high pet fees ($300 deposit + $35/mo per animal).",
    },
    {
        "question": "Which apartment is the quietest?",
        "expected": "(Deliberate hard case) No doc directly ranks quietness. Oakwood is 'super quiet'; Maple Ridge has thin walls; The Hub has loud weekends. System likely struggles.",
    },
]


if __name__ == "__main__":
    collection = build_database()
    print("\n" + "#" * 75)
    print("# EVALUATION RESULTS")
    print("#" * 75)

    for i, item in enumerate(EVAL, 1):
        answer, sources = answer_question(collection, item["question"])
        print(f"\n{'=' * 75}")
        print(f"Q{i}: {item['question']}")
        print(f"{'-' * 75}")
        print(f"EXPECTED:\n{item['expected']}\n")
        print(f"SYSTEM ANSWER:\n{answer}\n")
        print(f"SOURCES: {', '.join(sources)}")
        print(f"JUDGMENT: [ fill in: accurate / partially accurate / inaccurate ]")

    print(f"\n{'#' * 75}")
    print("# END")
    print("#" * 75)