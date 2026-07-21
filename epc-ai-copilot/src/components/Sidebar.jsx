import { NavLink } from "react-router-dom";
import {
  FaClipboardCheck,
  FaExclamationTriangle,
  FaRobot,
  FaTools,
  FaTruck
} from "react-icons/fa";
import { MdDashboard } from "react-icons/md";
import "../styles/sidebar.css";

export default function Sidebar() {
  const menu = [
    { name: "Dashboard", path: "/", icon: <MdDashboard /> },
    { name: "Compliance", path: "/compliance", icon: <FaClipboardCheck /> },
    { name: "Risk Register", path: "/risk", icon: <FaExclamationTriangle /> },
    { name: "Supply Chain", path: "/supplychain", icon: <FaTruck /> },
    { name: "Commissioning", path: "/commissioning", icon: <FaTools /> },
    { name: "AI Assistant", path: "/chat", icon: <FaRobot /> }
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">EO</div>

        <div className="sidebar-logo-text">
          <span className="sidebar-logo-name">EPC Orbit</span>
          <span className="sidebar-logo-sub">
            AI Control Tower
          </span>
        </div>
      </div>

      <nav
        className="sidebar-nav"
        aria-label="Primary navigation"
      >
        {menu.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === "/"}
            className={({ isActive }) =>
              isActive ? "active" : undefined
            }
          >
            {item.icon}
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-footer-project">
          <span className="sidebar-footer-dot" />
          <strong>System Online</strong>
        </div>

        <span>
          AI Control Tower for EPC Projects
        </span>
      </div>
    </aside>
);
}