import { LinearProgress } from "@mui/material";
import { FaClipboardList, FaHardHat, FaPercent, FaVial } from "react-icons/fa";
import ActivityTimeline from "../components/ActivityTimeline";
import DashboardCard from "../components/DashboardCard";
import "../styles/commissioning.css";

export default function Commissioning() {
  const checklist = [
    { item: "UPS integrated systems test", owner: "Cx Lead", progress: 86, status: "In Progress" },
    { item: "Generator black start sequence", owner: "Electrical", progress: 72, status: "Ready" },
    { item: "BMS point-to-point validation", owner: "Controls", progress: 58, status: "Blocked" },
    { item: "Chilled water balancing", owner: "Mechanical", progress: 91, status: "Passed" }
  ];

  return (
    <section className="page-stack commissioning-page">
      <div className="page-heading">
        <span className="section-label">Commissioning</span>
        <h1>Readiness Center</h1>
        <p>Coordinate test packs, inspection readiness, and completion progress across systems.</p>
      </div>

      <section className="cards">
        <DashboardCard title="Completion" value="76%" change="+9%" icon={<FaPercent />} tone="green" />
        <DashboardCard title="Test Packs" value="128" change="34 open" icon={<FaVial />} tone="blue" />
        <DashboardCard title="Inspections" value="41" change="12 due" icon={<FaClipboardList />} tone="amber" />
        <DashboardCard title="Systems Ready" value="18" change="+4" icon={<FaHardHat />} tone="violet" />
      </section>

      <section className="commissioning-grid">
        <article className="glass-panel checklist-panel">
          <div className="panel-heading">
            <span className="section-label">Checklist</span>
            <h2>Equipment Checklist</h2>
          </div>
          <div className="checklist">
            {checklist.map((row) => (
              <div className="checklist-row" key={row.item}>
                <div>
                  <strong>{row.item}</strong>
                  <span>{row.owner}</span>
                </div>
                <LinearProgress variant="determinate" value={row.progress} />
                <span className={`status-pill ${row.status === "Blocked" ? "danger" : row.status === "Passed" ? "success" : "warning"}`}>
                  {row.status}
                </span>
              </div>
            ))}
          </div>
        </article>

        <article className="glass-panel completion-card">
          <span className="section-label">Completion</span>
          <strong>76%</strong>
          <p>Level 3 and Level 4 commissioning completion based on accepted inspection evidence.</p>
          <LinearProgress variant="determinate" value={76} />
        </article>

        <article className="glass-panel">
          <div className="panel-heading">
            <span className="section-label">Inspection</span>
            <h2>Inspection Timeline</h2>
          </div>
          <ActivityTimeline
            items={[
              { title: "Level 4 UPS IST scheduled", detail: "Witness team assigned for Friday shift.", time: "Today", type: "info" },
              { title: "Generator punch item closed", detail: "Fuel polishing loop evidence accepted.", time: "Yesterday", type: "success" },
              { title: "Controls retest required", detail: "Two BMS alarm mappings failed validation.", time: "Mon", type: "warning" }
            ]}
          />
        </article>
      </section>
    </section>
  );
}
