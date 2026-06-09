from pathlib import Path

# Point to the documents folder (sits next to this script)
DOCS_FOLDER = Path("documents")

def load_documents():
    """Load every .txt file from the documents folder into a list."""
    documents = []  # we'll collect each file's info here

    # .glob("*.txt") grabs only .txt files — automatically skips .gitkeep
    for file_path in DOCS_FOLDER.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")  # read the file's contents
        documents.append({
            "source": file_path.name,  # e.g. "cedar_pointe_01.txt"
            "text": text               # the actual review/guide text
        })

    return documents
# How we decide short vs. long, and how we slice the long ones
SHORT_DOC_LIMIT = 1000   # docs under this many chars stay as ONE chunk
CHUNK_SIZE = 900         # target size for chunks of long docs
OVERLAP = 150            # chars repeated between neighboring chunks

def chunk_text(text):
    """Split one document's text into a list of chunks, using our strategy."""
    text = text.strip()  # remove blank space at the start/end

    # SHORT doc → keep whole (splitting wouldn't help; it's one thought)
    if len(text) <= SHORT_DOC_LIMIT:
        return [text]

    # LONG doc → split into overlapping pieces
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE          # tentative end of this chunk
        chunk = text[start:end]           # slice out the piece
        chunks.append(chunk.strip())
        start = end - OVERLAP             # step back by OVERLAP for the next one

    return chunks

# This block runs only when you run this file directly
if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents.\n")

    all_chunks = []
    for doc in docs:
        pieces = chunk_text(doc["text"])
        for piece in pieces:
            all_chunks.append({"source": doc["source"], "text": piece})

    print(f"Total chunks: {len(all_chunks)}\n")
    print("=" * 70)

    # Inspect 5 chunks: a few short-review chunks and a couple long-guide chunks
    inspect = [0, 10, 13, 14, 20]  # indexes picked to mix short + long docs
    for i in inspect:
        chunk = all_chunks[i]
        print(f"\n--- CHUNK #{i} | source: {chunk['source']} | {len(chunk['text'])} chars ---")
        print(chunk["text"])
        print("=" * 70)