import React, { useEffect, useState } from "react";
import { api } from "../api/client";
import StatCard from "../components/StatCard";
import AlertList from "../components/AlertList";

export default function Dashboard() {
  const [metrics, setMetrics] = useState({ total_messages: 0, recent_alerts: 0 });
  const [latest, setLatest] = useState([]);
  const [recentAlerts, setRecentAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    Promise.all([
      api.get("/metrics"),
      api.get("/sensors/latest"),
      api.get("/alerts", { params: { limit: 5, offset: 0 } })
    ])
      .then(([metricsRes, latestRes, alertsRes]) => {
        if (!mounted) return;
        setMetrics(metricsRes.data);
        setLatest(latestRes.data);
        setRecentAlerts(alertsRes.data);
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
          <h2>Dashboard</h2>
          <p>Overview of latest sensor activity.</p>
        </div>
        <div className="pill">Live</div>
      </div>

      <div className="grid cards">
        <StatCard title="Total Messages" value={metrics.total_messages} />
        <StatCard title="Recent Alerts" value={metrics.recent_alerts} />
        <StatCard title="Active Topics" value={latest.length} />
      </div>

      <div className="grid split">
        <div className="panel">
          <div className="panel-header">
            <h3>Latest Readings</h3>
            <span className="hint">Per topic snapshot</span>
          </div>
          {loading ? (
            <div className="skeleton">Loading latest readings...</div>
          ) : (
            <div className="reading-list">
              {latest.map((item) => (
                <div className="reading-card" key={item.id}>
                  <div>
                    <h4>{item.topic}</h4>
                    <p>{new Date(item.timestamp).toLocaleString()}</p>
                  </div>
                  <div className="reading-values">
                    <span>T: {item.temperature ?? "-"}</span>
                    <span>H: {item.humidity ?? "-"}</span>
                    <span>V: {item.voltage ?? "-"}</span>
                    <span>I: {item.current ?? "-"}</span>
                    <span>P: {item.pressure ?? "-"}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="panel">
          <div className="panel-header">
            <h3>Recent Alerts</h3>
            <span className="hint">Last 5 triggered</span>
          </div>
          <AlertList alerts={recentAlerts} />
        </div>
      </div>
    </section>
  );
}
