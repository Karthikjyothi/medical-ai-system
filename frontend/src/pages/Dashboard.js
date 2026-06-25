import Sidebar from "../components/Sidebar";

function Dashboard() {
  const user = JSON.parse(localStorage.getItem("user"));

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
          <h1 style={{ margin: 0 }}>Welcome, {user?.full_name}</h1>
          <p style={{ marginTop: "10px", opacity: 0.9 }}>
            MedIntel AI Universal Medical Intelligence Dashboard
          </p>
        </div>

        {/* TOP ANALYTICS */}
        <div style={topGrid}>
          <div style={cardStyle}>
            <h3>Diagnosis Modules Loaded</h3>
            <h1 style={{ color: "#2563eb" }}>3 Active</h1>
            <p>brain_tumor • lung_disease • skincancer</p>
          </div>

          <div style={cardStyle}>
            <h3>AI Core Engines</h3>
            <h1 style={{ color: "#16a34a" }}>GAN + SSL + CNN</h1>
            <p>Universal autonomous training enabled</p>
          </div>

          <div style={cardStyle}>
            <h3>Medical Copilot Status</h3>
            <h1 style={{ color: "#9333ea" }}>OpenRouter Live</h1>
            <p>Clinical AI consultation active</p>
          </div>

          <div style={cardStyle}>
            <h3>Explainability Layer</h3>
            <h1 style={{ color: "#dc2626" }}>GradCAM Ready</h1>
            <p>Confidence and uncertainty supported</p>
          </div>
        </div>

        {/* MID SECTION */}
        <div style={midGrid}>
          <div style={overviewCard}>
            <h2>Platform Overview</h2>
            <p style={para}>
              MedIntel AI is a universal plug-and-play medical intelligence platform designed to
              automate disease diagnosis from medical imaging datasets using a multi-stage deep
              learning workflow. The system supports dynamic onboarding of newly introduced medical
              repositories and performs GAN synthetic augmentation, self-supervised feature learning,
              CNN classification, explainable GradCAM visualization, PDF clinical reporting, and
              conversational AI-based patient guidance.
            </p>
          </div>

          <div style={overviewCard}>
            <h2>Universal Pipeline Status</h2>

            <div style={pipelineBox}>Named Dataset Intake</div>
            <div style={arrow}>↓</div>
            <div style={pipelineBox}>GAN Synthetic Augmentation</div>
            <div style={arrow}>↓</div>
            <div style={pipelineBox}>SSL Representation Learning</div>
            <div style={arrow}>↓</div>
            <div style={pipelineBox}>CNN Disease Classification</div>
            <div style={arrow}>↓</div>
            <div style={pipelineBox}>Dynamic Model Deployment</div>
          </div>
        </div>

        {/* LOWER FEATURE GRID */}
        <div style={bottomGrid}>
          <div style={miniCard}>
            <h3>✔ Multi Dataset Diagnosis</h3>
            <p>Single platform supports heterogeneous medical imaging domains.</p>
          </div>

          <div style={miniCard}>
            <h3>✔ AI Report Automation</h3>
            <p>Clinical PDF summaries generated after every diagnosis session.</p>
          </div>

          <div style={miniCard}>
            <h3>✔ Historical Tracking</h3>
            <p>User diagnosis records and GradCAM evidence preserved in database.</p>
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

const topGrid = {
  display: "grid",
  gridTemplateColumns: "repeat(4, 1fr)",
  gap: "20px",
  marginTop: "25px"
};

const midGrid = {
  display: "grid",
  gridTemplateColumns: "1.3fr 1fr",
  gap: "20px",
  marginTop: "25px"
};

const bottomGrid = {
  display: "grid",
  gridTemplateColumns: "repeat(3, 1fr)",
  gap: "20px",
  marginTop: "25px"
};

const cardStyle = {
  background: "white",
  padding: "22px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const overviewCard = {
  background: "white",
  padding: "22px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const miniCard = {
  background: "white",
  padding: "20px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const para = {
  lineHeight: "1.9",
  textAlign: "justify",
  color: "#334155"
};

const pipelineBox = {
  background: "#dbeafe",
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

export default Dashboard;