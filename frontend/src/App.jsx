import React from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Alerts from "./pages/Alerts";
import RawData from "./pages/RawData";

const navItems = [
  { to: "/", label: "Dashboard" },
  { to: "/alerts", label: "Alerts" },
  { to: "/raw-data", label: "Raw Data" }
];

export default function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="logo">
          <span className="logo-mark" />
          <div>
            <h1>Sensor Monitor</h1>
            <p>Live MQTT telemetry + alerting</p>
          </div>
        </div>
        <nav className="nav">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </header>

      <main className="app-main">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/alerts" element={<Alerts />} />
          <Route path="/raw-data" element={<RawData />} />
        </Routes>
      </main>
    </div>
  );
}
