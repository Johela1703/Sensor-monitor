import React from "react";

export default function AlertList({ alerts }) {
  if (!alerts.length) {
    return <div className="empty">No alerts recorded yet.</div>;
  }

  return (
    <div className="alert-list">
      {alerts.map((alert) => (
        <div className="alert-card" key={alert.id}>
          <div>
            <h4>{alert.topic}</h4>
            <p>{new Date(alert.timestamp).toLocaleString()}</p>
          </div>
          <div className="alert-meta">
            <span className="badge">{alert.violated_keys}</span>
            <span className="muted">{alert.actual_values}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
