import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, chunk_text   # reuse what you already built!

# --- 1. Build the chunks (same as before, reusing ingest.py) ---
def build_chunks():
    docs = load_documents()
    chunks = []
    for doc in docs:
        for piece in chunk_text(doc["text"]):
            chunks.append({"source": doc["source"], "text": piece})
    return chunks


# --- 2. Embed the chunks and store them in ChromaDB ---
def build_database():
    chunks = build_chunks()
    print(f"Built {len(chunks)} chunks. Loading embedding model...")

    # Load the local embedding model (first run downloads it, ~90MB, one time)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Create an in-memory ChromaDB and a "collection" (like a table) to hold chunks
    client = chromadb.Client()
    collection = client.create_collection(
        "housing",
        metadata={"hnsw:space": "cosine"}   # use cosine distance (matches the model)
    )

    print("Embedding chunks and adding to ChromaDB...")
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk["text"]).tolist()  # text -> meaning-numbers
        collection.add(
            ids=[str(i)],                          # a unique id for each chunk
            embeddings=[embedding],                # the meaning-numbers
            documents=[chunk["text"]],             # the original text
            metadatas=[{"source": chunk["source"]}]  # which file it came from
        )

    print(f"Done. Stored {collection.count()} chunks in ChromaDB.")
    return collection

# --- 3. Retrieve the top-k most relevant chunks for a question ---
def search(collection, query, k=5):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode(query).tolist()   # turn the QUESTION into numbers

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    # Unpack the results into something readable
    docs = results["documents"][0]
    sources = results["metadatas"][0]
    distances = results["distances"][0]
    return list(zip(docs, sources, distances))

if __name__ == "__main__":
    collection = build_database()
    print("\n" + "=" * 70)

    # Test with 3 of your evaluation questions
    test_questions = [
        "What heating problems do students report at Cedar Pointe?",
        "I have a car - which places have bad parking?",
        "Which apartment is the cheapest?",
        "How can I protect my security deposit?",
        "Which apartments are good for students with pets?",
        "Which apartment is the quietest?", 
    ]

    for q in test_questions:
        print(f"\nQUESTION: {q}\n")
        hits = search(collection, q, k=3)  # top 3 to keep output readable
        for rank, (text, meta, dist) in enumerate(hits, 1):
            preview = text[:120].replace("\n", " ")
            print(f"  [{rank}] distance={dist:.3f} | {meta['source']}")
            print(f"      {preview}...")
        print("-" * 70)