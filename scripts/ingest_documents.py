from pathlib import Path
from app.services.embedding_service import EmbeddingService
from app.services.chroma_service import ChromaService
import json
from app.services.pdf_service import PDFService

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("data/processed")

pdf_files = sorted(UPLOAD_DIR.glob("*.pdf"))

print("=" * 60)
print("KnowledgeHub AI - Document Ingestion")
print("=" * 60)

processed = 0
skipped = 0

for pdf in pdf_files:

    print(f"\n{pdf.name}")

    json_path = OUTPUT_DIR / f"{pdf.stem}.json"

    # Skip jika JSON sudah ada
    if json_path.exists():
        print("JSON already exists. Skip.")
        skipped += 1
        continue

    # Extract
    document = PDFService.extract_text(pdf)
    print(f"Pages  : {document['total_pages']}")

    # Chunk
    chunks = PDFService.chunk_document(document)
    print(f"Chunks : {len(chunks)}")

    # Save JSON
    json_file = PDFService.save_document(
        document=document,
        chunks=chunks
    )

    print(f"✓ JSON Saved : {json_file}")
    
    # ==========================
    # Generate Embedding
    # ==========================

    embedding = EmbeddingService()

    chroma = ChromaService()

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Generating Embeddings...")

    for chunk in data["chunks"]:

        vector = embedding.generate_embedding(chunk["text"])

        chroma.add_document(
            id=chunk["id"],
            document=chunk["text"],
            embedding=vector,
            metadata={
                "document": pdf.name,
                "page": chunk["page"],
                "chunk": chunk["chunk"]
            }
        )

    print(f"Stored {len(data['chunks'])} embeddings")

    processed += 1

print("\n" + "=" * 60)
print(f"Total PDF       : {len(pdf_files)}")
print(f"Processed       : {processed}")
print(f"Skipped         : {skipped}")
print("=" * 60)