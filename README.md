# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This Unofficial Guide covers off-campus student housing near Minnesota State University, Mankato. Official sources like the housing page and listing sites tell you rent, floor plans, and amenities — but they won't warn you about mold, slow maintenance, towing-happy parking lots, or landlords who keep your deposit. That honest, lived-experience knowledge only shows up in student reviews and word of mouth, which is scattered and hard to search.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| #  | Source | Type | URL or file path |
|----|--------|------|------------------|
| 1  | Synthetic student review (made-up) | Short review | documents/maple_ridge_01.txt |
| 2  | Synthetic student review (made-up) | Short review | documents/stonebrook_flats_01.txt |
| 3  | Synthetic student review (made-up) | Short review | documents/the_hub_on_7th_01.txt |
| 4  | Synthetic student review (made-up) | Short review | documents/the_hub_on_7th_02.txt |
| 5  | Synthetic student review (made-up) | Short review | documents/riverside_commons_01.txt |
| 6  | Synthetic student review (made-up) | Short review | documents/riverside_commons_02.txt |
| 7  | Synthetic student review (made-up) | Short review | documents/oakwood_townhomes_01.txt |
| 8  | Synthetic student review (made-up) | Short review | documents/birchwood_student_living_01.txt |
| 9  | Synthetic student review (made-up) | Short review | documents/cedar_pointe_01.txt |
| 10 | Synthetic student review (made-up) | Short review | documents/cedar_pointe_02.txt |
| 11 | Synthetic long-form guide (made-up) | Long guide | documents/housing_survival_guide.txt |
| 12 | Synthetic long-form guide (made-up) | Long guide | documents/neighborhood_commute_breakdown.txt |
| 13 | Synthetic forum thread (made-up) | Long thread | documents/housing_forum_megathread.txt |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** Short reviews (under ~1,000 characters) are kept whole as a single chunk. Long guides are split into chunks of ~900 characters.

**Overlap:** ~150 characters of overlap between chunks of the long guides. No overlap for short reviews, since they aren't split.

**Why these choices fit your documents:** My corpus has two shapes — short reviews (~350–450 chars, one apartment, one or two points) and long guides (~4,000–6,100 chars, many topics). A short review is already one complete thought, so splitting it would only break context. A long guide covers many topics, so leaving it whole would make one chunk match many queries weakly. Splitting the long guides keeps each chunk focused on a smaller set of topics, and the ~150-char overlap means a fact sitting on a chunk boundary still appears in both neighboring chunks instead of being cut in half.

**Preprocessing:** Documents are plain .txt files, so cleaning was minimal — I strip leading/trailing whitespace from each chunk. The loader uses `.glob("*.txt")` so non-document files like `.gitkeep` are skipped automatically.

**Final chunk count:** 32 chunks across 13 documents (10 short reviews → 1 chunk each; 3 long guides → 22 chunks total).

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2, via the sentence-transformers library. It runs locally on my machine, so there's no API key, no rate limits, and no cost. I retrieve the top k=5 chunks per query using cosine similarity in ChromaDB.

**Production tradeoff reflection:** I chose all-MiniLM-L6-v2 because it's small, fast, free, and accurate enough for a corpus this size. If I were deploying for real users and cost wasn't a constraint, I'd weigh several tradeoffs. A larger or API-hosted embedding model would likely give better accuracy on nuanced, opinion-heavy review text, at the cost of higher price and higher latency. I'd consider multilingual support if the student body needed languages beyond English, since all-MiniLM-L6-v2 is English-focused. Finally, I'd weigh local vs. API hosting: local keeps data private and free but is less powerful, while an API model is stronger but sends data off the machine and costs money per request.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** The system prompt explicitly restricts the model to the retrieved context. It instructs: answer the question using ONLY the information in the provided context, do not use any outside knowledge, and if the context does not contain enough information, respond exactly "I don't have enough information on that." I also set the model temperature low (0.2) to keep answers factual and close to the source text rather than creative.

**Structural grounding (not just instructions):** Grounding isn't left to the prompt alone. Before calling the LLM, I build a context block out of ONLY the top-k retrieved chunks, and each chunk is prefixed with its source filename like `[Source: cedar_pointe_01.txt]`. The model never sees the full document set or the open internet — only those retrieved chunks — so structurally its answer has to come from them.

**How source attribution is surfaced in the response:** Source attribution is added programmatically, not left to the model. After retrieval, I collect the unique source filenames of the retrieved chunks and return them alongside the answer. The Gradio interface displays these in a separate "Retrieved from" box, so every answer shows exactly which document(s) it drew from.

