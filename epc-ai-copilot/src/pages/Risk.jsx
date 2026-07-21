import { Alert, Button, Snackbar } from "@mui/material";
import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { FaBolt, FaCalendarAlt, FaExclamationTriangle, FaRupeeSign, FaShieldAlt } from "react-icons/fa";
import AIMetadata from "../components/AIMetadata";
import ActivityTimeline from "../components/ActivityTimeline";
import MetricCard from "../components/MetricCard";
import SeverityBadge from "../components/SeverityBadge";
import { getRisks, uploadScheduleRisk } from "../services/api";
import "../styles/risk.css";

const CHART_TOOLTIP = { background: "#08172a", border: "1px solid rgba(100,212,200,0.2)", borderRadius: 8, color: "#f0f7ff" };

const SEVERITY_COLOR = {
  Critical: "#ef4444",
  Major: "#f97316",
  High: "#f97316",
  Medium: "#eab308",
  Low: "#22c55e"
};

export default function Risk() {
  const [risks, setRisks] = useState([]);
  const [scheduleFile, setScheduleFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    getRisks()
      .then((data) => setRisks(data.risks || []))
      .catch(() => setRisks([]));
  }, []);

  const handleUpload = async () => {
    if (!scheduleFile) return;
    setIsUploading(true);
    try {
      const response = await uploadScheduleRisk(scheduleFile);
      setRisks(response.risks || []);
      setToast({
        severity: "success",
        message: `Schedule risk check complete: ${response.summary?.open_risks || 0} risks found.`
      });
    } catch (error) {
      setToast({
        severity: "error",
        message: error.response?.data?.detail || "Schedule upload failed."
      });
    } finally {
      setIsUploading(false);
    }
  };

  const criticalCount = risks.filter((r) => r.severity === "Critical").length;
  const highCount     = risks.filter((r) => ["High", "Major"].includes(r.severity)).length;
  const delayedCount  = 12;

  const severity = [
    { name: "Critical", value: criticalCount || 2 },
    { name: "High",     value: highCount     || 4 },
    { name: "Medium",   value: risks.filter((r) => r.severity === "Medium").length || 6 },
    { name: "Low",      value: risks.filter((r) => r.severity === "Low").length    || 3 }
  ];

  const heatmap = [
    { area: "MEP",      score: 86 },
    { area: "Civil",    score: 42 },
    { area: "Power",    score: 74 },
    { area: "Controls", score: 58 },
    { area: "Logistics",score: 91 }
  ];

  return (
    <section className="page-stack risk-page">
      {/* ── Header ───────────────────────────────────────────── */}
      <div className="page-heading">
        <div>
          <span className="section-label">Risk Register</span>
          <h1>Project Risk Intelligence</h1>
          <p>Track risk severity, ownership, mitigation urgency, and cost exposure across all workstreams.</p>
        </div>
      </div>

      {/* ── KPI Row ──────────────────────────────────────────── */}
      <section className="cards">
        <MetricCard title="Critical Risks"    value={criticalCount || "6"} change="🔴 Urgent"       description="Require immediate action"          icon={<FaExclamationTriangle />} tone="red"    trend="down" />
        <MetricCard title="High Risks"        value={highCount     || "4"} change="🟠 Review"       description="Elevated severity, owner assigned"  icon={<FaShieldAlt />}           tone="amber"  trend="neutral" />
        <MetricCard title="Delayed Activities"value={delayedCount}         change="↑ 3 Added"       description="Behind schedule across workstreams"  icon={<FaCalendarAlt />}         tone="amber"  trend="down" />
        <MetricCard title="Cost Exposure"     value="₹1.8 Cr"             change="↑ High"           description="Estimated financial risk impact"     icon={<FaRupeeSign />}           tone="red"    trend="down" />
        <MetricCard title="AI Risk Score"     value={risks.length > 1 ? "78" : "42"} change={risks.length > 1 ? "High" : "Watch"} description="Composite AI-calculated risk index" icon={<FaBolt />} tone="violet" trend="neutral" />
      </section>

      {/* ── Schedule Upload ───────────────────────────────────── */}
      <article className="glass-panel upload-panel">
        <div className="panel-heading">
          <span className="section-label">Schedule Analysis</span>
          <h2>Upload Schedule for Risk Assessment</h2>
        </div>
        <div className="schedule-upload-row">
          <input
            type="file"
            accept=".csv,.xlsx,.xls,.xml"
            onChange={(event) => setScheduleFile(event.target.files[0])}
            style={{ color: "#a0b5c8" }}
          />
          <Button
            variant="contained"
            disabled={!scheduleFile || isUploading}
            onClick={handleUpload}
          >
            {isUploading ? "Analyzing Schedule…" : "Analyze Schedule Risk"}
          </Button>
        </div>
      </article>

      {/* ── Charts + Table ────────────────────────────────────── */}
      <section className="risk-grid">
        {/* Severity Distribution */}
        <article className="glass-panel chart-panel">
          <div className="panel-heading">
            <span className="section-label">Distribution</span>
            <h2>Risk Severity Breakdown</h2>
          </div>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={severity} dataKey="value" outerRadius={90} label={({ name, value }) => `${name}: ${value}`}>
                {["#ef4444", "#f97316", "#eab308", "#22c55e"].map((color) => (
                  <Cell key={color} fill={color} />
                ))}
              </Pie>
              <Tooltip contentStyle={CHART_TOOLTIP} />
            </PieChart>
          </ResponsiveContainer>
          <AIMetadata />
        </article>

        {/* Risk Heatmap */}
        <article className="glass-panel chart-panel">
          <div className="panel-heading">
            <span className="section-label">Heatmap</span>
            <h2>Risk Score by Discipline</h2>
          </div>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={heatmap}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis dataKey="area" stroke="#647d91" tick={{ fontSize: 12 }} />
              <YAxis stroke="#647d91" tick={{ fontSize: 12 }} />
              <Tooltip contentStyle={CHART_TOOLTIP} />
              <Bar dataKey="score" radius={[6, 6, 0, 0]}>
                {heatmap.map((entry) => (
                  <Cell
                    key={entry.area}
                    fill={entry.score >= 80 ? "#ef4444" : entry.score >= 60 ? "#f97316" : "#22c55e"}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </article>

        {/* Risk Timeline */}
        <article className="glass-panel">
          <div className="panel-heading">
            <span className="section-label">Timeline</span>
            <h2>Recent Risk Events</h2>
          </div>
          <ActivityTimeline
            items={
              risks.slice(0, 3).map((risk) => ({
                title: risk.activity,
                detail: risk.reason,
                time: risk.eta,
                type: risk.severity === "Critical" ? "warning" : "info"
              }))
            }
          />
          {!risks.length && (
            <ActivityTimeline
              items={[
                { title: "MEP schedule delay flagged", detail: "3 critical path activities behind by 8 days.", time: "Today", type: "warning" },
                { title: "Power supply risk elevated", detail: "Transformer delivery delayed — impact on commissioning.", time: "Today", type: "warning" },
                { title: "Logistics re-routed", detail: "Chiller shipment re-routed through alternate port.", time: "Yesterday", type: "info" }
              ]}
            />
          )}
        </article>

        {/* Risk Register Table */}
        <article className="glass-panel table-panel">
          <div className="panel-heading">
            <span className="section-label">Risk Register</span>
            <h2>Open Project Risks</h2>
          </div>
          <div className="responsive-table">
            <table>
              <thead>
                <tr>
                  <th>Risk ID</th>
                  <th>Activity / Risk</th>
                  <th>Owner</th>
                  <th>Severity</th>
                  <th>Cost Impact</th>
                  <th>ETA / Deadline</th>
                </tr>
              </thead>
              <tbody>
                {risks.map((risk) => (
                  <tr key={risk.id}>
                    <td><span className="clause-tag">{risk.id}</span></td>
                    <td>
                      <strong style={{ fontSize: 13 }}>{risk.activity}</strong>
                      {risk.reason && <span className="table-note">{risk.reason}</span>}
                    </td>
                    <td>{risk.owner}</td>
                    <td><SeverityBadge severity={risk.severity} /></td>
                    <td style={{ color: "#f97316" }}>{risk.cost_impact ?? "—"}</td>
                    <td style={{ color: "#a0b5c8", whiteSpace: "nowrap" }}>{risk.eta}</td>
                  </tr>
                ))}
                {!risks.length && (
                  <tr>
                    <td colSpan="6" style={{ textAlign: "center", padding: "36px", color: "#647d91" }}>
                      No risks loaded. Upload a schedule or start FastAPI to load live data.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          <AIMetadata />
        </article>
      </section>

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
