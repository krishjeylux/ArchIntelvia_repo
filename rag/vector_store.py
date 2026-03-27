class VectorStore:
    def add(self, embeddings):
        pass
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
    """
    Handles:
    - Embedding generation
    - FAISS index creation
    - Saving & loading vector DB
    """

    def __init__(
        self,
        model_name="all-MiniLM-L6-v2",
        chunk_path="rag/chunks.pkl",
        index_path="rag/vector.index"
    ):
        self.model = SentenceTransformer(model_name)
        self.chunk_path = chunk_path
        self.index_path = index_path

        self.chunks = None
        self.embeddings = None
        self.index = None

    # -------------------------
    # LOAD CHUNKS
    # -------------------------
    def load_chunks(self):
        with open(self.chunk_path, "rb") as f:
            self.chunks = pickle.load(f)

        print(f"[✓] Loaded {len(self.chunks)} chunks")

    # -------------------------
    # CREATE EMBEDDINGS
    # -------------------------
    def create_embeddings(self):
        if self.chunks is None:
            raise ValueError("Chunks not loaded")

        print("[*] Generating embeddings...")

        self.embeddings = self.model.encode(
            self.chunks,
            show_progress_bar=True
        )

        print(f"[✓] Created embeddings: {len(self.embeddings)} vectors")

    # -------------------------
    # BUILD FAISS INDEX
    # -------------------------
    def build_index(self):
        if self.embeddings is None:
            raise ValueError("Embeddings not created")

        dim = len(self.embeddings[0])

        # L2 distance index
        self.index = faiss.IndexFlatL2(dim)

        # Convert to float32
        vectors = np.array(self.embeddings).astype("float32")

        self.index.add(vectors)

        print(f"[✓] FAISS index built with {self.index.ntotal} vectors")

    # -------------------------
    # SAVE INDEX
    # -------------------------
    def save_index(self):
        if self.index is None:
            raise ValueError("Index not built")

        faiss.write_index(self.index, self.index_path)
        print(f"[✓] Index saved to {self.index_path}")

    # -------------------------
    # FULL PIPELINE
    # -------------------------
    def build(self):
        """
        Run full ingestion pipeline
        """
        self.load_chunks()
        self.create_embeddings()
        self.build_index()
        self.save_index()


# -------------------------
# RUN INGESTION
# -------------------------
if __name__ == "__main__":
    vs = VectorStore()
    vs.build()