import { useState } from "react";
import api from "../Services/api";

function ResumeAnalysis() {
  const [resumeText, setResumeText] = useState("");
  const [analysis, setAnalysis] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setAnalysis(null);

    if (!resumeText.trim()) {
      setError("Please paste your resume text to analyze.");
      return;
    }

    setLoading(true);
    try {
      const response = await api.post("/rag/analyse-resume", {
        resume_text: resumeText,
      });
      setAnalysis(response.data.analysis);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to analyze resume. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="chat-panel">
      <div className="chat-header-panel">
        <h2>Resume Analysis</h2>
        <p>Paste your resume below to get insights into skills, strengths, and improvement areas.</p>
      </div>
      <form onSubmit={handleAnalyze} className="resume-analysis-form">
        <textarea
          className="resume-textarea"
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
          placeholder="Paste your resume text here..."
          rows={10}
        />
        <button type="submit" className="btn resume-analyze-button" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {error && (
        <div className="chat-window" style={{ marginTop: 20 }}>
          <p style={{ color: "#f87171", margin: 0 }}>{error}</p>
        </div>
      )}

      {analysis && (
        <div className="chat-window" style={{ marginTop: 20 }}>
          <div style={{ display: "flex", justifyContent: "space-between", gap: "18px", flexWrap: "wrap" }}>
            <h3 style={{ margin: 0, fontSize: "1.25rem", color: "#f8fafc" }}>Resume Analysis</h3>
            <span style={{ color: "#94a3b8", alignSelf: "center" }}>Insights generated from your resume text.</span>
          </div>
          <pre style={{ whiteSpace: "pre-wrap", marginTop: 18, color: "#e2e8f0", fontSize: "0.95rem", lineHeight: 1.75 }}>
            {analysis}
          </pre>
        </div>
      )}
    </section>
  );
}

export default ResumeAnalysis;

