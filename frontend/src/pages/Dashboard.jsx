import AnimatedBackground from "../components/AnimatedBackground";
import AIStatus from "../components/AIStatus";
import ActivityTimeline from "../components/ActivityTimeline";
import DashboardCard from "../components/DashboardCard";
import Navbar from "../components/Navbar";
import {
  FaClipboardCheck,
  FaExclamationTriangle,
  FaFileAlt,
  FaProjectDiagram
} from "react-icons/fa";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import "../styles/dashboard.css";

export default function Dashboard() {
  const kpis = [
    { title: "Documents", value: "1,248", change: "+12%", icon: <FaFileAlt />, tone: "blue" },
    { title: "Compliance", value: "92%", change: "+5%", icon: <FaClipboardCheck />, tone: "green" },
    { title: "Open Risks", value: "18", change: "-3", icon: <FaExclamationTriangle />, tone: "amber" },
    { title: "Active Packages", value: "47", change: "+8", icon: <FaProjectDiagram />, tone: "violet" }
  ];

  const progressData = [
    { name: "Design", value: 88 },
    { name: "Procure", value: 71 },
    { name: "Build", value: 63 },
    { name: "Test", value: 42 }
  ];

  const healthData = [
    { name: "Healthy", value: 64 },
    { name: "Watch", value: 24 },
    { name: "Critical", value: 12 }
  ];

  const trendData = [
    { week: "W1", compliance: 76, risk: 31 },
    { week: "W2", compliance: 80, risk: 28 },
    { week: "W3", compliance: 86, risk: 22 },
    { week: "W4", compliance: 92, risk: 18 }
  ];

  const activity = [
    {
      title: "Vendor HVAC package reviewed",
      detail: "AI found 3 deviations against project specification section 23.",
      time: "8 min",
      type: "success"
    },
    {
      title: "Transformer delivery risk updated",
      detail: "Port congestion changed schedule confidence from medium to high risk.",
      time: "24 min",
      type: "warning"
    },
    {
      title: "Commissioning checklist synced",
      detail: "Level 3 test packs were reconciled with inspection records.",
      time: "1 hr",
      type: "info"
    }
  ];

  return (
    <>
      <AnimatedBackground />
      <Navbar />

      <section className="page-hero">
        <div>
          <span className="section-label">Command Center</span>
          <h1>EPC AI Copilot</h1>
          <p>
            A live intelligence layer for engineering, procurement, construction, and
            commissioning teams.
          </p>
        </div>
        <div className="hero-health">
          <strong>87%</strong>
          <span>Project health</span>
        </div>
      </section>

      <AIStatus />

      <section className="cards">
        {kpis.map((card) => (
          <DashboardCard key={card.title} {...card} />
        ))}
      </section>

      <section className="dashboard-grid">
        <article className="glass-panel chart-panel">
          <div className="panel-heading">
            <span className="section-label">Execution</span>
            <h2>Workstream Progress</h2>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={progressData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
              <XAxis dataKey="name" stroke="#9fb1c3" />
              <YAxis stroke="#9fb1c3" />
              <Tooltip contentStyle={{ background: "#0c1724", border: "1px solid #24465d" }} />
              <Bar dataKey="value" radius={[8, 8, 0, 0]} fill="#64d4c8" />
            </BarChart>
          </ResponsiveContainer>
        </article>

        <article className="glass-panel chart-panel">
          <div className="panel-heading">
            <span className="section-label">Health</span>
            <h2>Project Health Mix</h2>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={healthData} dataKey="value" innerRadius={64} outerRadius={94} paddingAngle={4}>
                {["#64d4c8", "#68a7ff", "#ef6f5a"].map((color) => (
                  <Cell key={color} fill={color} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: "#0c1724", border: "1px solid #24465d" }} />
            </PieChart>
          </ResponsiveContainer>
        </article>

        <article className="glass-panel chart-panel wide">
          <div className="panel-heading">
            <span className="section-label">Trend</span>
            <h2>Compliance and Risk Movement</h2>
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
              <XAxis dataKey="week" stroke="#9fb1c3" />
              <YAxis stroke="#9fb1c3" />
              <Tooltip contentStyle={{ background: "#0c1724", border: "1px solid #24465d" }} />
              <Line type="monotone" dataKey="compliance" stroke="#64d4c8" strokeWidth={3} dot={false} />
              <Line type="monotone" dataKey="risk" stroke="#ef6f5a" strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </article>

        <article className="glass-panel">
          <div className="panel-heading">
            <span className="section-label">Recent Activity</span>
            <h2>AI Activity Timeline</h2>
          </div>
          <ActivityTimeline items={activity} />
        </article>
      </section>
    </>
  );
}
