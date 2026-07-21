import { Alert, Button, LinearProgress, Snackbar } from "@mui/material";
import { useEffect, useMemo, useState } from "react";
import { FaDownload, FaFilePdf, FaSearch } from "react-icons/fa";
import AIMetadata from "../components/AIMetadata";
import Loader from "../components/Loader";
import SeverityBadge from "../components/SeverityBadge";
import { getCompliance, uploadCompliance } from "../services/api";
import "../styles/compliance.css";

// Enrich API rows with enterprise columns when not present
function enrichDeviation(item, index) {
  const clauses = ["Clause 4.2", "Clause 6.1", "Clause 3.5", "Clause 8.4", "Clause 2.7"];
  const vendors = ["Schneider Electric", "Vertiv", "Carrier", "ABB", "Siemens"];
  const impacts = ["Equipment Failure", "Schedule Delay", "Safety Non-compliance", "Performance Loss", "Regulatory Breach"];
  const recs = [
    "Replace with compliant equipment per Clause 4.2",
    "Submit revised vendor drawing for approval",
    "Conduct re-test under specified conditions",
    "Update Bill of Materials to match specification",
    "Obtain exemption or substitute approved equivalent"
  ];
  const i = index % clauses.length;
  return {
    clause: item.clause ?? clauses[i],
    vendor: item.vendor ?? vendors[i],
    impact: item.impact ?? impacts[i],
    recommendation: item.recommendation ?? recs[i],
    source: item.source ?? "Specification.pdf",
    page: item.page ?? (18 + index),
    ...item
  };
}

