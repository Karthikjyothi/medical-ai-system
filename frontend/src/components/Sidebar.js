import { Link } from "react-router-dom";
import {
  LayoutDashboard,
  Stethoscope,
  History,
  BrainCircuit,
  GitCompare,
  BarChart3,
  LogOut
} from "lucide-react";

function Sidebar() {
  const user = JSON.parse(localStorage.getItem("user"));

  const handleLogout = () => {
    localStorage.clear();
    window.location.href = "/";
  };

  return (
    <div style={sidebarStyle}>
      <div>
        <div style={logoBox}>
          <BrainCircuit size={28} />
        </div>

        <h2 style={{ marginTop: "15px", marginBottom: "5px" }}>MedIntel AI</h2>
        <p style={{ color: "#94a3b8", fontSize: "13px" }}>
          Universal Medical Intelligence
        </p>

        <div style={{ marginTop: "40px", display: "flex", flexDirection: "column", gap: "14px" }}>
          <Link to="/dashboard" style={linkStyle}>
            <LayoutDashboard size={18} /> Dashboard
          </Link>

          <Link to="/diagnose" style={linkStyle}>
            <Stethoscope size={18} /> Diagnose
          </Link>

          <Link to="/medical-assistant" style={linkStyle}>
            <BrainCircuit size={18} /> Medical GPT
          </Link>

          <Link to="/history" style={linkStyle}>
            <History size={18} /> History
          </Link>

          <Link to="/compare-history" style={linkStyle}>
            <GitCompare size={18} /> Compare Reports
          </Link>

          <Link to="/admin-train" style={linkStyle}>
            <BrainCircuit size={18} /> Admin Train
          </Link>

          <Link to="/dataset-analytics" style={linkStyle}>
            <BarChart3 size={18} /> Dataset Analytics
          </Link>
        </div>
      </div>

      <div style={{ marginTop: "auto" }}>
        <div style={userBox}>
          Logged in as
          <br />
          <strong>{user?.full_name}</strong>
        </div>

        <button onClick={handleLogout} style={logoutBtn}>
          <LogOut size={16} /> Logout
        </button>
      </div>
    </div>
  );
}

const sidebarStyle = {
  width: "240px",
  height: "100vh",
  background: "#0f172a",
  color: "white",
  padding: "22px",
  position: "fixed",
  left: 0,
  top: 0,
  display: "flex",
  flexDirection: "column",
  boxShadow: "4px 0 18px rgba(0,0,0,0.15)"
};

const logoBox = {
  width: "55px",
  height: "55px",
  borderRadius: "14px",
  background: "linear-gradient(135deg, #1d4ed8, #2563eb)",
  display: "flex",
  alignItems: "center",
  justifyContent: "center"
};

const linkStyle = {
  color: "white",
  textDecoration: "none",
  background: "rgba(255,255,255,0.05)",
  padding: "12px 14px",
  borderRadius: "10px",
  display: "flex",
  alignItems: "center",
  gap: "10px",
  fontSize: "14px"
};

const userBox = {
  background: "rgba(255,255,255,0.05)",
  padding: "12px",
  borderRadius: "10px",
  fontSize: "13px",
  color: "#cbd5e1"
};

const logoutBtn = {
  marginTop: "12px",
  width: "100%",
  padding: "11px",
  border: "none",
  borderRadius: "10px",
  background: "#dc2626",
  color: "white",
  cursor: "pointer",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  gap: "8px"
};

export default Sidebar;