import { useEffect, useState } from "react";
import AnimatedBackground from "../components/AnimatedBackground";
import AIStatus from "../components/AIStatus";
import AIMetadata from "../components/AIMetadata";
import ActivityTimeline from "../components/ActivityTimeline";
import MetricCard from "../components/MetricCard";
import Navbar from "../components/Navbar";
import { getDashboard, getExecutiveBrief } from "../services/api";
import {
  FaCalendarAlt,
  FaChartLine,
  FaCheckCircle,
  FaExclamationTriangle,
  FaFileAlt,
  FaRobot,
  FaRupeeSign,
  FaShieldAlt,
  FaTruck
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

const CHART_TOOLTIP = { background: "#08172a", border: "1px solid rgba(100,212,200,0.2)", borderRadius: 8, color: "#f0f7ff" };

export default function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [brief, setBrief] = useState("Loading executive brief…");

  useEffect(() => {
    getDashboard().then(setDashboard).catch(() => setDashboard(null));
    getExecutiveBrief()
      .then((data) => setBrief(data.brief))
      .catch(() =>
        setBrief(
          "EPC Orbit is monitoring project compliance, procurement, risk and commissioning readiness. Start the backend to load live project intelligence."
        )
      );
  }, []);

  // ── Enterprise KPI definitions ──────────────────────────────────
  const kpis = [
    {
      title: "Project Health",
      value: "82%",
      change: "↑ +3%",
      description: "Overall project health index",
      icon: <FaShieldAlt />,
      tone: "teal",
      trend: "up"
    },
    {
      title: "Critical Risks",
      value: dashboard?.kpis?.compliance_deviations ?? "6",
      change: "↑ High",
      description: "Open high-severity risk items",
      icon: <FaExclamationTriangle />,
      tone: "red",
      trend: "down"
    },
    {
      title: "Compliance Issues",
      value: dashboard?.kpis?.compliance_deviations ?? "18",
      change: "3 Critical",
      description: "Specification deviations detected",
      icon: <FaFileAlt />,
      tone: "amber",
      trend: "neutral"
    },
    {
      title: "Schedule Delay",
      value: "12",
      change: "Delayed Tasks",
      description: "Delayed activities across workstreams",
      icon: <FaCalendarAlt />,
      tone: "amber",
      trend: "down"
    },
    {
      title: "Cost Exposure",
      value: "₹1.8 Cr",
      change: "↑ Risk",
      description: "Estimated cost impact of deviations",
      icon: <FaRupeeSign />,
      tone: "red",
      trend: "down"
    },
    {
      title: "Vendor Performance",
      value: "91%",
      change: "↑ +2%",
      description: "On-time delivery & compliance score",
      icon: <FaTruck />,
      tone: "green",
      trend: "up"
    },
    {
      title: "Open RFIs",
      value: "9",
      change: "3 Overdue",
      description: "Requests for information pending",
      icon: <FaChartLine />,
      tone: "blue",
      trend: "neutral"
    },
    {
  title: "Analysis Status",
  value: "Ready",
  change: "Live",
  description: "All AI services operational",
  icon: <FaRobot />,
  tone: "violet",
  trend: "up"
}
  ];

  // ── Chart data ──────────────────────────────────────────────────
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

  const activity = (dashboard?.activity || []).map((item, index) => ({
    ...item,
    time: index === 0 ? "Now" : "Today"
  }));

  return (
    <>
      <AnimatedBackground />
      <Navbar />

      {/* ── Hero ─────────────────────────────────────────────── */}
      <section className="page-hero">
        <div>
         <span className="section-label">Dashboard</span>
          <h1>EPC Orbit</h1>
          <p>
  AI-powered platform for monitoring project health, compliance,
  procurement, risk and commissioning across EPC projects.
</p>
        </div>
        <div className="hero-health">
  <strong>LIVE</strong>
  <span>AI Monitoring</span>
</div>
        
      </section>

      <AIStatus />

      {/* ── KPI Cards ────────────────────────────────────────── */}
      <section className="cards" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))" }}>
        {kpis.map((card) => (
          <MetricCard key={card.title} {...card} />
        ))}
      </section>

      {/* ── Dashboard Grid ───────────────────────────────────── */}
      <section className="dashboard-grid">

        {/* Executive Brief */}
        <article className="glass-panel wide">
          <div className="panel-heading">
            <span className="section-label">Executive Brief</span>
            <h2>Current Project Readout</h2>
          </div>
          <p className="executive-brief-text">{brief}</p>
          <AIMetadata source="Specification.pdf" page={18} />
          <div
  className="recommendation-panel"
  style={{
    marginTop: "20px",
    background: "rgba(100,212,200,0.05)"
  }}
