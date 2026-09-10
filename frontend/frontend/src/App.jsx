import { useState } from "react";
import "./App.css";

const API_URL = "https://comply-pdf-api.onrender.com";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");

  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [loginLoading, setLoginLoading] = useState(false);
  const [error, setError] = useState("");

  // =========================
  // LOGIN
  // =========================

  const handleLogin = async (event) => {
    event.preventDefault();

    setError("");
    setLoginLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Invalid email or password");
      }

      setToken(data.access_token);
      setLoggedIn(true);
      setEmail(data.user.email);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoginLoading(false);
    }
  };

  // =========================
  // FILE SELECTION
  // =========================

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    setError("");
    setResult(null);

    if (!selectedFile) {
      setFile(null);
      return;
    }

    if (selectedFile.type !== "application/pdf") {
      setError("Please select a PDF file.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  // =========================
  // PDF EXTRACTION
  // =========================

  const extractDocument = async () => {
    if (!file) {
      setError("Please select a PDF first.");
      return;
    }

    if (!token) {
      setError("Your session has expired. Please login again.");
      setLoggedIn(false);
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
        headers: {
          Authorization: `Bearer ${token}`,
        },
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

  // =========================
  // LOGOUT
  // =========================

  const logout = () => {
    setLoggedIn(false);
    setToken("");
    setFile(null);
    setResult(null);
    setPassword("");
    setError("");
  };

  // =========================
  // LOGIN SCREEN
  // =========================

  if (!loggedIn) {
    return (
      <div className="login-page">
        <div className="login-background">
          <div className="orb orb-one"></div>
          <div className="orb orb-two"></div>
          <div className="orb orb-three"></div>
        </div>

        <div className="login-card">
          <div className="brand">
            <div className="brand-icon">C</div>
            <div>
              <h1>Comply</h1>
              <span>Document Intelligence</span>
            </div>
          </div>

          <div className="login-heading">
            <p className="eyebrow">WELCOME BACK</p>
            <h2>Sign in to your workspace</h2>
            <p>
              Extract and structure filing documents with ease.
            </p>
          </div>

          <form onSubmit={handleLogin}>
            <label>Email address</label>

            <input
              type="email"
              placeholder="demo@comply.ai"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />

            <label>Password</label>

            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            <button
              className="login-button"
              type="submit"
              disabled={loginLoading}
            >
              {loginLoading ? "Signing in..." : "Sign In →"}
            </button>
          </form>

          <div className="demo-hint">
            <strong>Demo access</strong>
            <span>demo@comply.ai</span>
          </div>

          <div className="login-footer">
            Secure document extraction workspace
          </div>
        </div>
      </div>
    );
  }

  // =========================
  // MAIN APPLICATION
  // =========================

  return (
    <div className="app">

      <header className="header">
        <div className="header-brand">
          <div className="brand-icon small">C</div>

          <div>
            <strong>Comply</strong>
            <span>Document Intelligence</span>
          </div>
        </div>

        <div className="user-area">
          <div className="user-info">
            <span>Signed in as</span>
            <strong>{email}</strong>
          </div>

          <button
            className="logout-button"
            onClick={logout}
          >
            Logout
          </button>
        </div>
      </header>

      <main className="container">

        <section className="hero">
          <div className="hero-badge">
            ✦ AI-READY DOCUMENT EXTRACTION
          </div>

          <h1>
            Turn complex PDF filings
            <span> into structured data.</span>
          </h1>

          <p>
            Upload an insurance filing and automatically identify
            headings, sections, and document content.
          </p>
        </section>

        <section className="upload-card">

          <div className="upload-icon">
            ↑
          </div>

          <h2>Upload your filing</h2>

          <p>
            Select a PDF document to begin extraction.
          </p>

          <label className="file-picker">
            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
            />

            <span>
              {file ? file.name : "Choose PDF file"}
            </span>
          </label>

          {file && (
            <div className="selected-file">
              <span>PDF</span>

              <div>
                <strong>{file.name}</strong>
                <small>
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </small>
              </div>
            </div>
          )}

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button
            className="extract-button"
            onClick={extractDocument}
            disabled={loading || !file}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Extracting document...
              </>
            ) : (
              <>
                Extract Document →
              </>
            )}
          </button>

        </section>

        {result && (
          <section className="results">

            <div className="results-header">

              <div>
                <p className="eyebrow">
                  EXTRACTION COMPLETE
                </p>

                <h2>{result.filename}</h2>

                <p className="result-subtitle">
                  Structured filing content successfully extracted.
                </p>
              </div>

              <div className="stats">

                <div className="stat">
                  <strong>{result.pages}</strong>
                  <span>Pages</span>
                </div>

                <div className="stat">
                  <strong>
                    {result.stats?.headings || 0}
                  </strong>
                  <span>Headings</span>
                </div>

                <div className="stat">
                  <strong>
                    {result.stats?.sections || 0}
                  </strong>
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

                    <div className="section-number">
                      {String(index + 1).padStart(2, "0")}
                    </div>

                    <div className="section-heading">
                      <h3>{section.heading}</h3>

                      <div className="section-meta">
                        <span>
                          Page {section.page}
                        </span>

                        <span>
                          Confidence{" "}
                          {Math.round(
                            (section.confidence || 0) * 100
                          )}
                          %
                        </span>
                      </div>
                    </div>

                  </div>

                  <p className="section-text">
                    {section.text || "No body text detected."}
                  </p>

                </article>

              ))}

            </div>

          </section>
        )}

      </main>

      <footer>
        Comply PDF Extraction Pipeline · Secure document intelligence
      </footer>

    </div>
  );
}

export default App;