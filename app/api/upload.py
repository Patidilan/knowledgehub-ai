from pathlib import Path
import shutil

from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    pdf_files = sorted(UPLOAD_DIR.glob("*.pdf"))

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "files": pdf_files
    }
)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are allowed."}

    save_path = UPLOAD_DIR / file.filename

    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return RedirectResponse("/", status_code=303)