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

The extraction pipeline uses document formatting information instead of relying only on plain text.

For each extracted PDF line, the pipeline collects:

Text
Page number
Font size
Bold information
X/Y position
Line height

These signals are then used to distinguish likely headings from normal body content.

Heading Detection

A heading score is calculated using multiple signals.

Signals Used
Larger font size
Bold formatting
Shorter text length
Numbered heading patterns
Lettered heading patterns
Document layout information

For example, a line may receive a higher heading score when:

Font size is larger than normal body text
+
Text is bold
+
Text is relatively short

The final confidence value is limited to a range between 0 and 0.99.

Repeated Header and Footer Detection

Many PDF documents contain repeated content such as:

Company names
Document titles
Page information
Repeated footer text

The extractor checks text appearing near the top and bottom of pages and identifies text repeated across multiple pages.

Repeated elements are filtered before section construction.

Structured Output

The API returns structured JSON instead of returning a raw list of extracted lines.

Example:

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
Section Fields
Field	Description
heading	Detected heading
text	Body text associated with the heading
page	Page where the section starts
level	Heading hierarchy level
confidence	Confidence score for heading detection
Statistics
Field	Description
headings	Number of detected headings
sections	Number of generated sections
characters	Total extracted characters
body_font_size	Estimated body font size
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
Request Parameter
file: PDF document
Example Using curl
curl -X POST \
  https://comply-pdf-api.onrender.com/api/extract \
  -F "file=@sample.pdf"
Swagger API Documentation

When running locally, FastAPI provides interactive API documentation at:

http://127.0.0.1:8000/docs

The Swagger interface can be used to test the PDF extraction endpoint directly.

Running Locally
Backend

Open PowerShell and navigate to the backend:

cd backend

Create a virtual environment:

python -m venv .venv

Activate the virtual environment:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Start the FastAPI server:

uvicorn app.main:app --reload

The backend will run at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health
Frontend

Open another PowerShell terminal.

Navigate to the React application:

cd frontend\frontend

Install dependencies:

npm install

Start the development server:

npm run dev

Vite will display the local frontend URL.

Usually:

http://localhost:5173
Frontend Configuration

The frontend communicates with the deployed FastAPI backend using:

const API_URL = "https://comply-pdf-api.onrender.com";

The extraction request is sent to:

POST https://comply-pdf-api.onrender.com/api/extract
Production Deployment
Backend Deployment

The backend is deployed using Render.

Production API:

https://comply-pdf-api.onrender.com
Render Configuration
Root Directory:
backend

Build Command:
pip install -r requirements.txt

Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
Frontend Deployment

The frontend is deployed using Vercel.

Production frontend:

https://comply-assignment-git-main-vaishalis-projects-45ad94b1.vercel.app/
Vercel Configuration
Root Directory:
frontend/frontend

Framework:
Vite

Build Command:
npm run build

Output Directory:
dist

Install Command:
npm install
Scalability Considerations

The extraction logic is separated from the FastAPI API layer.

This makes it possible to extend the extraction pipeline independently from the frontend and API interface.

For larger production workloads, the architecture can be extended with:

Background PDF processing

Object storage
Database-backed document metadata
Job queues
Batch document processing
Authentication and authorization
Rate limiting
Caching
Structured logging
Monitoring and observability
Multiple extraction strategies
OCR for scanned documents

For example:

                 React
                   │
                   ▼
               FastAPI
                   │
                   ▼
             Job Queue
                   │
          ┌────────┴────────┐
          ▼                 ▼
     PDF Worker        PDF Worker
          │                 │
          └────────┬────────┘
                   ▼
              Object Store
                   │
                   ▼
                Database

This architecture allows PDF processing to scale independently as document volume increases.

Error Handling

The backend validates uploaded documents before processing.

The API checks:

File name
File extension
Empty uploads
PDF extraction failures

Invalid requests return appropriate HTTP errors.

The frontend displays extraction errors to the user instead of silently failing.

Security Considerations

The current implementation includes basic upload validation and temporary file cleanup.

For a production deployment, additional security controls should be implemented, including:

User authentication
Secure password storage
JWT or session-based authentication
File size limits
Content validation
Rate limiting
Secure object storage
Access control
Request logging
Monitoring
Protection against malicious documents
Per-user document isolation
Potential Future Enhancements

The application can be extended with additional document-processing capabilities.

Multi-document Processing

Allow users to upload multiple PDF filings and process them as a batch.

Search

Search across extracted filing content.

JSON Export

Allow users to download structured extraction results as JSON.

CSV Export

Convert structured filing data into CSV format for analysis.

PDF Preview

Display the original PDF next to the extracted structured content.

Advanced Heading Hierarchy

Detect multiple heading levels such as:

1. General Information
    1.1 Company Information
    1.2 Contact Information

2. Filing Information
    2.1 Filing Details
Document Comparison

Compare two filings and highlight differences.

Extraction History

Store previous extraction results for authenticated users.

OCR

Add OCR support for scanned PDFs that do not contain selectable text.

Technology Stack
Frontend
React
Vite
JavaScript
CSS
Lucide React
Backend
Python
FastAPI
PyMuPDF
Uvicorn
Deployment
GitHub
Render
Vercel

Assignment Coverage

Requirement	Implementation
PDF extraction	PyMuPDF-based extraction
Heading detection	Font, weight, position and text heuristics
Body text grouping	Text grouped under detected headings
Structured output	Heading + text + metadata
FastAPI endpoint	POST /api/extract
Health endpoint	GET /health
React UI	Upload and results dashboard
PDF validation	Frontend and backend validation
Error handling	HTTP errors + frontend messages
Responsive design	Responsive CSS
Backend deployment	Render
Frontend deployment	Vercel
Source control	GitHub
Design

The frontend uses a modern SaaS-style interface designed around the document extraction workflow.

The UI focuses on:

Clear upload interaction
Visual extraction status
Summary statistics
Structured section cards
Page references
Confidence indicators
Responsive layout

The goal is to make complex insurance filing documents easier to inspect and understand.

Future Authentication

Authentication is planned as an extension of the current architecture.

The intended flow is:

User
  │
  ▼
Login
  │
  ▼
Authentication API
  │
  ▼
Access Token
  │
  ▼
Authenticated Upload
  │
  ▼
PDF Extraction
  │
  ▼
User-specific Results

Authentication can be implemented using JWT or secure session-based authentication.

Author

Developed as part of the Comply take-home assignment.

GitHub

https://github.com/Vaishali-kale/comply-assignment

Live Application

https://comply-assignment-git-main-vaishalis-projects-45ad94b1.vercel.app/

API

https://comply-pdf-api.onrender.com/


### One thing to do now

After replacing the README, run:

powershell
cd C:\Users\ADMIN\Desktop\comply-assignment
git add README.md
git commit -m "Improve project documentation"
git push
