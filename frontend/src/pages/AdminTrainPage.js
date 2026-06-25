import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import API from "../services/api";

function AdminTrainPage() {
  const [datasetName, setDatasetName] = useState("");
  const [status, setStatus] = useState("");
  const [activeDataset, setActiveDataset] = useState("");

  const handleTrain = async () => {
    if (!datasetName) {
      alert("Enter dataset name");
      return;
    }

    setActiveDataset(datasetName);
    setStatus("Sending autonomous training request to backend pipeline...");

    try {
      const res = await API.post("/admin/train", {
        dataset_name: datasetName
      });

      setStatus(res.data.message);
    } catch (err) {
      console.log(err);
      setStatus("Training failed.");
    }
  };

  useEffect(() => {
    if (!activeDataset) return;

    const interval = setInterval(async () => {
      try {
        const res = await API.get(`/admin/train-status/${activeDataset}`);
        setStatus(res.data.status);
      } catch (err) {
        console.log(err);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [activeDataset]);

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
          <h1 style={{ margin: 0 }}>Autonomous Medical Dataset Training Console</h1>
          <p style={{ marginTop: "10px", opacity: 0.9 }}>
            Trigger GAN + SSL + CNN universal onboarding for newly introduced medical repositories
          </p>
        </div>

        <div style={mainGrid}>
          {/* LEFT */}
          <div style={trainCard}>
            <h2>Dataset Deployment Request</h2>

            <label>Dataset Folder Name</label>
            <input
              type="text"
              value={datasetName}
              onChange={(e) => setDatasetName(e.target.value)}
              placeholder="Example: skincancer"
              style={inputStyle}
            />

            <button onClick={handleTrain} style={trainBtn}>
              Start Universal Training
            </button>

            <div style={statusBox}>
              <strong>Live Backend Status:</strong>
              <br />
              {status || "Waiting for dataset trigger..."}
            </div>
          </div>

          {/* RIGHT */}
          <div style={pipelineCard}>
            <h2>Autonomous Internal Pipeline</h2>

            <div style={stepBox}>Named Dataset Intake</div>
            <div style={arrow}>↓</div>

            <div style={stepBox}>Universal GAN Training</div>
            <div style={arrow}>↓</div>

            <div style={stepBox}>Synthetic Image Generation</div>
            <div style={arrow}>↓</div>

            <div style={stepBox}>FAST SSL Pretraining</div>
            <div style={arrow}>↓</div>

            <div style={stepBox}>CNN Fine Tuning</div>
            <div style={arrow}>↓</div>

            <div style={stepBox}>Dynamic Model Registry Loading</div>
          </div>
        </div>

        <div style={infoCard}>
          <h2>Universal Dataset Requirements</h2>
          <p style={para}>
            Newly introduced datasets must contain organized train and test folders with
            class-wise medical image subdirectories. Once the dataset folder name is submitted,
            the backend autonomous engine performs synthetic augmentation, self-supervised feature
            learning, classifier optimization, and automatic deployment into the diagnosis runtime
            without requiring manual frontend changes.
          </p>
        </div>
      </div>
    </div>
  );
}

const heroBanner = {
  background: "linear-gradient(135deg, #7f1d1d, #dc2626)",
  color: "white",
  padding: "28px",
  borderRadius: "18px",
  boxShadow: "0 8px 20px rgba(0,0,0,0.12)"
};

const mainGrid = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: "20px",
  marginTop: "25px"
};

const trainCard = {
  background: "white",
  padding: "25px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const pipelineCard = {
  background: "white",
  padding: "25px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const infoCard = {
  marginTop: "25px",
  background: "white",
  padding: "25px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const inputStyle = {
  width: "100%",
  padding: "12px",
  marginTop: "10px",
  borderRadius: "10px",
  border: "1px solid #cbd5e1"
};

const trainBtn = {
  width: "100%",
  padding: "14px",
  marginTop: "20px",
  background: "#dc2626",
  color: "white",
  border: "none",
  borderRadius: "10px",
  cursor: "pointer"
};

const statusBox = {
  marginTop: "25px",
  background: "#fef2f2",
  padding: "15px",
  borderRadius: "12px",
  lineHeight: "1.7",
  color: "#7f1d1d"
};

const stepBox = {
  background: "#fee2e2",
  padding: "12px",
  borderRadius: "10px",
  textAlign: "center",
  fontWeight: "600",
  marginTop: "8px"
};

const arrow = {
  textAlign: "center",
  fontSize: "20px",
  marginTop: "4px"
};

const para = {
  lineHeight: "1.9",
  textAlign: "justify",
  color: "#334155"
};

export default AdminTrainPage;