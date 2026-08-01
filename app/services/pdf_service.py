from pathlib import Path
import fitz
import re
import json

class PDFService:
    

    @staticmethod
    def extract_text(pdf_path: Path):

        document = fitz.open(pdf_path)

        pages = []

        for page_number, page in enumerate(document, start=1):

            pages.append(
                {
                    "page": page_number,
                    "text": PDFService.clean_text(page.get_text())
                }
            )

        result = {
            "filename": pdf_path.name,
            "total_pages": len(pages),
            "pages": pages
        }

        document.close()

        return result
    
    @staticmethod
    def chunk_document(document, chunk_size=500, overlap=100):

        chunks = []
        chunk_id = 1

        chunk_id = 1

        for page in document["pages"]:

            text = page["text"]

            start = 0

            local_chunk = 1

            while start < len(text):

                end = start + chunk_size

                chunk_text = text[start:end]

                chunks.append(
                    {
                        "id": f"chunk_{chunk_id:05}",
                        "page": page["page"],
                        "chunk": local_chunk,
                        "length": len(chunk_text),
                        "text": chunk_text
                    }
                )

                chunk_id += 1
                local_chunk += 1

                start += chunk_size - overlap

        return chunks
    
    @staticmethod
    def clean_text(text: str) -> str:
    
        text = text.replace("\xa0", " ")

        text = re.sub(r"[ \t]+", " ", text)

        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()
    
    
    @staticmethod
    def save_document(document: dict, chunks: list):

        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = Path(document["filename"]).stem + ".json"

        output_file = output_dir / filename

        payload = {
            "filename": document["filename"],
            "total_pages": document["total_pages"],
            "total_chunks": len(chunks),
            "chunks": chunks
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                payload,
                f,
                ensure_ascii=False,
                indent=4
            )

        return output_file