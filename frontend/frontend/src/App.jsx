import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    setError("");
    setResult(null);

    if (!selectedFile) {
      setFile(null);
      return;
    }

    if (!selectedFile.name.toLowerCase().endsWith(".pdf")) {
      setError("Please select a PDF file.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const extractDocument = async () => {
    if (!file) {
      setError("Please select a PDF first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_URL}/api/extract`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Extraction failed.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      {/* Header */}
      <header className="header">
        <div className="logo">
          <span className="logo-mark">C</span>
          <span>Comply</span>
        </div>

        <div className="header-badge">
          AI Document Extraction
        </div>
      </header>

      {/* Main */}
      <main className="container">

        <section className="hero">
          <p className="eyebrow">INSURANCE FILING INTELLIGENCE</p>

          <h1>
            Turn complex PDF filings into
            <span> structured data.</span>
          </h1>

          <p className="subtitle">
            Upload an insurance filing and automatically identify
            headings, sections and document content.
          </p>
        </section>

        {/* Upload Card */}
        <section className="upload-card">

          <div className="upload-icon">
            ↑
          </div>

          <h2>Upload your PDF</h2>

          <p>
            Select an insurance filing to extract its structure.
          </p>

          <label className="file-button">
            Choose PDF
            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
            />
          </label>

          {file && (
            <div className="selected-file">
              <strong>{file.name}</strong>
              <span>
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </span>
            </div>
          )}

          <button
            className="extract-button"
            onClick={extractDocument}
            disabled={!file || loading}
          >
            {loading ? "Extracting..." : "Extract Document"}
          </button>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

        </section>

        {/* Results */}
        {result && (
          <section className="results">

            <div className="results-header">
              <div>
                <p className="eyebrow">EXTRACTION COMPLETE</p>
                <h2>{result.filename}</h2>
              </div>

              <div className="stats">
                <div>
                  <strong>{result.pages}</strong>
                  <span>Pages</span>
                </div>

                <div>
                  <strong>{result.stats?.headings || 0}</strong>
                  <span>Headings</span>
                </div>

                <div>
                  <strong>{result.stats?.sections || 0}</strong>
                  <span>Sections</span>
                </div>
              </div>
            </div>

            <div className="sections">

              {result.sections?.map((section, index) => (
                <article
                  className="section-card"
                  key={index}
                >

                  <div className="section-top">

                    <span className="section-number">
                      {String(index + 1).padStart(2, "0")}
                    </span>

                    <div>
                      <h3>{section.heading}</h3>

                      <div className="section-meta">
                        <span>
                          Page {section.page}
                        </span>

                        <span>
                          Confidence {Math.round(
                            section.confidence * 100
                          )}%
                        </span>
                      </div>
                    </div>

                  </div>

                  <p>{section.text}</p>

                </article>
              ))}

            </div>

          </section>
        )}

      </main>

      <footer>
        Comply PDF Extraction Pipeline
      </footer>

    </div>
  );
}

export default App;