>
  <div className="panel-heading">
    <span className="section-label">Recommended Actions</span>
    <h2>AI Recommendations</h2>
  </div>

  <ul
    style={{
      margin: 0,
      paddingLeft: "18px",
      lineHeight: "2"
    }}
  >
    <li>Review critical compliance deviations.</li>
    <li>Resolve delayed procurement packages.</li>
    <li>Prioritize vendor approvals.</li>
    <li>Generate executive summary before project review.</li>
  </ul>
</div>
        </article>

        {/* Workstream Progress */}
        <article className="glass-panel chart-panel">
          <div className="panel-heading">
            <span className="section-label">Execution</span>
            <h2>Workstream Progress</h2>
          </div>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={progressData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis dataKey="name" stroke="#647d91" tick={{ fontSize: 12 }} />
              <YAxis stroke="#647d91" tick={{ fontSize: 12 }} />
              <Tooltip contentStyle={CHART_TOOLTIP} />
              <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                {progressData.map((entry, index) => (
                  <Cell
                    key={index}
                    fill={entry.value >= 80 ? "#5ecc8a" : entry.value >= 60 ? "#64d4c8" : "#f2b84b"}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </article>

        {/* Health Mix Pie */}
        <article className="glass-panel chart-panel">
          <div className="panel-heading">
            <span className="section-label">Health</span>
            <h2>Project Health Mix</h2>
          </div>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie
                data={healthData}
                dataKey="value"
                innerRadius={64}
                outerRadius={94}
                paddingAngle={4}
                label={({ name, value }) => `${name}: ${value}%`}
              >
                {["#5ecc8a", "#f2b84b", "#ef4444"].map((color) => (
                  <Cell key={color} fill={color} />
                ))}
              </Pie>
              <Tooltip contentStyle={CHART_TOOLTIP} />
            </PieChart>
          </ResponsiveContainer>
        </article>

        {/* Compliance & Risk Trend */}
        <article className="glass-panel chart-panel wide">
          <div className="panel-heading">
            <span className="section-label">Trend</span>
            <h2>Compliance &amp; Risk Movement — 4 Weeks</h2>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis dataKey="week" stroke="#647d91" tick={{ fontSize: 12 }} />
              <YAxis stroke="#647d91" tick={{ fontSize: 12 }} />
              <Tooltip contentStyle={CHART_TOOLTIP} />
              <Line type="monotone" dataKey="compliance" stroke="#64d4c8" strokeWidth={2.5} dot={false} name="Compliance %" />
              <Line type="monotone" dataKey="risk" stroke="#ef4444" strokeWidth={2.5} dot={false} name="Open Risks" />
            </LineChart>
          </ResponsiveContainer>
        </article>

        {/* Activity Timeline */}
        <article className="glass-panel">
          <div className="panel-heading">
            <span className="section-label">Recent Activity</span>
            <h2>AI Activity Timeline</h2>
          </div>
          <ActivityTimeline
            items={
              activity.length
                ? activity
                : [
                    { title: "EPC Orbit monitoring active",detail: "Monitoring compliance, procurement, risk and commissioning activities in real time.",  time: "Now", type: "info" },
                    { title: "Backend pending", detail: "Start FastAPI to load live seeded activity.", time: "Now", type: "warning" }
                  ]
            }
          />
          <AIMetadata />
        </article>

      </section>
    </>
  );
}
