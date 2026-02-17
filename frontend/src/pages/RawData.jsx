import React, { useEffect, useState } from "react";
import { api } from "../api/client";
import DataTable from "../components/DataTable";

const PAGE_SIZE = 25;

export default function RawData() {
  const [rows, setRows] = useState([]);
  const [topic, setTopic] = useState("");
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    api
      .get("/sensors/raw", {
        params: {
          limit: PAGE_SIZE,
          offset: page * PAGE_SIZE,
          topic: topic || undefined
        }
      })
      .then((res) => {
        if (mounted) setRows(res.data);
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, [page, topic]);

  return (
    <section className="page">
      <div className="page-header">
        <div>
          <h2>Raw Data</h2>
          <p>Inspect full telemetry payloads and timestamps.</p>
        </div>
        <div className="controls">
          <input
            className="input"
            placeholder="Filter by topic"
            value={topic}
            onChange={(event) => {
              setPage(0);
              setTopic(event.target.value);
            }}
          />
          <button className="button" onClick={() => setPage(Math.max(page - 1, 0))}>
            Prev
          </button>
          <button className="button" onClick={() => setPage(page + 1)}>
            Next
          </button>
        </div>
      </div>

      <div className="panel">
        {loading ? <div className="skeleton">Loading telemetry...</div> : <DataTable rows={rows} />}
      </div>
    </section>
  );
}
