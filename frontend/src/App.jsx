import { useState, useRef } from "react";
import "./App.css";

export default function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const inputRef = useRef();

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setResult(null);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (data.error) setError(data.raw);
      else setResult(data);
    } catch (e) {
      setError("Could not connect to backend. Make sure FastAPI is running.");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>🔍 AI Research Paper Skeptic Agent</h1>
      <p className="subtitle">Upload a research paper and get a critical skeptical review powered by local LLM.</p>

      <div className="upload-box" onClick={() => inputRef.current.click()}>
        <input ref={inputRef} type="file" accept=".pdf" hidden onChange={e => setFile(e.target.files[0])} />
        <p>📄 Click to upload a PDF</p>
        {file && <p className="filename">Selected: {file.name}</p>}
      </div>

      <button className="btn" onClick={handleAnalyze} disabled={!file || loading}>
        {loading ? "Analyzing... please wait (1-2 min)" : "Analyze Paper"}
      </button>

      {loading && <div className="spinner">🧠 Local LLM is reading the paper...</div>}

      {error && <div className="danger" style={{marginTop: 20}}>{error}</div>}

      {result && (
        <>
          <div className="card">
            <h2>📌 Main Claim</h2>
            <p>{result.main_claim}</p>
          </div>

          <div className="card">
            <h2>🔬 Method Summary</h2>
            <p>{result.method_summary}</p>
          </div>

          <div className="card">
            <h2>📊 Evidence for Claims</h2>
            {result.evidence_for_claims?.map((e, i) => (
              <div key={i} className="evidence-item">
                <p><strong>Claim:</strong> {e.claim}</p>
                <p style={{marginTop: 6}}><strong>Evidence:</strong> {e.evidence_found}</p>
                <span className={`badge ${e.evidence_strength}`}>{e.evidence_strength}</span>
              </div>
            ))}
          </div>

          <div className="card">
            <h2>⚠️ Limitations</h2>
            {result.limitations?.map((l, i) => <div key={i} className="warning">{l}</div>)}
          </div>

          <div className="card">
            <h2>❓ Questions to Ask</h2>
            <ul>{result.questions_to_ask?.map((q, i) => <li key={i}>{q}</li>)}</ul>
          </div>

          <div className="card">
            <h2>🚨 Unsupported Claims</h2>
            {result.unsupported_claims?.length > 0
              ? result.unsupported_claims.map((u, i) => <div key={i} className="danger">{u}</div>)
              : <div className="success">No unsupported claims detected.</div>}
          </div>
        </>
      )}
    </div>
  );
}