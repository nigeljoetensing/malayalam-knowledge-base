def retrieve(collection, query: str, embedder, top_k: int = 5) -> list[dict]:
    """
    Embed the query and retrieve top-k most relevant chunks.
    Works for both Malayalam and English queries.
    """
    query_embedding = embedder.embed_single(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    retrieved = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        retrieved.append({
            "text": doc,
            "source": meta["source"],
            "page_num": meta["page_num"],
            "score": round(1 - dist, 4)   # Convert distance → similarity
        })
    
    return retrieved

if __name__ == "__main__":
    print("Excecution Successful")

