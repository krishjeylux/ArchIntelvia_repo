import os
import pickle

class Chunker:
    """
    Splits markdown documents into concept-level chunks for RAG.
    Each chunk starts with 'Title:' and includes Concept, Effect, Use Case, Rules.
    """

    def __init__(self, docs_path="rag/documents", output_path="rag/chunks.pkl"):
        self.docs_path = docs_path
        self.output_path = output_path

    def chunk_file(self, filepath):
        """Split a single .md file into concept chunks."""
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Split by 'Title:' but keep the delimiter
        raw_chunks = content.split("Title:")
        chunks = []
        for c in raw_chunks:
            c = c.strip()
            if not c:
                continue
            chunks.append("Title:" + c)
        return chunks

    def chunk_all(self):
        """Chunk all .md files in the documents folder."""
        all_chunks = []
        for fname in os.listdir(self.docs_path):
            if fname.endswith(".md"):
                path = os.path.join(self.docs_path, fname)
                file_chunks = self.chunk_file(path)
                all_chunks.extend(file_chunks)
        return all_chunks

    def save_chunks(self, chunks):
        """Persist chunks to pickle for embeddings."""
        with open(self.output_path, "wb") as f:
            pickle.dump(chunks, f)
        print(f"Saved {len(chunks)} chunks to {self.output_path}")

    def run(self):
        chunks = self.chunk_all()
        self.save_chunks(chunks)
        return chunks


if __name__ == "__main__":
    chunker = Chunker()
    all_chunks = chunker.run()
    print(f"Total chunks created: {len(all_chunks)}")