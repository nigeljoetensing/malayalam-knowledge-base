from sentence_transformers import SentenceTransformer
import numpy as np

class MalayalamEmbedder:
    def __init__(self):
        # LaBSE supports 109 languages including Malayalam
        # Alternative: "ai4bharat/indic-bert" for Indic-specific tasks
        self.model = SentenceTransformer("sentence-transformers/LaBSE")
        print(f"Loaded LaBSE embedder (dim={self.model.get_sentence_embedding_dimension()})")
    
    def embed(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        """Embed a list of texts in batches."""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True   # Cosine similarity works better normalized
        )
        return embeddings.tolist()
    
    def embed_single(self, text: str) -> list[float]:
        """Embed a single query."""
        embedding = self.model.encode([text], normalize_embeddings=True)
        return embedding[0].tolist()

if __name__ == "__main__":
    print("Excecution Successful")