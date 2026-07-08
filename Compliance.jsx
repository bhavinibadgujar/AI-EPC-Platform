import { Button, LinearProgress } from "@mui/material";
import { useState } from "react";
import { FaDownload, FaFilePdf, FaSearch } from "react-icons/fa";
import Loader from "../components/Loader";
import { uploadCompliance } from "../services/api";
import "../styles/compliance.css";

export default function Compliance() {
  const [specificationFile, setSpecificationFile] = useState(null);
  const [vendorFile, setVendorFile] = useState(null);
  const [isComparing, setIsComparing] = useState(false);

  const missingClauses = [
    { clause: "23 05 93", requirement: "TAB report format", status: "Missing vendor evidence" },
    { clause: "26 32 13", requirement: "Generator load bank test", status: "Partial compliance" },
    { clause: "27 05 26", requirement: "Grounding continuity", status: "Action required" }
  ];

  const handleCompare = async () => {
    if (!specificationFile || !vendorFile) return;
    setIsComparing(true);
    try {
      await uploadCompliance({ specificationFile, vendorFile });
    } finally {
      setIsComparing(false);
    }
  };

  return (
    <section className="page-stack compliance-page">
      <div className="page-heading">
        <span className="section-label">Compliance</span>
        <h1>Specification Comparison</h1>
        <p>Upload EPC specifications and vendor documents to identify gaps before procurement release.</p>
      </div>

      <div className="compliance-layout">
        <article className="glass-panel upload-panel">
          <div className="upload-grid">
            <label className="upload-dropzone">
              <FaFilePdf />
              <strong>EPC Specification PDF</strong>
              <span>{specificationFile ? specificationFile.name : "Choose project specification"}</span>
              <input type="file" accept="application/pdf" onChange={(event) => setSpecificationFile(event.target.files[0])} />
            </label>

            <label className="upload-dropzone">
              <FaFilePdf />
              <strong>Vendor PDF</strong>
              <span>{vendorFile ? vendorFile.name : "Choose vendor submittal"}</span>
              <input type="file" accept="application/pdf" onChange={(event) => setVendorFile(event.target.files[0])} />
            </label>
          </div>

          <Button
            variant="contained"
            startIcon={<FaSearch />}
            disabled={!specificationFile || !vendorFile || isComparing}
            onClick={handleCompare}
          >
            {isComparing ? "Comparing" : "Compare Documents"}
          </Button>

          {isComparing && <Loader label="AI is comparing uploaded PDFs" />}
        </article>

        <article className="glass-panel summary-card">
          <span className="section-label">Summary</span>
          <strong>92%</strong>
          <p>Compliance match across technical, commercial, and closeout requirements.</p>
          <LinearProgress variant="determinate" value={92} />
          <Button variant="outlined" startIcon={<FaDownload />}>Download Report</Button>
        </article>
      </div>

      <article className="glass-panel table-panel">
        <div className="panel-heading">
          <span className="section-label">Exceptions</span>
          <h2>Missing Clauses</h2>
        </div>
        <div className="responsive-table">
          <table>
            <thead>
              <tr>
                <th>Clause</th>
                <th>Requirement</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {missingClauses.map((item) => (
                <tr key={item.clause}>
                  <td>{item.clause}</td>
                  <td>{item.requirement}</td>
                  <td><span className="status-pill warning">{item.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </article>
    </section>
  );
}
