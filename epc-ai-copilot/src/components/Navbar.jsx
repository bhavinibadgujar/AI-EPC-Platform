import { FaBell, FaCircle, FaSearch, FaUserCircle } from "react-icons/fa";
import "../styles/navbar.css";

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-title">
        <div className="navbar-brand-icon">EO</div>

        <div className="navbar-title-text">
          <span className="navbar-kicker">EPC Orbit</span>
          <span className="navbar-kicker-sub">
            AI Control Tower for EPC Projects
          </span>
        </div>
      </div>

      <div className="navbar-actions">
        <span className="live-badge">
          <FaCircle />
          Live Monitoring
        </span>

        <span className="last-updated">
          Updated 2 mins ago
        </span>

        <label
          className="navbar-search"
          title="Search coming in the next release"
        >
          <FaSearch />

          <input
            type="search"
            placeholder="Search (Coming Soon)"
            readOnly
          />
        </label>

        <button
          className="icon-button"
          type="button"
          title="Notifications"
        >
          <FaBell />
          <span className="badge">3</span>
        </button>

        <div className="profile">
          <FaUserCircle />
          <span>User</span>
        </div>
      </div>
    </header>
  );
}