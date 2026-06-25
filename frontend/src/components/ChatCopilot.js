import { useState } from "react";
import API from "../services/api";

function ChatCopilot({ diagnosis }) {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello, I am MedIntel AI Doctor Copilot. I can explain this diagnosis, its seriousness, symptoms, precautions, confidence level, and recommended next steps."
    }
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState("sess_" + Date.now());

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const currentInput = input;

    const userMsg = { sender: "user", text: currentInput };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    const formData = new FormData();
    formData.append("session_id", sessionId);
    formData.append("user_query", currentInput);
    formData.append("disease_name", diagnosis.predicted_disease);
    formData.append("confidence", diagnosis.confidence);
    formData.append("uncertainty_level", diagnosis.uncertainty_level);

    try {
      const res = await API.post("/chat", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      const botMsg = { sender: "bot", text: res.data.response };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "AI Copilot temporarily unavailable." }
      ]);
    }

    setLoading(false);
  };

  return (
    <div style={wrapper}>
      <div style={headerBox}>
        <h2 style={{ margin: 0 }}>MedIntel AI Doctor Copilot</h2>
        <p style={{ marginTop: "8px", color: "#475569" }}>
          Interactive post-diagnosis clinical explanation assistant
        </p>
      </div>

      <div style={chatWindow}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              textAlign: msg.sender === "user" ? "right" : "left",
              marginBottom: "14px"
            }}
          >
            <span
              style={{
                display: "inline-block",
                background:
                  msg.sender === "user" ? "#2563eb" : "#e2e8f0",
                color: msg.sender === "user" ? "white" : "#111827",
                padding: "12px 16px",
                borderRadius: "14px",
                maxWidth: "72%",
                lineHeight: "1.6"
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}

        {loading && (
          <div style={{ textAlign: "left", marginBottom: "14px" }}>
            <span style={typingBubble}>AI analyzing medical context...</span>
          </div>
        )}
      </div>

      <div style={inputRow}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask about this diagnosis..."
          style={inputStyle}
        />
        <button onClick={sendMessage} style={sendBtn}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

const wrapper = {
  marginTop: "30px",
  background: "white",
  padding: "25px",
  borderRadius: "18px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const headerBox = {
  borderBottom: "1px solid #e2e8f0",
  paddingBottom: "12px"
};

const chatWindow = {
  height: "320px",
  overflowY: "auto",
  marginTop: "18px",
  padding: "15px",
  borderRadius: "12px",
  background: "#f8fafc",
  border: "1px solid #e2e8f0"
};

const typingBubble = {
  display: "inline-block",
  background: "#e2e8f0",
  padding: "10px 14px",
  borderRadius: "12px",
  color: "#334155"
};

const inputRow = {
  display: "flex",
  gap: "10px",
  marginTop: "18px"
};

const inputStyle = {
  flex: 1,
  padding: "13px",
  borderRadius: "10px",
  border: "1px solid #cbd5e1",
  fontSize: "14px"
};

const sendBtn = {
  padding: "13px 22px",
  background: "#2563eb",
  color: "white",
  border: "none",
  borderRadius: "10px",
  cursor: "pointer"
};

export default ChatCopilot;