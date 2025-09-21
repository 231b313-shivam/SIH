// frontend/src/App.js
import React, { useState } from "react";

function App() {
  const [workerId, setWorkerId] = useState("");
  const [data, setData] = useState(null);

  const fetchRecords = async () => {
    const res = await fetch(`http://localhost:8000/worker/${workerId}`);
    const json = await res.json();
    setData(json);
  };

  return (
    <div className="p-6 text-center">
      <h1 className="text-2xl font-bold">Migrant Worker Health Records</h1>
      <input
        type="text"
        placeholder="Enter Worker ID"
        value={workerId}
        onChange={(e) => setWorkerId(e.target.value)}
        className="border p-2 m-2"
      />
      <button onClick={fetchRecords} className="bg-blue-500 text-white px-4 py-2">
        Fetch Records
      </button>

      {data && (
        <div className="mt-4 text-left">
          <h2 className="font-bold">Worker: {data.worker}</h2>
          <p>Preferred Language: {data.language}</p>
          <h3 className="mt-2">Records:</h3>
          <ul>
            {data.records.map((rec, idx) => (
              <li key={idx}>
                <b>Doctor:</b> {rec.doctor_name} | <b>Diagnosis:</b> {rec.diagnosis} | <b>Prescription:</b> {rec.prescription}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
