# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

This Unofficial Guide covers off-campus student housing near Minnesota State University, Mankato. Official sources like the housing page and listing sites tell you rent, floor plans, and amenities — but they won't warn you about mold, slow maintenance, towing-happy parking lots, or landlords who keep your deposit. That honest, lived-experience knowledge only shows up in student reviews and word of mouth, which is scattered and hard to search.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #  | Source | Description | URL or location |
|----|--------|-------------|-----------------|
| 1  | Original synthetic review (made-up data) | Maple Ridge — nice gym/pool, slow maintenance (AC out 9 days), thin walls, ~$600/mo | documents/maple_ridge_01.txt |
| 2  | Original synthetic review (made-up data) | Stonebrook Flats — bad parking/towing, mold in bathroom, in-unit washer/dryer | documents/stonebrook_flats_01.txt |
| 3  | Original synthetic review (made-up data) | The Hub on 7th — pricey ($1,150), great downtown location, loud weekends, responsive mgmt | documents/the_hub_on_7th_01.txt |
| 4  | Original synthetic review (made-up data) | The Hub on 7th — 24/7 study lounges, elevator always broken, package stolen | documents/the_hub_on_7th_02.txt |
| 5  | Original synthetic review (made-up data) | Riverside Commons — cheapest (~$450), utilities included, roach issue, kind landlord | documents/riverside_commons_01.txt |
| 6  | Original synthetic review (made-up data) | Riverside Commons — responsive landlord, spring parking-lot flooding by the river | documents/riverside_commons_02.txt |
| 7  | Original synthetic review (made-up data) | Oakwood Townhomes — good for groups, attached garage, no summer sublet, deposit dispute | documents/oakwood_townhomes_01.txt |
| 8  | Original synthetic review (made-up data) | Birchwood Student Living — pet friendly, dog park, high pet fees, shared laundry | documents/birchwood_student_living_01.txt |
| 9  | Original synthetic review (made-up data) | Cedar Pointe — cheap (~$475) but far from campus, poor winter heating, free parking | documents/cedar_pointe_01.txt |
| 10 | Original synthetic review (made-up data) | Cedar Pointe — cheap, parking-lot break-ins, slow snow removal | documents/cedar_pointe_02.txt |
| 11 | Original synthetic long-form doc (made-up data) | Off-Campus Housing Survival Guide — leases, deposits, utilities, parking, roommates, red flags; references all 7 complexes | documents/housing_survival_guide.txt |
| 12 | Original synthetic long-form doc (made-up data) | Neighborhood & Commute Breakdown — areas by walkability/commute/price; references all 7 complexes | documents/neighborhood_commute_breakdown.txt |
| 13 | Original synthetic long-form doc (made-up data) | Forum Megathread — anonymous students debating value, deposits, parking; references all 7 complexes | documents/housing_forum_megathread.txt |
---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** Short reviews are kept as a single chunk (~400 characters), with a ~1,000 character cutoff to decide what counts as "short." Long guides are split into multiple chunks of roughly 800–1,000 characters.

**Overlap:** ~100–150 characters of overlap between chunks of the long guides. No overlap for the short reviews, since they aren't split.

**Reasoning:** My documents come in two types — long ones and short ones. The short ones are single reviews tied to one apartment by name. The long ones pull together information from different sources like forums and neighborhood/commute guides, and usually mention several apartments. I keep the short ones as one chunk because they only have a few sentences and splitting them wouldn't help — each is already one complete thought. I split the long ones into multiple chunks because they're many paragraphs and each paragraph usually covers a different apartment or topic, so splitting keeps each chunk focused. I add a little overlap so that if an important fact sits right where I cut, it still appears in both neighboring chunks instead of getting split in half and lost.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->


**Embedding model:** all-MiniLM-L6-v2, via the sentence-transformers library. It runs locally on my computer, so there's no API key, no rate limits, and no cost.

**Top-k:** Start with k=5 (retrieve the 5 most relevant chunks per query). Few enough to keep the context focused, but enough to cover answers that are spread across multiple chunks/files. I'll tune this after seeing real retrieval results.

