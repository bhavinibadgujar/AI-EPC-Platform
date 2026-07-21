import { FaCheckCircle, FaShip, FaStar, FaTruck, FaWarehouse } from "react-icons/fa";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import AIMetadata from "../components/AIMetadata";
import ActivityTimeline from "../components/ActivityTimeline";
import MetricCard from "../components/MetricCard";
import SeverityBadge from "../components/SeverityBadge";
import "../styles/supply.css";

const CHART_TOOLTIP = { background: "#08172a", border: "1px solid rgba(100,212,200,0.2)", borderRadius: 8, color: "#f0f7ff" };

export default function SupplyChain() {
  const deliveryTrend = [
    { week: "W1", planned: 12, actual: 10 },
    { week: "W2", planned: 18, actual: 16 },
    { week: "W3", planned: 21, actual: 18 },
    { week: "W4", planned: 25, actual: 22 }
  ];

  const vendors = [
    { name: "Schneider Electric", package: "Switchgear", status: "On Track",  performance: 94, delay: 0   },
    { name: "Vertiv",             package: "UPS Systems", status: "At Risk",  performance: 78, delay: 5   },
    { name: "Carrier",            package: "Chillers",    status: "Delayed",  performance: 62, delay: 12  },
    { name: "ABB",                package: "MCC Panels",  status: "On Track", performance: 91, delay: 0   },
    { name: "Siemens",            package: "BMS",         status: "At Risk",  performance: 81, delay: 3   }
  ];

  const statusToSeverity = (status) => {
    if (status === "Delayed")  return "Critical";
    if (status === "At Risk")  return "High";
    return "Low";
  };

  return (
    <section className="page-stack supply-page">
      {/* ── Header ───────────────────────────────────────────── */}
      <div className="page-heading">
        <div>
          <span className="section-label">Supply Chain</span>
          <h1>Logistics Control Tower</h1>
          <p>Monitor shipment health, vendor performance, delayed deliveries, and procurement confidence.</p>
        </div>
      </div>

      {/* ── KPIs ─────────────────────────────────────────────── */}
      <section className="cards">
        <MetricCard title="Active Shipments"   value="32"  change="+6 This Week"  description="Shipments in transit globally"        icon={<FaShip />}        tone="blue"   trend="up" />
        <MetricCard title="Warehouse Holds"    value="7"   change="-2 Released"   description="Items awaiting inspection clearance" icon={<FaWarehouse />}   tone="violet" trend="up" />
        <MetricCard title="On-time Delivery"   value="84%" change="↑ +4%"         description="Vendor delivery compliance rate"    icon={<FaCheckCircle />} tone="green"  trend="up" />
        <MetricCard title="Delayed Items"      value="11"  change="🔴 Critical"   description="Past committed delivery date"       icon={<FaTruck />}       tone="red"    trend="down" />
        <MetricCard title="Vendor Performance" value="91%" change="↑ +2%"         description="Weighted vendor scorecard average"  icon={<FaStar />}        tone="teal"   trend="up" />
      </section>

      {/* ── Charts + Tables ───────────────────────────────────── */}
      <section className="supply-grid">
        {/* Delivery Trend */}
        <article className="glass-panel chart-panel wide">
          <div className="panel-heading">
            <span className="section-label">Delivery Tracking</span>
            <h2>Planned vs Actual Deliveries</h2>
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={deliveryTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis dataKey="week" stroke="#647d91" tick={{ fontSize: 12 }} />
              <YAxis stroke="#647d91" tick={{ fontSize: 12 }} />
              <Tooltip contentStyle={CHART_TOOLTIP} />
              <Line type="monotone" dataKey="planned" stroke="#68a7ff" strokeWidth={2.5} name="Planned" dot={{ r: 4, fill: "#68a7ff" }} />
              <Line type="monotone" dataKey="actual"  stroke="#64d4c8" strokeWidth={2.5} name="Actual"  dot={{ r: 4, fill: "#64d4c8" }} />
            </LineChart>
          </ResponsiveContainer>
          <AIMetadata />
        </article>

        {/* Activity Timeline */}
        <article className="glass-panel">
          <div className="panel-heading">
            <span className="section-label">Logistics Timeline</span>
            <h2>Recent Delivery Events</h2>
          </div>
          <ActivityTimeline
            items={[
              { title: "UPS factory acceptance test passed", detail: "Witness report received and linked to PO.", time: "Today", type: "success" },
              { title: "Chiller shipment delayed — 12 days", detail: "Carrier vessel schedule slipped. Impact on commissioning.", time: "Today", type: "warning" },
              { title: "Switchgear cleared customs", detail: "Package released to inland logistics partner.", time: "Tue", type: "info" },
              { title: "MCC Panels dispatched — ABB", detail: "ETA 3 days to site. Inspection team notified.", time: "Mon", type: "info" }
            ]}
          />
        </article>

        {/* Vendor Status Table */}
        <article className="glass-panel table-panel wide">
          <div className="panel-heading">
            <span className="section-label">Vendor Intelligence</span>
            <h2>Vendor Performance Dashboard</h2>
          </div>
          <div className="responsive-table">
            <table>
              <thead>
                <tr>
                  <th>Vendor</th>
                  <th>Package</th>
                  <th>Delivery Status</th>
                  <th>Severity</th>
                  <th>Delay (Days)</th>
                  <th>Performance Score</th>
                </tr>
              </thead>
              <tbody>
                {vendors.map((vendor) => (
                  <tr key={vendor.name}>
                    <td><strong style={{ fontSize: 13 }}>{vendor.name}</strong></td>
                    <td style={{ color: "#a0b5c8" }}>{vendor.package}</td>
                    <td>
                      <span className={`status-pill ${vendor.status === "Delayed" ? "critical" : vendor.status === "At Risk" ? "high" : "low"}`}>
                        {vendor.status}
                      </span>
                    </td>
                    <td><SeverityBadge severity={statusToSeverity(vendor.status)} /></td>
                    <td style={{ color: vendor.delay > 0 ? "#f97316" : "#22c55e" }}>
                      {vendor.delay > 0 ? `+${vendor.delay} days` : "On time"}
                    </td>
                    <td>
                      <div className="perf-bar-row">
                        <span className="perf-bar-track">
                          <span
                            className="perf-bar-fill"
                            style={{
                              width: `${vendor.performance}%`,
                              background: vendor.performance >= 90 ? "#22c55e" : vendor.performance >= 75 ? "#f2b84b" : "#ef4444"
                            }}
                          />
                        </span>
                        <span className="perf-value">{vendor.performance}%</span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <AIMetadata />
        </article>
      </section>
    </section>
  );
}
