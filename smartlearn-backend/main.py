import os
import re

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.llm import answer_from_pages
from services.pdf import extract_pages

app = FastAPI()

allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

documents = {}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/upload")
async def upload_pdf(
    chat_id: str = Query(..., description="Chat ID to store the document under"),
    file: UploadFile = File(..., description="PDF file to upload"),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    content = await file.read()

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty file is not allowed")

    try:
        pages = extract_pages(content)
    except ValueError:
        raise HTTPException(status_code=400, detail="PDF page count exceeds the limit of 30 pages")
    except Exception:
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    character_count = sum(len(p["text"]) for p in pages)

    if character_count == 0:
        raise HTTPException(
            status_code=422,
            detail="Scanned PDF without extractable text is not supported (OCR not available)",
        )

    documents[chat_id] = pages

    return {
        "page_count": len(pages),
        "character_count": character_count,
    }


class ChatRequest(BaseModel):
    chat_id: str
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    pages = documents.get(request.chat_id)
    if pages is None:
        raise HTTPException(status_code=404, detail="Chat session not found")

    answer = answer_from_pages(pages, request.message)

    citations: list[int] = []
    if "does not provide enough information" not in answer:
        page_refs = re.findall(r"\[Page (\d+)\]", answer)
        valid_pages = {p["page"] for p in pages}
        citations = sorted(set(
            int(p) for p in page_refs if int(p) in valid_pages
        ))

    return {"answer": answer, "citations": citations}