**Production tradeoff reflection:** I'm using all-MiniLM-L6-v2 because it's small, fast, free, and good enough for a project of this size. If I were deploying this for real users and cost wasn't a constraint, I'd weigh a few tradeoffs. A larger or API-based embedding model would likely give better accuracy on nuanced, opinion-heavy review text, at the cost of higher price and slower latency. I'd also consider multilingual support if the student body needed languages other than English, since all-MiniLM-L6-v2 is English-focused. Finally, I'd weigh local vs. API hosting: local keeps data private and free but is less powerful, while an API model is stronger but sends data off my machine and costs money per request.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What heating problems do students report at Cedar Pointe? | Older units don't get above ~62°F in January no matter the thermostat setting; maintenance calls it "normal for the older units." |
| 2 | Which apartment is the cheapest, and what's the catch? | Riverside Commons (~$450/month, utilities included). Catch: it's an older building (had a roach problem) and the parking lot floods in spring. |
| 3 | I have a car — which places have bad parking? | Stonebrook Flats — small lot and aggressive towing (students towed twice). Cedar Pointe, by contrast, has free/easy parking but is far from campus. |
| 4 | How can I protect my security deposit? | Take timestamped move-in photos of every room before unpacking, photograph existing damage, and email them to yourself. Minnesota law requires the deposit be returned within 21 days with itemized deductions. |
| 5 | Which apartments are good for students with pets? | Birchwood Student Living — pet friendly with an on-site dog park and a bus stop outside, but pet fees are high ($300 deposit + $35/month pet rent per animal). |
| 6 | Which apartment is the quietest? | ( hard case) No document directly ranks quietness. Oakwood Townhomes is described as "super quiet," while Maple Ridge has thin walls and The Hub on 7th has loud weekends — so the system may struggle to give a single clean answer. Likely failure case. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->


1. Duplicate information across documents. The same fact (e.g. Cedar Pointe's heating problem) appears in a short review, the survival guide, and the forum thread. Retrieval might return two chunks that say almost the same thing, wasting a slot and giving the LLM redundant context instead of new information.

2. Questions whose answer is scattered or not stated directly. For example "which apartment is the quietest?" — no single chunk ranks quietness; the clues are spread across multiple documents. Retrieval may pull related-but-imperfect chunks and the system could give a vague or inaccurate answer.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
┌─────────────────────────────────────────────────────────────────────┐
│                    THE UNOFFICIAL GUIDE — RAG PIPELINE                │
└─────────────────────────────────────────────────────────────────────┘

   [1] DOCUMENT INGESTION
       Load 13 .txt files from documents/  (skip .gitkeep)
       Tool: plain Python (open / read files)
                       │
                       ▼
   [2] CHUNKING
       Short reviews → kept whole (1 chunk)
       Long guides   → split at section/paragraph boundaries
                       (~800–1,000 chars, ~100–150 char overlap)
       Tool: custom Python chunk_text() function
                       │
                       ▼
   [3] EMBEDDING + VECTOR STORE
       Turn each chunk into a vector, store with source metadata
       Tools: all-MiniLM-L6-v2 (sentence-transformers) + ChromaDB
                       │
                       ▼
   [4] RETRIEVAL
       Embed the user's question, find top-k=5 most similar chunks
       Tool: ChromaDB similarity search
                       │
                       ▼
   [5] GENERATION
       Feed retrieved chunks to the LLM, answer ONLY from them,
       cite which document(s) the answer came from
       Tools: Groq (llama-3.3-70b-versatile) + Gradio (UI)
```
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->


**Milestone 3 — Ingestion and chunking:** I'll use Claude. Input: my Documents section (13 .txt files, two types — short reviews and long guides), my Chunking Strategy section (keep short reviews whole, split long guides at section/paragraph boundaries at ~800–1,000 chars with ~100–150 char overlap), and my Architecture diagram. I expect it to produce a Python script that loads all .txt files from documents/ (skipping .gitkeep), decides short-vs-long by length, and produces clean chunks. I'll verify by printing 5 sample chunks and checking each is readable, self-contained, and tagged with its source filename.

**Milestone 4 — Embedding and retrieval:** I'll use Claude. Input: my Retrieval Approach section (all-MiniLM-L6-v2, top-k=5) and my Architecture diagram. I expect it to produce code that embeds each chunk, stores it in ChromaDB with source metadata, and a retrieval function that takes a query and returns the top-5 chunks with their sources and distance scores. I'll verify by running 3 of my evaluation questions and checking the returned chunks are actually relevant (distance scores below ~0.5) before adding any generation.

**Milestone 5 — Generation and interface:** I'll use Claude. Input: my grounding requirement (answer ONLY from retrieved chunks, say "I don't have enough information" otherwise), my desired output format (answer + source list), and the Gradio skeleton from the spec. I expect it to wire retrieval → Groq (llama-3.3-70b-versatile) → a Gradio UI, with source attribution added programmatically. I'll verify by asking an in-scope question (must cite a real source) and an out-of-scope question (must refuse instead of making something up).