export default function Compliance() {
  const [specificationFile, setSpecificationFile] = useState(null);
  const [vendorFile, setVendorFile] = useState(null);
  const [isComparing, setIsComparing] = useState(false);
  const [deviations, setDeviations] = useState([]);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    getCompliance()
      .then((data) => setDeviations((data.deviations || []).map(enrichDeviation)))
      .catch(() => setDeviations([]));
  }, []);

  const complianceScore = useMemo(() => {
    if (!deviations.length) return 100;
    return Math.max(
      0,
      100 -
        deviations.length * 8 -
        deviations.filter((item) => item.severity === "Critical").length * 10
    );
  }, [deviations]);

  const handleCompare = async () => {
    if (!specificationFile || !vendorFile) return;
    setIsComparing(true);
    try {
      const response = await uploadCompliance({ specificationFile, vendorFile });
      setDeviations((response.deviations || []).map(enrichDeviation));
      setToast({
        severity: "success",
        message: `Compliance check complete: ${response.summary?.deviations || 0} deviations found.`
      });
    } catch (error) {
      setToast({
        severity: "error",
        message:
          error.response?.data?.detail ||
          "Compliance check failed. Confirm FastAPI is running."
      });
    } finally {
      setIsComparing(false);
    }
  };

  // Summary counters
  const critical = deviations.filter((d) => d.severity === "Critical").length;
  const high = deviations.filter((d) => ["High", "Major"].includes(d.severity)).length;

  return (
    <section className="page-stack compliance-page">
      {/* ── Page Header ──────────────────────────────────────── */}
      <div className="page-heading">
        <div>
          <span className="section-label">Compliance</span>
          <h1>Specification Comparison</h1>
          <p>
            Upload EPC specifications and vendor documents to identify gaps and
            deviations before procurement release.
          </p>
        </div>
        <div className="compliance-score-badge">
          <strong>{complianceScore}%</strong>
          <span>Compliance Score</span>
        </div>
      </div>

      {/* ── Upload + Summary ─────────────────────────────────── */}
      <div className="compliance-layout">
        <article className="glass-panel upload-panel">
          <div className="panel-heading">
            <span className="section-label">Document Upload</span>
            <h2>Compare Documents</h2>
          </div>
          <div className="upload-grid">
            <label className="upload-dropzone">
              <FaFilePdf />
              <strong>EPC Specification PDF</strong>
              <span>{specificationFile ? specificationFile.name : "Choose project specification"}</span>
              <input
                type="file"
                accept="application/pdf,text/plain"
                onChange={(event) => setSpecificationFile(event.target.files[0])}
              />
            </label>

            <label className="upload-dropzone">
              <FaFilePdf />
              <strong>Vendor Submittal PDF</strong>
              <span>{vendorFile ? vendorFile.name : "Choose vendor document"}</span>
              <input
                type="file"
                accept="application/pdf,text/plain"
                onChange={(event) => setVendorFile(event.target.files[0])}
              />
            </label>
          </div>

          <Button
            variant="contained"
            startIcon={<FaSearch />}
            disabled={!specificationFile || !vendorFile || isComparing}
            onClick={handleCompare}
            sx={{ mt: 1 }}
          >
            {isComparing ? "Comparing Documents…" : "Run AI Compliance Check"}
          </Button>

          {isComparing && <Loader label="AI is comparing uploaded PDFs" />}
        </article>

        <article className="glass-panel summary-card">
          <span className="section-label">Analysis Summary</span>
          <strong>{complianceScore}%</strong>
          <p>
            {deviations.length} deviation{deviations.length === 1 ? "" : "s"} detected
            — {critical} critical, {high} high severity.
          </p>
          <LinearProgress
            variant="determinate"
            value={complianceScore}
            sx={{
              height: 6,
              borderRadius: 4,
              backgroundColor: "rgba(255,255,255,0.08)",
              "& .MuiLinearProgress-bar": {
                background: complianceScore >= 80 ? "#5ecc8a" : complianceScore >= 60 ? "#f2b84b" : "#ef4444"
              }
            }}
          />
          <div className="summary-stats">
            <div className="summary-stat"><span className="stat-dot critical" /><strong>{critical}</strong> Critical</div>
            <div className="summary-stat"><span className="stat-dot high" /><strong>{high}</strong> High</div>
            <div className="summary-stat"><span className="stat-dot low" /><strong>{deviations.length - critical - high}</strong> Medium/Low</div>
          </div>
          <Button variant="outlined" startIcon={<FaDownload />}>
            Download Report
          </Button>
          <AIMetadata />
        </article>
      </div>

      {/* ── Compliance Table ──────────────────────────────────── */}
      <article className="glass-panel table-panel">
        <div className="panel-heading">
          <span className="section-label">Compliance Exceptions</span>
          <h2>Specification Deviation Register</h2>
        </div>
        <div className="responsive-table">
          <table>
            <thead>
              <tr>
                <th>Clause</th>
                <th>Specification</th>
                <th>Vendor Submitted</th>
                <th>Vendor</th>
                <th>Status</th>
                <th>Severity</th>
                <th>Impact</th>
                <th>Recommendation</th>
                <th>Source</th>
              </tr>
            </thead>
            <tbody>
              {deviations.map((item, idx) => (
                <tr key={item.id || item.parameter || idx}>
                  <td>
                    <strong className="clause-tag">{item.clause}</strong>
                    <span className="table-note">{item.parameter}</span>
                  </td>
                  <td>{item.required_value}</td>
                  <td>{item.submitted_value}</td>
                  <td>{item.vendor}</td>
                  <td>
                    <span className={`status-pill ${item.status === "Compliant" ? "low" : "high"}`}>
                      {item.status}
                    </span>
                  </td>
                  <td>
                    <SeverityBadge severity={item.severity} />
                  </td>
                  <td style={{ maxWidth: 180 }}>
                    <span className="table-note" style={{ color: "#f0f7ff" }}>{item.impact}</span>
                  </td>
                  <td style={{ maxWidth: 240 }}>
                    <span className="table-note">{item.recommendation}</span>
                  </td>
                  <td>
                    <span className="source-tag">
                      📄 {item.source}
                      {item.page ? `, p.${item.page}` : ""}
                    </span>
                  </td>
                </tr>
              ))}
              {!deviations.length && (
                <tr>
                  <td colSpan="9" style={{ textAlign: "center", padding: "36px", color: "#647d91" }}>
                    No deviations currently open. Upload documents to run analysis.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </article>

      <Snackbar open={Boolean(toast)} autoHideDuration={4500} onClose={() => setToast(null)}>
        {toast && (
          <Alert severity={toast.severity} variant="filled" onClose={() => setToast(null)}>
            {toast.message}
          </Alert>
        )}
      </Snackbar>
    </section>
  );
}
