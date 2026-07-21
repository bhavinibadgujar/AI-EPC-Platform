import { LinearProgress } from "@mui/material";
import { FaCalendarCheck, FaClipboardList, FaHardHat, FaPercent, FaVial } from "react-icons/fa";
import AIMetadata from "../components/AIMetadata";
import ActivityTimeline from "../components/ActivityTimeline";
import MetricCard from "../components/MetricCard";
import "../styles/commissioning.css";

export default function Commissioning() {
  const checklist = [
    { item: "UPS Integrated Systems Test",        owner: "Cx Lead",    progress: 86, status: "In Progress" },
    { item: "Generator Black Start Sequence",      owner: "Electrical", progress: 72, status: "Ready"       },
    { item: "BMS Point-to-Point Validation",       owner: "Controls",   progress: 58, status: "Blocked"     },
    { item: "Chilled Water Balancing",             owner: "Mechanical", progress: 91, status: "Passed"      },
    { item: "Fireloop Circuit Verification",       owner: "Safety",     progress: 44, status: "In Progress" },
    { item: "Emergency Lighting Walk-through",     owner: "Electrical", progress: 100, status: "Passed"     }
  ];

  const statusSeverity = (status) => {
    if (status === "Blocked")     return "danger";
    if (status === "In Progress") return "warning";
    if (status === "Passed")      return "success";
    return "notice";
  };

  return (
    <section className="page-stack commissioning-page">
      {/* ── Header ───────────────────────────────────────────── */}
      <div className="page-heading">
        <div>
          <span className="section-label">Commissioning</span>
          <h1>Readiness Center</h1>
          <p>Coordinate test packs, inspection milestones, punch list progress, and system completion.</p>
        </div>
        <div className="cx-completion-badge">
          <strong>76%</strong>
          <span>Overall Completion</span>
        </div>
      </div>

      {/* ── KPIs ─────────────────────────────────────────────── */}
      <section className="cards">
        <MetricCard title="Completion"      value="76%"  change="↑ +9%"   description="L3 + L4 commissioning progress"       icon={<FaPercent />}      tone="green"  trend="up" />
        <MetricCard title="Test Packs"      value="128"  change="34 Open"  description="Total test packs issued"             icon={<FaVial />}         tone="blue"   trend="neutral" />
        <MetricCard title="Inspections Due" value="12"   change="⚠️ Urgent" description="Pending inspection confirmations"   icon={<FaClipboardList />} tone="amber" trend="down" />
        <MetricCard title="Systems Ready"   value="18"   change="+4 Today"  description="Accepted by witness team"           icon={<FaHardHat />}      tone="teal"   trend="up" />
        <MetricCard title="Punch Items"     value="41"   change="8 Critical" description="Outstanding punch list items"     icon={<FaCalendarCheck />} tone="violet" trend="neutral" />
      </section>

      {/* ── Grid ─────────────────────────────────────────────── */}
      <section className="commissioning-grid">
        {/* Checklist */}
        <article className="glass-panel checklist-panel wide">
          <div className="panel-heading">
            <span className="section-label">Equipment Checklist</span>
            <h2>System Commissioning Status</h2>
          </div>
          <div className="checklist">
            {checklist.map((row) => (
              <div className="checklist-row" key={row.item}>
                <div className="checklist-info">
                  <strong>{row.item}</strong>
                  <span>{row.owner}</span>
                </div>
                <div className="checklist-progress">
                  <LinearProgress
                    variant="determinate"
                    value={row.progress}
                    sx={{
                      height: 6,
                      borderRadius: 4,
                      backgroundColor: "rgba(255,255,255,0.08)",
                      "& .MuiLinearProgress-bar": {
                        background: row.status === "Passed" ? "#22c55e" : row.status === "Blocked" ? "#ef4444" : "#64d4c8"
                      }
                    }}
                  />
                  <span className="progress-pct">{row.progress}%</span>
                </div>
                <span className={`status-pill ${statusSeverity(row.status)}`}>
                  {row.status}
                </span>
              </div>
            ))}
          </div>
          <AIMetadata />
        </article>

        {/* Inspection Timeline */}
        <article className="glass-panel">
          <div className="panel-heading">
            <span className="section-label">Inspection Events</span>
            <h2>Inspection Timeline</h2>
          </div>
          <ActivityTimeline
            items={[
              { title: "Level 4 UPS IST Scheduled", detail: "Witness team assigned for Friday shift.", time: "Today", type: "info" },
              { title: "Generator Punch Item Closed", detail: "Fuel polishing loop evidence accepted.", time: "Yesterday", type: "success" },
              { title: "Controls Retest Required", detail: "Two BMS alarm mappings failed validation.", time: "Mon", type: "warning" },
              { title: "Chilled Water System Passed", detail: "Balancing certificates issued by QA lead.", time: "Last Fri", type: "success" }
            ]}
          />
        </article>

        {/* Completion card */}
        <article className="glass-panel cx-completion-card">
          <span className="section-label">Level Completion</span>
          <strong>76%</strong>
          <p>Level 3 and Level 4 commissioning completion based on accepted inspection evidence.</p>
          <LinearProgress
            variant="determinate"
            value={76}
            sx={{
              height: 8,
              borderRadius: 6,
              backgroundColor: "rgba(255,255,255,0.08)",
              "& .MuiLinearProgress-bar": { background: "linear-gradient(90deg, #64d4c8, #5ecc8a)" }
            }}
          />
          <AIMetadata />
        </article>
      </section>
    </section>
  );
}
