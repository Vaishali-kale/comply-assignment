# Comply PDF Extraction Pipeline

A full-stack PDF document extraction application built for the Comply take-home assignment.

The application accepts insurance filing PDFs, extracts their text, identifies likely headings using document formatting signals, and returns structured sections through a FastAPI backend. A React frontend provides a simple interface for uploading and reviewing the extracted content.

## Live Demo

Frontend:
https://comply-assignment-git-main-vaishalis-projects-45ad94b1.vercel.app/

Backend API:
https://comply-pdf-api.onrender.com/

Health Check:
https://comply-pdf-api.onrender.com/health

## GitHub Repository

https://github.com/Vaishali-kale/comply-assignment

---

## Features

### PDF Extraction

- Accepts PDF documents
- Extracts text using PyMuPDF
- Preserves page information
- Detects likely headings
- Groups body content under headings
- Removes repeated headers and footers
- Calculates heading confidence
- Returns structured JSON

### FastAPI Backend

- `POST /api/extract`
- `GET /health`
- PDF file validation
- Temporary file handling
- CORS support
- Error handling

### React Frontend

- PDF upload interface
- File validation
- Extraction progress state
- Extraction statistics
- Structured section display
- Page numbers
- Heading confidence
- Responsive UI

---

## Architecture

```text
                    ┌──────────────────────┐
                    │      React UI        │
                    │      Vercel          │
                    └──────────┬───────────┘
                               │
                               │ POST /api/extract
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI API      │
                    │       Render         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   PDF Extraction     │
                    │     PyMuPDF          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Structured Sections  │
                    │ heading + text +     │
                    │ page + confidence    │
                    └──────────────────────┘
Project Structure
comply-assignment/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── extractor.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── test_samples.py
│
├── frontend/
│   └── frontend/
│       ├── src/
│       │   ├── App.jsx
│       │   ├── main.jsx
│       │   └── styles.css
│       │
│       ├── package.json
│       ├── index.html
│       └── vite.config.js
│
├── docker-compose.yml
├── .gitignore
└── README.md
Extraction Approach

The extraction pipeline uses document-level formatting information rather than relying only on plain text.

For each PDF line, the extractor collects:

Text
Page number
Font size
Bold information
X/Y position
Line height
Heading Detection

A heading score is calculated using signals such as:

Larger font size
Bold formatting
Shorter text length
Numbered heading patterns
Lettered heading patterns

Repeated text appearing near the top or bottom of multiple pages is treated as a possible repeated header/footer and filtered out.

Structured Output

The API returns data in the following format:

{
  "filename": "example.pdf",
  "pages": 15,
  "sections": [
    {
      "heading": "General Information",
      "text": "Extracted section content...",
      "page": 3,
      "level": 1,
      "confidence": 0.95
    }
  ],
  "stats": {
    "headings": 10,
    "sections": 11,
    "characters": 12450,
    "body_font_size": 10
  }
}

The confidence value represents how strongly the formatting and text characteristics indicate that a line is a heading.

API
Health Check
GET /health

Example response:

{
  "status": "ok",
  "service": "comply-pdf-extractor"
}
Extract PDF
POST /api/extract
Content-Type: multipart/form-data

Parameter:

file: PDF document

Example using curl:

curl -X POST \
  https://comply-pdf-api.onrender.com/api/extract \
  -F "file=@sample.pdf"
Running Locally
Backend

Open PowerShell:

cd backend

Create a virtual environment:

python -m venv .venv

Activate it:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Start the API:

uvicorn app.main:app --reload

The API will run at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
Frontend

Open another terminal:

cd frontend\frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will be available at the URL shown by Vite, usually:

http://localhost:5173
Production Deployment
Backend

The backend is deployed on Render.

https://comply-pdf-api.onrender.com

Render configuration:

Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Frontend

The frontend is deployed on Vercel.

https://comply-assignment-git-main-vaishalis-projects-45ad94b1.vercel.app/

Vercel configuration:

Root Directory: frontend/frontend
Framework: Vite
Build Command: npm run build
Output Directory: dist
Install Command: npm install
Scalability Considerations

The extraction logic is separated from the API layer, allowing the extraction pipeline to evolve independently.

For larger production workloads, the architecture can be extended with:

Background PDF processing
Object storage for uploaded documents
Database-backed document metadata
Job queues for large documents
Batch document processing
Authentication and authorization
Rate limiting
Caching
Observability and structured logging
Multiple extraction strategies for different document types

This allows the application to process many documents without coupling document extraction directly to the frontend.

Potential Future Enhancements

Possible extensions include:

Multi-document upload
Search across extracted filings
Download extracted JSON
Export to CSV
Side-by-side PDF and extracted content
Heading hierarchy detection
Document comparison
Search and filtering
Extraction history
User-specific document libraries
More advanced OCR support for scanned PDFs
Technology Stack
Frontend
React
Vite
JavaScript
CSS
Backend
Python
FastAPI
PyMuPDF
Uvicorn
Deployment
Vercel
Render
GitHub
Error Handling

The API validates:

File name
PDF extension
Empty uploads
Extraction failures

Errors are returned using appropriate HTTP responses and displayed by the frontend.

Security Considerations

For a production version, the application should additionally implement:

User authentication
Secure password storage
JWT/session management
File size limits
Content validation
Rate limiting
Secure object storage
Request logging and monitoring
Access control for uploaded documents
Assignment Coverage
Requirement	Implementation
PDF extraction	PyMuPDF-based extraction
Heading detection	Font, weight, position and text heuristics
Structured output	Heading + text sections
FastAPI endpoint	/api/extract
React UI	Upload and results dashboard
Responsive design	CSS responsive layout
Deployment	Vercel + Render
Git repository	GitHub
Author

Developed as part of the Comply take-home assignment.

GitHub:

https://github.com/Vaishali-kale/comply-assignment


### One important correction before submission

The README above accurately describes your **current implementation**, but the assignment specifically requires **login**. Your current backend code does not yet have authentication.

So **don't submit yet**.

Next we should add:

**Login → JWT authentication → Upload PDF → Extract → Results**

Then I'll help you update the README's authentication section and do a final submission checklist.
