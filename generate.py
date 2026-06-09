import os
from dotenv import load_dotenv
from groq import Groq
from embed import build_database, search

load_dotenv()  # reads your .env file so the key is available

# Connect to Groq using the key from .env (never hardcoded)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def answer_question(collection, question, k=5):
    """Retrieve relevant chunks, then have the LLM answer using ONLY those chunks."""

    # 1. Retrieve the top-k chunks (your Milestone 4 work)
    hits = search(collection, question, k=k)

    # 2. Build the context block from retrieved chunks, tagged with sources
    context = ""
    sources = []
    for text, meta, dist in hits:
        context += f"[Source: {meta['source']}]\n{text}\n\n"
        if meta["source"] not in sources:
            sources.append(meta["source"])

    # 3. The grounding instructions — this is the key engineering part
    system_prompt = (
        "You are a helpful assistant answering questions about off-campus student "
        "housing near Minnesota State University, Mankato. Answer the user's question "
        "using ONLY the information in the provided context below. Do not use any outside "
        "knowledge. If the context does not contain enough information to answer, say "
        "exactly: 'I don't have enough information on that.' Keep your answer concise."
    )

    user_prompt = f"Context:\n\n{context}\nQuestion: {question}"

    # 4. Call the Groq LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,  # low = stick close to the facts, less creative drift
    )

    answer = response.choices[0].message.content
    return answer, sources


if __name__ == "__main__":
    collection = build_database()
    print("\n" + "=" * 70)

    question = "What is the pet policy at the campus dorms?"
    answer, sources = answer_question(collection, question)

    print(f"\nQUESTION: {question}\n")
    print(f"ANSWER:\n{answer}\n")
    print(f"SOURCES: {', '.join(sources)}")
    print("=" * 70)