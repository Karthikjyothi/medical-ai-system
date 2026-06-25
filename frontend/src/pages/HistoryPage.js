import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import API from "../services/api";

function HistoryPage() {
  const user = JSON.parse(localStorage.getItem("user"));
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await API.get(`/history/${user.id}`);
      setHistory(res.data.history);
    } catch (err) {
      console.log(err);
    }
  };

  const handleDelete = async (id) => {
    const ok = window.confirm("Delete this diagnosis record?");
    if (!ok) return;

    try {
      await API.delete(`/history/delete/${id}`);
      fetchHistory();
    } catch (err) {
      alert("Delete failed");
    }
  };

  return (
    <div style={{ display: "flex", background: "#edf2f7" }}>
      <Sidebar />

      <div
        style={{
          marginLeft: "260px",
          padding: "25px",
          width: "100%",
          minHeight: "100vh"
        }}
      >
        <div style={heroBanner}>
          <h1 style={{ margin: 0 }}>Medical Diagnosis History Vault</h1>
          <p style={{ marginTop: "10px", opacity: 0.9 }}>
            Review previously generated AI clinical intelligence reports and explainability evidence
          </p>
        </div>

        <div style={historyGrid}>
          {history.map((item) => {
            const gradcamURL =
              "http://127.0.0.1:8000/" + item.gradcam_image.replace(/\\/g, "/");

            const pdfURL =
              "http://127.0.0.1:8000/" + item.pdf_report.replace(/\\/g, "/");

            return (
              <div key={item.id} style={cardStyle}>
                <img
                  src={gradcamURL}
                  alt="gradcam"
                  style={{
                    width: "100%",
                    height: "180px",
                    objectFit: "cover",
                    borderRadius: "12px"
                  }}
                />

                <h2 style={{ marginTop: "15px", color: "#dc2626" }}>
                  {item.predicted_disease}
                </h2>

                <p><strong>Dataset:</strong> {item.dataset}</p>
                <p><strong>Confidence:</strong> {item.confidence}%</p>
                <p><strong>Uncertainty:</strong> {item.uncertainty_level}</p>
                <p><strong>Date:</strong> {item.created_at}</p>

                <div style={{ display: "flex", gap: "10px", marginTop: "15px" }}>
                  <a href={pdfURL} target="_blank" rel="noreferrer" style={{ flex: 1 }}>
                    <button style={pdfBtn}>View PDF</button>
                  </a>

                  <button onClick={() => handleDelete(item.id)} style={deleteBtn}>
                    Delete
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

const heroBanner = {
  background: "linear-gradient(135deg, #0f172a, #1d4ed8)",
  color: "white",
  padding: "28px",
  borderRadius: "18px",
  boxShadow: "0 8px 20px rgba(0,0,0,0.12)"
};

const historyGrid = {
  display: "grid",
  gridTemplateColumns: "repeat(3, 1fr)",
  gap: "20px",
  marginTop: "25px"
};

const cardStyle = {
  background: "white",
  padding: "18px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const pdfBtn = {
  width: "100%",
  padding: "11px",
  background: "#16a34a",
  color: "white",
  border: "none",
  borderRadius: "10px",
  cursor: "pointer"
};

const deleteBtn = {
  flex: 1,
  padding: "11px",
  background: "#dc2626",
  color: "white",
  border: "none",
  borderRadius: "10px",
  cursor: "pointer"
};

export default HistoryPage;