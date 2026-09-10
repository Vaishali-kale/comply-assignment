from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .extractor import extract_pdf

import tempfile
import os


app = FastAPI(
    title="Comply PDF Extraction API",
    version="1.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# -------------------------
# Health Check
# -------------------------

@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "comply-pdf-extractor"
    }


# -------------------------
# PDF Extraction
# -------------------------

@app.post("/api/extract")
async def extract_document(
    file: UploadFile = File(...)
):

    # Check filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required"
        )

    # Check PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Read uploaded file
    contents = await file.read()

    # Check empty file
    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    temp_path = None

    try:

        # Create temporary PDF
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(contents)

            temp_path = temp_file.name

        # Extract PDF
        result = extract_pdf(temp_path)

        # Return structured JSON
        return result

    except Exception as e:

        raise HTTPException(
            status_code=422,
            detail=f"Could not extract PDF: {str(e)}"
        )

    finally:

        # Delete temporary file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)