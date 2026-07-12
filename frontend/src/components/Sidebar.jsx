import { NavLink } from "react-router-dom";
import {
  FaClipboardCheck,
  FaExclamationTriangle,
  FaHome,
  FaRobot,
  FaTools,
  FaTruck
} from "react-icons/fa";

import "../styles/sidebar.css";

export default function Sidebar() {
  const menu = [
    { name: "Dashboard", path: "/", icon: <FaHome /> },
    { name: "Compliance", path: "/compliance", icon: <FaClipboardCheck /> },
    { name: "Risk Dashboard", path: "/risk", icon: <FaExclamationTriangle /> },
    { name: "Supply Chain", path: "/supplychain", icon: <FaTruck /> },
    { name: "Commissioning", path: "/commissioning", icon: <FaTools /> },
    { name: "AI Chat", path: "/chat", icon: <FaRobot /> }
  ];

  return (
    <aside className="sidebar">
      <h2 className="logo">
        <span className="logo-mark">EPC</span>
        <span>AI Copilot</span>
      </h2>

      <nav className="sidebar-nav" aria-label="Primary navigation">
        {menu.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => (isActive ? "active" : undefined)}
            end={item.path === "/"}
          >
            {item.icon}
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <strong>Project Synapse</strong>
        <span>Live FastAPI-ready frontend for enterprise EPC workflows.</span>
      </div>
    </aside>
  );
}
