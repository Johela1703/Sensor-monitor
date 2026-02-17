import React from "react";

export default function DataTable({ rows }) {
  if (!rows.length) {
    return <div className="empty">No readings available.</div>;
  }

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Topic</th>
            <th>Temp</th>
            <th>Humidity</th>
            <th>Voltage</th>
            <th>Current</th>
            <th>Pressure</th>
            <th>Payload</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              <td>{new Date(row.timestamp).toLocaleString()}</td>
              <td>{row.topic}</td>
              <td>{row.temperature ?? "-"}</td>
              <td>{row.humidity ?? "-"}</td>
              <td>{row.voltage ?? "-"}</td>
              <td>{row.current ?? "-"}</td>
              <td>{row.pressure ?? "-"}</td>
              <td className="payload">{row.raw_payload}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
