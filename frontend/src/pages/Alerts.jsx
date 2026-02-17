import React, { useEffect, useState } from "react";
import { api } from "../api/client";
import AlertList from "../components/AlertList";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    api
      .get("/alerts", { params: { limit: 100, offset: 0 } })
      .then((res) => {
        if (mounted) setAlerts(res.data);
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, []);

  return (
    <section className="page">
      <div className="page-header">
        <div>
          <h2>Alerts</h2>
          <p>All threshold breaches across monitored topics.</p>
        </div>
        <div className="pill alert">{alerts.length} total</div>
      </div>

      <div className="panel">
        <div className="panel-header">
          <h3>Triggered Alerts</h3>
          <span className="hint">Latest first</span>
        </div>
        {loading ? <div className="skeleton">Loading alerts...</div> : <AlertList alerts={alerts} />}
      </div>
    </section>
  );
}
