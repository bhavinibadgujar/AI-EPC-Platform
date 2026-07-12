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
import { FaBolt, FaClock, FaExclamationTriangle } from "react-icons/fa";
import ActivityTimeline from "../components/ActivityTimeline";
import DashboardCard from "../components/DashboardCard";
import "../styles/risk.css";

export default function Risk() {
  const severity = [
    { name: "Critical", value: 6 },
    { name: "High", value: 12 },
    { name: "Medium", value: 24 },
    { name: "Low", value: 18 }
  ];

  const heatmap = [
    { area: "MEP", score: 86 },
    { area: "Civil", score: 42 },
    { area: "Power", score: 74 },
    { area: "Controls", score: 58 },
    { area: "Logistics", score: 91 }
  ];

  const risks = [
    { id: "R-104", owner: "Procurement", impact: "Transformer delay", severity: "Critical", eta: "9 days" },
    { id: "R-118", owner: "Engineering", impact: "BMS interface gap", severity: "High", eta: "4 days" },
    { id: "R-127", owner: "Construction", impact: "Cable tray access", severity: "Medium", eta: "12 days" }
  ];

  return (
    <section className="page-stack risk-page">
      <div className="page-heading">
        <span className="section-label">Risk</span>
        <h1>Risk Dashboard</h1>
        <p>Track project risk severity, ownership, trends, and mitigation urgency.</p>
      </div>

      <section className="cards">
        <DashboardCard title="Critical Risks" value="6" change="+2" icon={<FaExclamationTriangle />} tone="amber" />
        <DashboardCard title="Mitigations Due" value="14" change="48h" icon={<FaClock />} tone="blue" />
        <DashboardCard title="AI Risk Score" value="78" change="High" icon={<FaBolt />} tone="violet" />
      </section>

      <section className="risk-grid">
        <article className="glass-panel chart-panel">
          <div className="panel-heading">
            <span className="section-label">Severity</span>
            <h2>Distribution</h2>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={severity} dataKey="value" outerRadius={94} label>
                {["#ef6f5a", "#f2b84b", "#68a7ff", "#64d4c8"].map((color) => (
                  <Cell key={color} fill={color} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: "#0c1724", border: "1px solid #24465d" }} />
            </PieChart>
          </ResponsiveContainer>
        </article>

        <article className="glass-panel chart-panel">
          <div className="panel-heading">
            <span className="section-label">Heatmap</span>
            <h2>Risk by Discipline</h2>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={heatmap}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
              <XAxis dataKey="area" stroke="#9fb1c3" />
              <YAxis stroke="#9fb1c3" />
              <Tooltip contentStyle={{ background: "#0c1724", border: "1px solid #24465d" }} />
              <Bar dataKey="score" fill="#ef6f5a" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </article>

        <article className="glass-panel">
          <div className="panel-heading">
            <span className="section-label">Timeline</span>
            <h2>Risk Movement</h2>
          </div>
          <ActivityTimeline
            items={[
              { title: "Critical supplier flagged", detail: "Cooling tower motor delivery moved to risk register.", time: "Today", type: "warning" },
              { title: "Mitigation accepted", detail: "Temporary power sequence approved by commissioning lead.", time: "Yesterday", type: "success" },
              { title: "New interface issue", detail: "Controls integration dependency added to open actions.", time: "Mon", type: "info" }
            ]}
          />
        </article>

        <article className="glass-panel table-panel">
          <div className="panel-heading">
            <span className="section-label">Register</span>
            <h2>Project Risks</h2>
          </div>
          <div className="responsive-table">
            <table>
              <thead>
                <tr><th>ID</th><th>Owner</th><th>Impact</th><th>Severity</th><th>ETA</th></tr>
              </thead>
              <tbody>
                {risks.map((risk) => (
                  <tr key={risk.id}>
                    <td>{risk.id}</td>
                    <td>{risk.owner}</td>
                    <td>{risk.impact}</td>
                    <td><span className="status-pill danger">{risk.severity}</span></td>
                    <td>{risk.eta}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </article>
      </section>
    </section>
  );
}
