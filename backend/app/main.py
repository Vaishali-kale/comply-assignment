from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from .extractor import extract_pdf

import tempfile
import os
import jwt
from datetime import datetime, timedelta, timezone


# ============================================================
# Configuration
# ============================================================

SECRET_KEY = os.getenv("SECRET_KEY", "comply-demo-secret-change-in-production")
ALGORITHM = "HS256"

DEMO_EMAIL = os.getenv("DEMO_EMAIL", "demo@comply.ai")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "Comply@123")


# ============================================================
# FastAPI App
# ============================================================

app = FastAPI(
    title="Comply PDF Extraction API",
    version="1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Authentication
# ============================================================

security = HTTPBearer()


class LoginRequest(BaseModel):
    email: str
    password: str


def create_access_token(email: str):
    expires = datetime.now(timezone.utc) + timedelta(hours=8)

    payload = {
        "sub": email,
        "exp": expires,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

        return email

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Authentication token has expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "comply-pdf-extractor"
    }


# ============================================================
# Login
# ============================================================

@app.post("/api/auth/login")
def login(request: LoginRequest):

    if (
        request.email != DEMO_EMAIL
        or request.password != DEMO_PASSWORD
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(request.email)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "email": request.email
        }
    }


# ============================================================
# PDF Extraction
# ============================================================

@app.post("/api/extract")
async def extract_document(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required"
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(contents)
            temp_path = temp_file.name

        result = extract_pdf(temp_path)

        # Return the original uploaded filename
        result["filename"] = file.filename

        # Information about authenticated user
        result["uploaded_by"] = current_user

        return result

    except Exception as e:

        raise HTTPException(
            status_code=422,
            detail=f"Could not extract PDF: {str(e)}"
        )

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)