# Comply PDF Extraction System

A full-stack document intelligence application built for the Comply take-home assignment.

The application allows users to securely log in, upload insurance filing PDFs, extract structured content, and view detected headings, sections, page numbers, and confidence scores through a modern React interface.

## Live Demo

### Frontend
https://comply-assignment-git-main-vaishalis-projects-45ad94b1.vercel.app/

### Backend API
https://comply-pdf-api.onrender.com

### API Documentation
https://comply-pdf-api.onrender.com/docs

### GitHub
https://github.com/Vaishali-kale/comply-assignment

---

## Features

- Secure demo login using JWT authentication
- PDF document upload
- PDF text extraction using PyMuPDF
- Automatic heading and body-text detection
- Structured section extraction
- Page number tracking
- Confidence scoring
- Extraction statistics
- Responsive React interface
- FastAPI backend
- REST API
- Production deployment using Vercel and Render
- CORS-enabled frontend/backend communication
- Validation for PDF uploads
- Authentication-protected extraction endpoint
- Temporary file handling with cleanup

---

## Application Flow

```text
User
  |
  v
React Frontend
  |
  | Login
  v
FastAPI Authentication
  |
  | JWT Token
  v
Authenticated Workspace
  |
  | Upload PDF
  v
FastAPI Extraction API
  |
  v
PyMuPDF
  |
  v
Heading / Body Detection
  |
  v
Structured JSON
  |
  v
React Results Dashboard


Technology Stack
Frontend
React
Vite
JavaScript
CSS
Responsive UI
Backend
Python
FastAPI
Uvicorn
PyMuPDF
PyJWT
python-multipart
Deployment
Vercel — Frontend
Render — Backend
GitHub — Source Control


Project Structure

comply-assignment/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── extractor.py
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── test_samples.py
│
├── frontend/
│   └── frontend/
│       ├── src/
│       │   ├── App.jsx
│       │   ├── App.css
│       │   ├── styles.css
│       │   └── main.jsx
│       │
│       ├── package.json
│       ├── index.html
│       └── vite.config.js
│
├── docker-compose.yml
├── README.md
└── .gitignore

Authentication

The application includes JWT-based authentication.

Demo Credentials
Email: demo@comply.ai
Password: Comply@123

The login endpoint returns a JWT access token.

POST /api/auth/login

The extraction endpoint requires a valid Bearer token.

POST /api/extract
Authorization: Bearer <token>

For production environments, authentication credentials and the JWT secret should be supplied through environment variables rather than committed to source control.

PDF Extraction

The backend accepts PDF files through the extraction API.

POST /api/extract

The uploaded document is temporarily stored, processed using PyMuPDF, and removed after extraction.

The extraction pipeline identifies document structure and returns structured information rather than only returning raw PDF text.

Structured Output

The API returns structured JSON containing information such as:

{
  "filename": "example.pdf",
  "pages": 15,
  "sections": [
    {
      "heading": "General Information",
      "text": "Extracted section content...",
      "page": 3,
      "confidence": 0.95
    }
  ],
  "stats": {
    "headings": 10,
    "sections": 10
  }
}

This structure makes the extracted document easier for downstream applications to consume.

Heading Detection

The extraction pipeline uses PDF text and layout information to identify likely headings.

Signals used by the extraction process can include:

Font size
Text formatting
Text length
Position
Capitalization
Layout characteristics
Section boundaries

The objective is to distinguish meaningful document headings from normal body text.

Error Handling

The API validates uploaded documents before processing.

Examples include:

Missing file
Empty file
Non-PDF file
Invalid authentication token
Expired authentication token
Invalid login credentials
PDF extraction failures

The API returns appropriate HTTP error responses for invalid requests.

API Endpoints
Method	Endpoint	Description	Authentication
GET	/health	Health check	No
POST	/api/auth/login	Authenticate user	No
POST	/api/extract	Extract PDF content	JWT

Interactive API documentation:

https://comply-pdf-api.onrender.com/docs

Running Locally
Backend

Navigate to the backend:

cd backend

Install dependencies:

pip install -r requirements.txt

Start the API:

uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
Frontend

Navigate to the frontend:

cd frontend/frontend

Install dependencies:

npm install

Start the development server:

npm run dev
Deployment
Backend — Render

The backend is deployed as a Python web service.

Root Directory:
backend

Build command:

pip install -r requirements.txt

Start command:

uvicorn app.main:app --host 0.0.0.0 --port $PORT
Frontend — Vercel

The React/Vite application is deployed on Vercel.

Because the repository contains a nested frontend directory, the Vercel project uses:

frontend/frontend

as its Root Directory.

Scalability Considerations

The extraction service is designed so that the API layer and extraction logic are separated.

FastAPI
   |
   v
Extraction Service
   |
   v
PyMuPDF

This makes it possible to extend the system with additional processing stages.

Potential production improvements include:

Background processing for large documents
Job queues
Object storage for uploaded documents
Database-backed document history
Batch document processing
Pagination for large extraction results
Caching
Rate limiting
Role-based access control
Persistent authentication
Observability and monitoring
Design

The frontend focuses on a clean document-intelligence workflow:

Sign in
Upload a PDF
Start extraction
View extraction statistics
Review structured sections

The interface is responsive and designed to make extracted document structure easy to scan.

Assignment Coverage
Requirement	Implementation
Python PDF extraction	PyMuPDF extraction pipeline
Heading/body distinction	Layout and text-based detection
Structured output	JSON section objects
FastAPI endpoint	/api/extract
File upload	Multipart PDF upload
Login	JWT authentication
React UI	React + Vite
Document upload UI	Implemented
Results display	Implemented
Live deployment	Vercel + Render
Git repository	GitHub
API documentation	FastAPI Swagger
Security Notes

The project uses JWT authentication for protected extraction requests.

For a production system, secrets should be configured through environment variables:

SECRET_KEY
DEMO_EMAIL
DEMO_PASSWORD

Secrets should never be committed to GitHub.

Additional production security measures can include:

HTTPS
Secure token storage
Short-lived access tokens
Refresh tokens
Rate limiting
File size limits
Malware scanning
Restricted CORS origins
User and role management
Future Enhancements

Potential improvements include:

Search within extracted sections
Download extracted JSON
Document history
Batch PDF processing
AI-generated document summaries
Automatic metadata extraction
Table extraction
Named entity extraction
Advanced document classification
Background processing for large PDFs
Multi-user workspaces
Author

Vaishali Kale

GitHub:

https://github.com/Vaishali-kale

Submission Links

Live Application:
https://comply-assignment-git-main-vaishalis-projects-45ad94b1.vercel.app/

Backend API:
https://comply-pdf-api.onrender.com

Swagger API Documentation:
https://comply-pdf-api.onrender.com/docs

Source Code:
https://github.com/Vaishali-kale/comply-assignment


### Then commit it

At the bottom of GitHub, enter a commit message:


Update README with authentication and deployment details

