import ollama

# ── Configuration ──
OLLAMA_MODEL  = "llama3"          # Change to "mistral" or "gemma3" as preferred
OLLAMA_HOST   = "http://localhost:11434"   # Default Ollama server address

SYSTEM_PROMPT = """You are an expert assistant for a Malayalam Knowledge Base called VaakSetu.

STRICT RULES:
1. Answer ONLY using the provided context from the uploaded PDFs.
2. If the answer is not in the context, respond with:
   "ഈ ചോദ്യത്തിനുള്ള ഉത്തരം നൽകിയ PDF-കളിൽ കണ്ടെത്താനായില്ല."
   (The answer to this question was not found in the provided PDFs.)
3. Always cite which PDF and page number the answer comes from.
4. Answer in the same language as the question (Malayalam or English).
5. Do not use any external knowledge — only what is in the context below.
"""

def build_context(retrieved_chunks: list[dict]) -> str:
    """Format retrieved chunks into a structured context block."""
    parts = []
    for i, chunk in enumerate(retrieved_chunks, 1):
        parts.append(
            f"[Source {i}: {chunk['source']}, Page {chunk['page_num']} "
            f"(relevance: {chunk['score']})]:\n{chunk['text']}"
        )
    return "\n\n---\n\n".join(parts)


def answer_question(query: str, retrieved_chunks: list[dict]) -> str:
    """
    Generate a grounded answer using a local Ollama model.
    Fully offline — no data leaves the machine.
    """
    context = build_context(retrieved_chunks)

    user_message = f"""Context from PDFs:
{context}

Question: {query}

Answer based strictly on the above context. Cite your sources (PDF name and page number)."""

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        options={
            "temperature": 0.1,    # Low temperature = more factual, less creative
            "num_ctx":     4096,   # Context window — increase to 8192 for longer answers
        }
    )

    return response["message"]["content"]


def check_ollama_connection() -> bool:
    """Verify Ollama server is running before starting the Q&A loop."""
    try:
        ollama.list()
        return True
    except Exception:
        return False

if __name__ == "__main__":
    print("Excecution Successful")