**Verification:** I confirmed grounding works by asking an out-of-scope question ("What is the pet policy at the campus dorms?"). Even though retrieval still returned the closest available chunks (about off-campus pet policies), the system correctly refused with "I don't have enough information on that" rather than fabricating a dorm policy.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What heating problems do students report at Cedar Pointe? | Older units stay below ~62°F in January no matter the thermostat; maintenance calls it "normal." | Reported older units struggle to stay above 62°F in deep winter, thermostat doesn't help, maintenance called it "normal." | Relevant | Accurate |
| 2 | Which apartment is the cheapest, and what's the catch? | Riverside Commons (~$450, utilities included); catch: old building, roaches, spring flooding. | Riverside Commons (~$450, utilities included); catch: old building with a roach issue. Did NOT mention spring flooding. | Partially relevant | Partially accurate |
| 3 | I have a car — which places have bad parking? | Stonebrook Flats (small lot, towing); Cedar Pointe by contrast has easy parking. | Stonebrook Flats has bad parking — small lot, frequent towing. Did NOT give the Cedar Pointe easy-parking contrast. | Relevant | Partially accurate |
| 4 | How can I protect my security deposit? | Timestamped move-in photos, photograph existing damage, email to self; MN law = 21-day return. | Take timestamped photos of every room before unpacking, email them to yourself, to avoid disputes. Omitted the 21-day MN law detail. | Relevant | Accurate |
| 5 | Which apartments are good for students with pets? | Birchwood (dog park, bus stop, pet friendly); high pet fees ($300 + $35/mo per animal). | Birchwood is the pet-friendly option — dog park, bus stop outside; pet fees $300 deposit + $35/mo per animal. | Relevant | Accurate |
| 6 | Which apartment is the quietest? | (Hard case) No doc ranks quietness; Oakwood "super quiet," Maple Ridge thin walls, Hub loud. | Correctly answered Oakwood Townhomes ("super quiet, no party noise") — BUT retrieval ranked The Hub on 7th (the loudest building) #1. | Off-target (top result was the loudest place) | Partially accurate (generation recovered) |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

**Summary:** Of 6 questions, 3 were fully accurate (Q1, Q4, Q5) and 3 partially accurate (Q2, Q3, Q6). The two "partially accurate" non-failure cases (Q2, Q3) were both cases of *incomplete* answers — the system gave correct information but missed a secondary detail that lived in a chunk outside the retrieved top-k. Q6 is analyzed in detail below as the failure case.

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "Which apartment is the quietest?"

**What the system returned:** The final answer was actually correct — it named Oakwood Townhomes ("super quiet neighborhood, no party noise"). However, the *retrieval* step failed: the top-ranked retrieved chunk was The Hub on 7th, which is described in my documents as one of the LOUDEST options (downtown bar district, loud weekends). So the answer was right, but the retrieval that fed it was off-target.

**Root cause (tied to a specific pipeline stage):** This is a **retrieval-stage** failure with two causes. First, semantic search matches on *topic*, not *stance*: the words "quietest" and "loud" both live in the semantic neighborhood of "noise," so a chunk that talks heavily about being loud scores as highly relevant to a query about quietness. The embedding model has no notion that "loud" is the opposite of what was asked. Second, no single document in my corpus explicitly *ranks* quietness — the relevant clues are scattered (Oakwood "super quiet," Maple Ridge "thin walls," Hub "loud weekends"), so there is no clean, directly-matching chunk for retrieval to surface even in principle.

**Why the final answer was still correct (and why that's its own risk):** The grounded generation step compensated for the bad retrieval. The LLM read all the retrieved chunks and correctly identified Oakwood as the quiet one while ignoring the loud Hub chunk. This reveals an important separation: retrieval quality and generation quality are independent, and a strong generation step can *mask* a weak retrieval result. That masking is itself a risk — in a less obvious case, bad retrieval could quietly degrade answers without any visible signal, because the surface answer still looks plausible.

**What I would change to fix it:** A few options, in order of effort. (1) Increase top-k or retrieve more context so the genuinely-relevant chunk (Oakwood) is reliably included rather than crowded out. (2) Add hybrid search (semantic + BM25 keyword) so exact terms get weighted, though this wouldn't fully solve the topic-vs-stance issue. (3) The deeper fix: stance/sentiment is hard for pure semantic similarity, so for comparative questions like "quietest" or "cheapest," the system would benefit from metadata or structured fields (e.g., a noise rating per complex) that the model could filter or sort on, rather than relying on free-text similarity alone.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Writing planning.md before any code forced me to decide my chunking strategy up front, based on actually reading my documents. Because I'd already reasoned through "short reviews stay whole, long guides get split," the implementation was straightforward and I knew what correct output looked like when I inspected the chunks. The spec's "test retrieval before adding generation" rule also caught a real issue early — I saw my distance scores looked wrong at the retrieval stage and fixed it before generation, instead of debugging a confusing end-to-end failure later.

**One way your implementation diverged from the spec, and why:** My planning.md said I'd split long guides at section/paragraph boundaries, but my actual chunk_text() splits at a fixed ~900 characters with overlap, so cuts sometimes land mid-section. I kept the simpler fixed-size approach because when I tested retrieval, it returned relevant, correct chunks anyway — there was no evidence the blurred boundaries were hurting results. Following the spec's own "test before optimizing" principle, I chose not to add complexity the results didn't justify. It's noted as a candidate improvement if retrieval quality needed to go up.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My planning.md chunking strategy and document descriptions, and asked it to implement the loading and chunking pipeline (ingest.py).
- *What it produced:* A loader using `.glob("*.txt")` and a `chunk_text()` function that keeps short documents whole and splits long ones with character-based overlap.
- *What I changed or overrode:* I questioned why overlap only steps backward by 150 chars instead of padding both sides, and confirmed the seam logic before accepting it. I also decided to keep fixed-size splitting rather than upgrading to section-aware splitting, after testing showed retrieval worked.

**Instance 2**

- *What I gave the AI:* My first retrieval test output, where the correct chunks were ranked right but the distance scores were oddly high (0.8–1.1).
- *What it produced:* The diagnosis that ChromaDB defaults to squared-L2 distance while all-MiniLM-L6-v2 expects cosine, plus the one-line fix to create the collection with `metadata={"hnsw:space": "cosine"}`.
- *What I changed or overrode:* I applied the fix and verified it myself — confirming the rankings stayed identical while distances dropped into an interpretable range (~0.4 for good matches), proving the data was always fine and only the metric was mismatched.
