import json
from pathlib import Path

from app.services.embedding_service import EmbeddingService
from app.services.chroma_service import ChromaService


json_file = Path("data/processed/Basis Pengetahuan & SOP Manajemen Tiket v.1.5 (2023).json")

with json_file.open("r", encoding="utf-8") as f:
    document = json.load(f)

chroma = ChromaService()

chunks = document["chunks"]

print(f"Total Chunks : {len(chunks)}")

for chunk in chunks:

    embedding = EmbeddingService.generate_embedding(
        chunk["text"]
    )

    chroma.add_document(

        chunk_id=chunk["id"],

        text=chunk["text"],

        embedding=embedding,

        metadata={

            "page": chunk["page"],

            "chunk": chunk["chunk"]

        }

    )

    print(
        f"{chunk['id']}"
    )