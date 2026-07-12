import { FaBell, FaSearch, FaUserCircle } from "react-icons/fa";
import "../styles/navbar.css";

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-title">
        <span className="navbar-kicker">EPC AI Copilot</span>
        <h2>AI Command Center</h2>
        <p>Data center EPC intelligence for compliance, risk, logistics, and commissioning.</p>
      </div>

      <div className="navbar-actions">
        <label className="navbar-search" aria-label="Search project intelligence">
          <FaSearch />
          <input type="search" placeholder="Search documents, RFIs, risks" />
        </label>

        <button className="icon-button" type="button" aria-label="Notifications">
          <FaBell />
          <span className="badge">3</span>
        </button>

        <div className="profile" aria-label="Signed in user">
          <FaUserCircle />
          <span>Mahek</span>
        </div>
      </div>
    </header>
  );
}
