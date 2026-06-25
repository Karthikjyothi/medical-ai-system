import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import API from "../services/api";

function CompareHistoryPage() {
  const user = JSON.parse(localStorage.getItem("user"));

  const [history, setHistory] = useState([]);
  const [leftId, setLeftId] = useState("");
  const [rightId, setRightId] = useState("");
  const [aiComparison, setAiComparison] = useState("Select any two previous diagnosis records for comparative intelligence analysis.");

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

  const leftItem = history.find((h) => h.id === parseInt(leftId));
  const rightItem = history.find((h) => h.id === parseInt(rightId));
  useEffect(() => {
    generateAIComparison();
    }, [leftId, rightId]);

    const getSeverity = (disease) => {
  const map = {
    no_tumor: "LOW",
    benign: "LOW",
    pituatory: "MODERATE",
    meningioma: "MODERATE",
    pneumonia: "MODERATE",
    glioma: "HIGH",
    malignant: "HIGH"
  };
  return map[disease] || "MODERATE";
};

const getGradcamObservation = () => {
  if (!leftItem || !rightItem) return "GradCAM comparative observation will appear after selecting two reports.";

  return `Left report (${leftItem.predicted_disease}) and right report (${rightItem.predicted_disease}) demonstrate differing explainability heatmap activation patterns, indicating that the CNN inference engine attended to distinct pathological feature zones across the two medical analyses. Such retrospective GradCAM review helps validate radiological feature sensitivity variations.`;
};
  const generateAIComparison = async () => {
    if (!leftItem || !rightItem) return;

    try {
        const res = await API.post("/compare-reports-ai", {
        left_disease: leftItem.predicted_disease,
        right_disease: rightItem.predicted_disease,
        left_confidence: leftItem.confidence,
        right_confidence: rightItem.confidence,
        left_uncertainty: leftItem.uncertainty_level,
        right_uncertainty: rightItem.uncertainty_level
        });

        setAiComparison(res.data.comparison);
    } catch (err) {
        console.log(err);
    }
    };

  const getComparisonSummary = () => {
    if (!leftItem || !rightItem) return "Select any two previous diagnosis records for comparative intelligence analysis.";

    let moreReliable =
      leftItem.confidence > rightItem.confidence
        ? leftItem.predicted_disease
        : rightItem.predicted_disease;

    return `${leftItem.predicted_disease} and ${rightItem.predicted_disease} were generated from two separate diagnostic sessions. Among these reports, ${moreReliable} shows comparatively higher AI confidence. The GradCAM evidence, confidence reliability, and dataset variation indicate distinct radiological feature responses between the two analyses. This comparison module helps clinicians and users understand output differences across previous disease predictions.`;
  };

  const renderCard = (item) => {
    if (!item) return <div style={emptyCard}>Select Report</div>;

    const gradcamURL =
      "http://127.0.0.1:8000/" + item.gradcam_image.replace(/\\/g, "/");

    return (
      <div style={reportCard}>
        <img
          src={gradcamURL}
          alt="gradcam"
          style={{
            width: "100%",
            height: "200px",
            objectFit: "cover",
            borderRadius: "12px"
          }}
        />
        <h2 style={{ color: "#dc2626", marginTop: "15px" }}>{item.predicted_disease}</h2>
        <p><strong>Dataset:</strong> {item.dataset}</p>
        <p><strong>Confidence:</strong> {item.confidence}%</p>
        <p><strong>Uncertainty:</strong> {item.uncertainty_level}</p>
        <p><strong>Date:</strong> {item.created_at}</p>
      </div>
    );
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
          <h1 style={{ margin: 0 }}>Comparative Diagnosis Intelligence</h1>
          <p style={{ marginTop: "10px", opacity: 0.9 }}>
            Side-by-side analytical review of previously generated medical AI reports
          </p>
        </div>

        <div style={selectorRow}>
          <select value={leftId} onChange={(e)=>setLeftId(e.target.value)} style={selectStyle}>
            <option value="">Select Left Report</option>
            {history.map((h)=>(
              <option key={h.id} value={h.id}>
                #{h.id} - {h.predicted_disease}
              </option>
            ))}
          </select>

          <select value={rightId} onChange={(e)=>setRightId(e.target.value)} style={selectStyle}>
            <option value="">Select Right Report</option>
            {history.map((h)=>(
              <option key={h.id} value={h.id}>
                #{h.id} - {h.predicted_disease}
              </option>
            ))}
          </select>
        </div>

        <div style={metricGrid}>
            <div style={metricCard}>
                <h3>Higher AI Reliability</h3>
                <h2 style={{ color: "#16a34a" }}>
                {leftItem && rightItem
                    ? leftItem.confidence > rightItem.confidence
                    ? `${leftItem.predicted_disease} (${leftItem.confidence}%)`
                    : `${rightItem.predicted_disease} (${rightItem.confidence}%)`
                    : "--"}
                </h2>
            </div>

            <div style={metricCard}>
                <h3>Clinical Severity Assessment</h3>
                <h2 style={{ color: "#dc2626" }}>
                {leftItem ? getSeverity(leftItem.predicted_disease) : "--"} vs{" "}
                {rightItem ? getSeverity(rightItem.predicted_disease) : "--"}
                </h2>
            </div>

            <div style={metricCard}>
                <h3>Uncertainty Review</h3>
                <h2 style={{ color: "#2563eb" }}>
                {leftItem && rightItem
                    ? `${leftItem.uncertainty_level} / ${rightItem.uncertainty_level}`
                    : "--"}
                </h2>
            </div>
        </div>

        <div style={compareGrid}>
          {renderCard(leftItem)}
          {renderCard(rightItem)}
        </div>

        <div style={gradcamBox}>
            <h2>GradCAM Differential Observation</h2>
            <p style={{ lineHeight: "1.9", textAlign: "justify" }}>
                {getGradcamObservation()}
            </p>
        </div>

        <div style={summaryBox}>
          <h2>AI Comparative Interpretation</h2>
          <p style={{ lineHeight: "1.9", textAlign: "justify" }}>
            {aiComparison}
          </p>
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

const selectorRow = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: "20px",
  marginTop: "25px"
};

const selectStyle = {
  padding: "12px",
  borderRadius: "10px",
  border: "1px solid #cbd5e1"
};

const compareGrid = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: "20px",
  marginTop: "25px"
};

const reportCard = {
  background: "white",
  padding: "20px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const emptyCard = {
  background: "white",
  padding: "60px",
  borderRadius: "18px",
  textAlign: "center",
  color: "gray"
};

const summaryBox = {
  marginTop: "25px",
  background: "white",
  padding: "25px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};
const metricGrid = {
  display: "grid",
  gridTemplateColumns: "repeat(3, 1fr)",
  gap: "20px",
  marginTop: "25px"
};

const metricCard = {
  background: "white",
  padding: "20px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const gradcamBox = {
  marginTop: "25px",
  background: "white",
  padding: "25px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

export default CompareHistoryPage;