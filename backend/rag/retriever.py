import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class Retriever:
    """
    Runtime retrieval system

    Flow:
    Query → Embedding → FAISS search → Top-K chunks → Context
    """

    def __init__(
        self,
        index_path="rag/vector.index",
        chunk_path="rag/chunks.pkl",
        model_name="all-MiniLM-L6-v2"
    ):
        # Load embedding model
        self.model = SentenceTransformer(model_name)

        # Load FAISS index
        self.index = faiss.read_index(index_path)

        # Load chunks
        with open(chunk_path, "rb") as f:
            self.chunks = pickle.load(f)

        print(f"[✓] Retriever initialized | {len(self.chunks)} chunks loaded")

    # -------------------------
    # INTERNAL: QUERY BUILDER
    # -------------------------
    def build_query(self, params: dict) -> str:
        """
        Convert structured params → natural language query
        This improves retrieval quality significantly
        """

        query = "Memory controller design with "

        parts = []
        for k, v in params.items():
            parts.append(f"{k} = {v}")

        query += ", ".join(parts)

        # Add domain hint
        query += ". Consider architecture, banks, arbitration, pipeline, and power."

        return query

    # -------------------------
    # MAIN RETRIEVE FUNCTION
    # -------------------------
    def search(self, params: dict, k: int = 6) -> str:
        """
        Returns top-k relevant chunks as a single context string
        """

        # Build query
        query = self.build_query(params)

        # Embed query
        q_emb = self.model.encode([query], normalize_embeddings=True)

        # Search FAISS
        distances, indices = self.index.search(np.array(q_emb), k)

        # Collect results
        results = []
        for idx in indices[0]:
            if idx < len(self.chunks):
                results.append(self.chunks[idx])

        # Join into context
        context = "\n\n---\n\n".join(results)
        context = context[:2000]  # prevent LLM overload
        return context

    # -------------------------
    # DEBUG FUNCTION
    # -------------------------
    def debug_search(self, params: dict, k: int = 5):
        """
        Prints retrieved chunks for debugging
        """
        context = self.search(params, k)

        print("\n🔍 Retrieved Context:\n")
        print(context)
        print("\n" + "=" * 50 + "\n")

        return context


# -------------------------
# TEST RUN
# -------------------------
if __name__ == "__main__":
    retriever = Retriever()

    test_params = {
        "DATA_WIDTH": 32,
        "ADDR_WIDTH": 10,
        "BANKS": 4,
        "PIPELINE_DEPTH": 2,
        "LOW_POWER_MODE": True
    }

    retriever.debug_search(test_params)
# Singleton retriever instance
retriever_instance = Retriever()


def retrieve_context(params: dict) -> str:
    """
    External interface used by planner
    """
    return retriever_instance.search(params)