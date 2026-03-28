from pathlib import Path
from tqdm import tqdm
from src.extractor import extract_pdf
from src.chunker import chunk_pages
from src.embedder import MalayalamEmbedder
from src.indexer import get_chroma_client, get_or_create_collection, index_chunks

PDF_DIR = "./pdfs"
CHROMA_DIR = "./chroma_db"

def ingest_all():
    embedder = MalayalamEmbedder()
    client = get_chroma_client(CHROMA_DIR)
    collection = get_or_create_collection(client)
    
    pdf_files = list(Path(PDF_DIR).glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDFs to ingest")
    
    for pdf_path in tqdm(pdf_files, desc="Processing PDFs"):
        try:
            # Step 1: Extract
            pages = extract_pdf(str(pdf_path))
            if not pages:
                print(f"No text extracted from {pdf_path.name}")
                continue
            
            # Step 2: Chunk
            chunks = chunk_pages(pages, chunk_size=512, overlap=64)
            print(f"  → {len(chunks)} chunks from {pdf_path.name}")
            
            # Step 3: Embed + Index
            index_chunks(collection, chunks, embedder)
        
        except Exception as e:
            print(f"Error processing {pdf_path.name}: {e}")
    
    print(f"\nDone! Total docs in ChromaDB: {collection.count()}")

if __name__ == "__main__":
    ingest_all()