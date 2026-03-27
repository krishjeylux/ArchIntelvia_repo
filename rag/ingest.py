import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

import chunker


class Ingestor:
    """
    Full ingestion pipeline:
    1. Load markdown documents
    2. Chunk into concept blocks
    3. Generate embeddings
    4. Store FAISS index + chunks
    """

    def __init__(
        self,
        docs_path="rag/documents",
        chunk_path="rag/chunks.pkl",
        index_path="rag/vector.index"
    ):
        self.docs_path = docs_path
        self.chunk_path = chunk_path
        self.index_path = index_path

        # Embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    # -------------------------
    # STEP 1: CHUNK DOCUMENTS
    # -------------------------
    def create_chunks(self):
        doc_chunker = chunker.Chunker(self.docs_path, self.chunk_path)
        chunks = doc_chunker.chunk_all()
        doc_chunker.save_chunks(chunks)
        print(f"[✓] Created {len(chunks)} chunks")
        return chunks

    # -------------------------
    # STEP 2: EMBED CHUNKS
    # -------------------------
    def embed_chunks(self, chunks):
        print("[*] Generating embeddings...")
        embeddings = self.model.encode(chunks)
        return np.array(embeddings)

    # -------------------------
    # STEP 3: BUILD FAISS INDEX
    # -------------------------
    def build_index(self, embeddings):
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        print(f"[✓] FAISS index built with {index.ntotal} vectors")
        return index

    # -------------------------
    # STEP 4: SAVE INDEX + DATA
    # -------------------------
    def save(self, index, chunks):
        faiss.write_index(index, self.index_path)

        with open(self.chunk_path, "wb") as f:
            pickle.dump(chunks, f)

        print(f"[✓] Saved index → {self.index_path}")
        print(f"[✓] Saved chunks → {self.chunk_path}")

    # -------------------------
    # RUN FULL PIPELINE
    # -------------------------
    def run(self):
        print("\n🚀 Starting ingestion pipeline...\n")

        chunks = self.create_chunks()
        embeddings = self.embed_chunks(chunks)
        index = self.build_index(embeddings)
        self.save(index, chunks)

        print("\n✅ Ingestion complete!\n")


# -------------------------
# CLI ENTRYPOINT
# -------------------------
if __name__ == "__main__":
    ingestor = Ingestor()
    ingestor.run()