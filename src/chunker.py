import re

def is_malayalam(text: str) -> bool:
    """Check if text contains Malayalam Unicode characters (U+0D00–U+0D7F)."""
    return bool(re.search(r'[\u0D00-\u0D7F]', text))

def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    """
    Chunk text respecting Malayalam sentence boundaries.
    Malayalam sentences often end with '।' (danda) or newlines.
    """
    # Split on Malayalam danda, newlines, or full stops
    sentences = re.split(r'(?<=[।\.\n])\s+', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # If adding this sentence exceeds chunk_size, save current and start new
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Overlap: keep last `overlap` characters for context continuity
            current_chunk = current_chunk[-overlap:] + " " + sentence
        else:
            current_chunk += " " + sentence
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def chunk_pages(pages: list[dict], **kwargs) -> list[dict]:
    """Convert pages to overlapping chunks with metadata."""
    all_chunks = []
    for page in pages:
        chunks = chunk_text(page["text"], **kwargs)
        for j, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": page["source"],
                "page_num": page["page_num"],
                "chunk_id": f"{page['source']}_p{page['page_num']}_c{j}",
                "is_malayalam": is_malayalam(chunk)
            })
    return all_chunks

if __name__ == "__main__":
    print("Excecution Successful")