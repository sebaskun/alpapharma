import os
import chromadb
from sentence_transformers import SentenceTransformer


class ChromaManager:
    def __init__(self, persist_dir: str = "../chroma_store"):
        # check if persist_dir exists, if not error
        print(f"Using Chroma persist directory: {persist_dir}")
        if not os.path.exists(persist_dir):
            raise ValueError(f"Chroma persist directory '{persist_dir}' does not exist. Please create it and add data before querying.")

        # Use SapBERT for biomedical embeddings (same as used for indexing)
        self.embedding_model = SentenceTransformer("cambridgeltl/SapBERT-from-PubMedBERT-fulltext")
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="fda_drugs")

    def query(self, query: str, n_results: int = 5):
        query_embedding = self.embedding_model.encode([query]).tolist()[0]
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
    