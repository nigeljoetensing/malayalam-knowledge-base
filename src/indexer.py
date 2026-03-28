import chromadb
from chromadb.config import Settings

def get_chroma_client(persist_dir: str = "./chroma_db"):
    """Initialize a persistent ChromaDB client."""
    client = chromadb.PersistentClient(path=persist_dir)
    return client

def get_or_create_collection(client, name: str = "malayalam_kb"):
    """Get or create the Malayalam knowledge base collection."""
    collection = client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}  # Use cosine distance for LaBSE
    )
    return collection

def index_chunks(collection, chunks: list[dict], embedder):
    """Index all chunks into ChromaDB with embeddings and metadata."""
    
    # ChromaDB requires ids, documents, embeddings, and metadata separately
    ids = [c["chunk_id"] for c in chunks]
    texts = [c["text"] for c in chunks]
    metadatas = [
        {
            "source": c["source"],
            "page_num": c["page_num"],
            "is_malayalam": str(c["is_malayalam"])
        }
        for c in chunks
    ]
    
    # Embed in one shot (LaBSE handles batching internally)
    print(f"Embedding {len(texts)} chunks...")
    embeddings = embedder.embed(texts)
    
    # Upsert — safe to re-run without duplicating
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )
    print(f"✓ Indexed {len(chunks)} chunks into ChromaDB")

if __name__ == "__main__":
    print("Excecution Successful")