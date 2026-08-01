from pathlib import Path
import shutil

from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.pdf_service import PDFService
from fastapi import HTTPException
from urllib.parse import quote

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)




@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    message: str = None,
    status: str = None
):

    pdf_files = sorted(UPLOAD_DIR.glob("*.pdf"))

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "files": pdf_files,
            "message": message,
            "status": status
        }
    )


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are allowed."}


    existing_files = {
        f.name.lower()
        for f in UPLOAD_DIR.glob("*.pdf")
    }

    if file.filename.lower() in existing_files:
        return RedirectResponse(
            url=f"/?status=error&message={quote('Document already exists!')}",
            status_code=303
        )

    save_path = UPLOAD_DIR / file.filename

    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract PDF
    document = PDFService.extract_text(save_path)

    print("=" * 60)
    print(f"Filename : {document['filename']}")
    print(f"Pages    : {document['total_pages']}")

    if document["pages"]:
        print("\nPreview:\n")
        print(document["pages"][0]["text"][:500])
        
    chunks = PDFService.chunk_document(document)

    json_file = PDFService.save_document(
        document=document,
        chunks=chunks
    )

    print("=" * 60)
    print(f"Total Chunks : {len(chunks)}")

    print("\nFirst Chunk Metadata:")
    print(chunks[0])

    print("\nFirst Chunk Text:")
    print(chunks[0]["text"])
    
    print("=" * 60)
    print(f"JSON Saved : {json_file}")

    return RedirectResponse(
        url=f"/?status=success&message={quote('Document uploaded successfully!')}",
        status_code=303
    )