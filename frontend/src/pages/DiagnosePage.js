import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import API from "../services/api";

function DiagnosePage() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user"));

  const [datasets, setDatasets] = useState([]);
  const [datasetName, setDatasetName] = useState("");
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      const res = await API.get("/datasets");
      setDatasets(res.data.available_datasets);
      if (res.data.available_datasets.length > 0) {
        setDatasetName(res.data.available_datasets[0]);
      }
    } catch (err) {
      console.log(err);
    }
  };

  const handleDiagnose = async () => {
    if (!file) {
      alert("Please upload medical image");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("user_id", user.id);
    formData.append("dataset_name", datasetName);
    formData.append("file", file);

    try {
      const res = await API.post("/diagnose", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      localStorage.setItem("diagnosis_result", JSON.stringify(res.data));
      navigate("/result");
    } catch (err) {
      alert("Diagnosis failed");
      console.log(err);
    }

    setLoading(false);
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
        {/* HERO */}
        <div style={heroBanner}>
          <h1 style={{ margin: 0 }}>AI Medical Diagnosis Workstation</h1>
          <p style={{ marginTop: "10px", opacity: 0.9 }}>
            Upload clinical scan and execute diagnosis on dynamically trained medical AI modules
          </p>
        </div>

        {/* ACTIVE DATASETS */}
        <div style={datasetStrip}>
          {datasets.map((d, i) => (
            <div key={i} style={datasetCard}>{d}</div>
          ))}
        </div>

        {/* MAIN GRID */}
        <div style={mainGrid}>
          <div style={uploadCard}>
            <h2>Diagnosis Input Console</h2>

            <label>Select Dataset Module</label>
            <select
              value={datasetName}
              onChange={(e) => setDatasetName(e.target.value)}
              style={selectStyle}
            >
              {datasets.map((d, i) => (
                <option key={i} value={d}>
                  {d}
                </option>
              ))}
            </select>

            <label style={{ marginTop: "20px", display: "block" }}>
              Upload Medical Scan
            </label>
            <input
              type="file"
              onChange={(e) => {
                setFile(e.target.files[0]);
                setPreview(URL.createObjectURL(e.target.files[0]));
              }}
              style={{ marginTop: "10px" }}
            />

            {preview && (
              <div style={previewBox}>
                <img
                  src={preview}
                  alt="preview"
                  style={{
                    width: "100%",
                    maxHeight: "280px",
                    objectFit: "contain",
                    borderRadius: "12px"
                  }}
                />
              </div>
            )}

            <button onClick={handleDiagnose} style={runBtn}>
              {loading ? "Running AI Diagnostic Pipeline..." : "Run AI Diagnosis"}
            </button>
          </div>

          <div style={featureCard}>
            <h2>Integrated AI Diagnostic Engines</h2>

            <div style={featureMini}>✔ GAN Synthetic Augmentation Enabled</div>
            <div style={featureMini}>✔ SSL Feature Representation Loaded</div>
            <div style={featureMini}>✔ CNN Disease Classifier Active</div>
            <div style={featureMini}>✔ GradCAM Explainability Available</div>
            <div style={featureMini}>✔ PDF Clinical Report Generator</div>
            <div style={featureMini}>✔ MedIntel AI Doctor Copilot Ready</div>

            <div style={noteBox}>
              Selected uploaded scan will be processed through the universal medical
              inference pipeline and a confidence-aware clinical intelligence report
              will be generated automatically.
            </div>
          </div>
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

const datasetStrip = {
  display: "flex",
  gap: "15px",
  marginTop: "20px"
};

const datasetCard = {
  background: "#dbeafe",
  color: "#1d4ed8",
  padding: "10px 18px",
  borderRadius: "10px",
  fontWeight: "600"
};

const mainGrid = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: "20px",
  marginTop: "25px"
};

const uploadCard = {
  background: "white",
  padding: "25px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const featureCard = {
  background: "white",
  padding: "25px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const selectStyle = {
  width: "100%",
  padding: "12px",
  marginTop: "10px",
  borderRadius: "10px",
  border: "1px solid #cbd5e1"
};

const previewBox = {
  marginTop: "20px",
  background: "#f8fafc",
  padding: "15px",
  borderRadius: "14px"
};

const featureMini = {
  background: "#f8fafc",
  padding: "12px",
  borderRadius: "10px",
  marginTop: "12px"
};

const noteBox = {
  marginTop: "25px",
  background: "#dbeafe",
  padding: "15px",
  borderRadius: "12px",
  lineHeight: "1.7",
  color: "#1e3a8a"
};

const runBtn = {
  width: "100%",
  padding: "14px",
  marginTop: "25px",
  background: "#2563eb",
  color: "white",
  border: "none",
  cursor: "pointer",
  borderRadius: "10px"
};

export default DiagnosePage;