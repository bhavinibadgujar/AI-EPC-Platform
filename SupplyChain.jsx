import { FaCheckCircle, FaShip, FaTruck, FaWarehouse } from "react-icons/fa";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import ActivityTimeline from "../components/ActivityTimeline";
import DashboardCard from "../components/DashboardCard";
import "../styles/supply.css";

export default function SupplyChain() {
  const deliveryTrend = [
    { week: "W1", planned: 12, actual: 10 },
    { week: "W2", planned: 18, actual: 16 },
    { week: "W3", planned: 21, actual: 18 },
    { week: "W4", planned: 25, actual: 22 }
  ];

  const vendors = [
    { name: "Schneider Electric", package: "Switchgear", status: "On Track" },
    { name: "Vertiv", package: "UPS Systems", status: "At Risk" },
    { name: "Carrier", package: "Chillers", status: "Delayed" }
  ];

  return (
    <section className="page-stack supply-page">
      <div className="page-heading">
        <span className="section-label">Supply Chain</span>
        <h1>Logistics Control Tower</h1>
        <p>Monitor shipment health, vendor commitments, delayed items, and delivery confidence.</p>
      </div>

      <section className="cards">
        <DashboardCard title="Active Shipments" value="32" change="+6" icon={<FaShip />} tone="blue" />
        <DashboardCard title="Warehouse Holds" value="7" change="-2" icon={<FaWarehouse />} tone="violet" />
        <DashboardCard title="On-time Delivery" value="84%" change="+4%" icon={<FaCheckCircle />} tone="green" />
        <DashboardCard title="Delayed Items" value="11" change="High" icon={<FaTruck />} tone="amber" />
      </section>

      <section className="supply-grid">
        <article className="glass-panel chart-panel wide">
          <div className="panel-heading">
            <span className="section-label">Delivery</span>
            <h2>Planned vs Actual Deliveries</h2>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={deliveryTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
              <XAxis dataKey="week" stroke="#9fb1c3" />
              <YAxis stroke="#9fb1c3" />
              <Tooltip contentStyle={{ background: "#0c1724", border: "1px solid #24465d" }} />
              <Line type="monotone" dataKey="planned" stroke="#68a7ff" strokeWidth={3} />
              <Line type="monotone" dataKey="actual" stroke="#64d4c8" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </article>

        <article className="glass-panel">
          <div className="panel-heading">
            <span className="section-label">Timeline</span>
            <h2>Delivery Timeline</h2>
          </div>
          <ActivityTimeline
            items={[
              { title: "UPS factory acceptance test passed", detail: "Witness report received and linked to PO.", time: "Today", type: "success" },
              { title: "Chiller shipment delayed", detail: "Carrier vessel schedule slipped by 5 days.", time: "Today", type: "warning" },
              { title: "Switchgear cleared customs", detail: "Package released to inland logistics partner.", time: "Tue", type: "info" }
            ]}
          />
        </article>

        <article className="glass-panel table-panel">
          <div className="panel-heading">
            <span className="section-label">Vendors</span>
            <h2>Vendor Status</h2>
          </div>
          <div className="responsive-table">
            <table>
              <thead>
                <tr><th>Vendor</th><th>Package</th><th>Status</th></tr>
              </thead>
              <tbody>
                {vendors.map((vendor) => (
                  <tr key={vendor.name}>
                    <td>{vendor.name}</td>
                    <td>{vendor.package}</td>
                    <td><span className={`status-pill ${vendor.status === "Delayed" ? "danger" : vendor.status === "At Risk" ? "warning" : "success"}`}>{vendor.status}</span></td>
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
