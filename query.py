import os
from dotenv import load_dotenv
from src.embedder  import MalayalamEmbedder
from src.indexer   import get_chroma_client, get_or_create_collection
from src.retriever import retrieve
from src.qa_engine import answer_question, check_ollama_connection, OLLAMA_MODEL

load_dotenv()

def main():
    print("Malayalam Knowledge Base (Ollama Local Mode)")
    print("=" * 56)

    # Verify Ollama is running
    if not check_ollama_connection():
        print("\n Ollama server not reachable at http://localhost:11434")
        print("   Start it with:  ollama serve")
        print("   Then re-run:    python query.py")
        return

    print(f" Ollama connected  |  Model: {OLLAMA_MODEL}")
    print("   All inference is local — no data leaves this machine.\n")

    # Load components
    embedder   = MalayalamEmbedder()
    client     = get_chroma_client("./chroma_db")
    collection = get_or_create_collection(client)
    print(f" Knowledge base loaded: {collection.count()} chunks indexed\n")
    print("Type 'exit' to quit\n")

    while True:
        query = input("ചോദ്യം (Question): ").strip()
        if query.lower() in ("exit", "quit"):
            break
        if not query:
            continue

        chunks = retrieve(collection, query, embedder, top_k=5)

        print("\n Retrieved sources:")
        for c in chunks:
            print(f"   • {c['source']}, p.{c['page_num']}  (score: {c['score']})")

        print(f"\n Answer  [{OLLAMA_MODEL} — local]:")
        answer = answer_question(query, chunks)
        print(answer)
        print("\n" + "─" * 56 + "\n")

if __name__ == "__main__":
    main()