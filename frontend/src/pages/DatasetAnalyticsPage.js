import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import API from "../services/api";

function DatasetAnalyticsPage() {
  const [stats, setStats] = useState({});

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await API.get("/admin/dataset-analytics");
      setStats(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div style={{ display: "flex", background: "#edf2f7" }}>
      <Sidebar />

      <div style={{
        marginLeft: "260px",
        padding: "25px",
        width: "100%",
        minHeight: "100vh"
      }}>
        <div style={heroBanner}>
          <h1 style={{ margin: 0 }}>Medical AI Deployment Analytics Center</h1>
          <p style={{ marginTop: "10px", opacity: 0.9 }}>
            Institutional monitoring dashboard for universal model registry and clinical usage intelligence
          </p>
        </div>

        <div style={metricGrid}>
          <div style={metricCard}>
            <h3>Active Datasets</h3>
            <h1>{stats.active_datasets}</h1>
          </div>

          <div style={metricCard}>
            <h3>Total Disease Classes</h3>
            <h1>{stats.total_classes}</h1>
          </div>

          <div style={metricCard}>
            <h3>Generated Diagnosis Reports</h3>
            <h1>{stats.total_reports}</h1>
          </div>

          <div style={metricCard}>
            <h3>Latest Onboarded Dataset</h3>
            <h1>{stats.latest_dataset}</h1>
          </div>
        </div>

        <div style={midGrid}>
          <div style={bigCard}>
            <h2>AI Engine Registry</h2>

            <div style={engineBox}>✔ Universal GAN Synthetic Augmentation</div>
            <div style={engineBox}>✔ FAST SSL Feature Learning</div>
            <div style={engineBox}>✔ CNN Disease Classification</div>
            <div style={engineBox}>✔ GradCAM Explainability Layer</div>
            <div style={engineBox}>✔ OpenRouter Medical Copilot</div>
          </div>

          <div style={bigCard}>
            <h2>Model Deployment Summary</h2>
            <p style={para}>
              The MedIntel AI universal deployment registry currently manages {stats.active_datasets} autonomous
              medical datasets comprising {stats.total_classes} disease classes. A cumulative total of {stats.total_reports}
              clinical diagnosis reports have been generated through the runtime inference engine. The latest successfully
              onboarded dataset into the plug-and-play model registry is <strong>{stats.latest_dataset}</strong>.
            </p>
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
  borderRadius: "18px"
};

const metricGrid = {
  display: "grid",
  gridTemplateColumns: "repeat(4, 1fr)",
  gap: "20px",
  marginTop: "25px"
};

const metricCard = {
  background: "white",
  padding: "22px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const midGrid = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: "20px",
  marginTop: "25px"
};

const bigCard = {
  background: "white",
  padding: "25px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const engineBox = {
  background: "#dbeafe",
  padding: "12px",
  borderRadius: "10px",
  marginTop: "12px"
};

const para = {
  lineHeight: "1.9",
  textAlign: "justify"
};

export default DatasetAnalyticsPage;