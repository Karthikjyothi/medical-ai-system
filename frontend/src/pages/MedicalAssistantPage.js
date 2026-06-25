import { useState } from "react";
import Sidebar from "../components/Sidebar";
import API from "../services/api";

function MedicalAssistantPage() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello, I am MedIntel MedicalGPT. Ask me any medical question related to diseases, symptoms, treatments, nutrition, preventive care, or healthcare guidance."
    }
  ]);

  const [input, setInput] = useState("");
  const [sessionId] = useState("medgpt_" + Date.now());
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [recognitionObj, setRecognitionObj] = useState(null);

  const startVoiceInput = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Voice recognition not supported in this browser");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event) => {
      let transcript = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      setInput(transcript);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.onerror = () => {
      setIsListening(false);
    };

    recognition.start();
    setRecognitionObj(recognition);
  };

  const stopVoiceInput = () => {
    if (recognitionObj) {
      recognitionObj.stop();
      setIsListening(false);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    const formData = new FormData();
    formData.append("session_id", sessionId);
    formData.append("user_query", input);

    try {
      const res = await API.post("/medical-assistant-chat", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      const botMsg = { sender: "bot", text: res.data.response };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Medical AI assistant temporarily unavailable." }
      ]);
    }

    setInput("");
    setLoading(false);
  };

  return (
    <div style={{ display: "flex", background: "#edf2f7" }}>
      <Sidebar />

      <div style={{
        marginLeft: "260px",
        width: "100%",
        padding: "25px",
        minHeight: "100vh"
      }}>
        <div style={heroBanner}>
          <h1 style={{ margin: 0 }}>MedIntel MedicalGPT Assistant</h1>
          <p style={{ marginTop: "10px", opacity: 0.9 }}>
            Persistent conversational medical intelligence assistant for healthcare guidance
          </p>
        </div>

        <div style={chatContainer}>
          <div style={chatWindow}>
            {messages.map((msg, i) => (
              <div
                key={i}
                style={{
                  display: "flex",
                  justifyContent: msg.sender === "user" ? "flex-end" : "flex-start",
                  marginBottom: "18px"
                }}
              >
                <div
                  style={{
                    maxWidth: "72%",
                    padding: "14px 18px",
                    borderRadius: "14px",
                    background: msg.sender === "user" ? "#2563eb" : "white",
                    color: msg.sender === "user" ? "white" : "#111827",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
                    lineHeight: "1.8",
                    whiteSpace: "pre-line",
                    textAlign: "justify"
                  }}
                >
                  {msg.text}
                </div>
              </div>
            ))}

            {isListening && (
              <p style={{ color: "#dc2626", fontWeight: "600", marginTop: "10px" }}>
                🎙 Listening... speech is being transcribed live
              </p>
            )}
          </div>

          <div style={inputBar}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask any medical question..."
              style={inputStyle}
            />

            {!isListening ? (
              <button onClick={startVoiceInput} style={voiceBtn}>
                🎤 Speak
              </button>
            ) : (
              <button onClick={stopVoiceInput} style={stopBtn}>
                ⏹ Stop
              </button>
            )}

            <button onClick={sendMessage} style={sendBtn}>
              Send
            </button>
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

const chatContainer = {
  marginTop: "25px",
  background: "white",
  borderRadius: "18px",
  padding: "20px",
  boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
};

const chatWindow = {
  height: "520px",
  overflowY: "auto",
  padding: "15px",
  background: "#f8fafc",
  borderRadius: "15px"
};

const inputBar = {
  display: "flex",
  gap: "12px",
  marginTop: "18px"
};

const inputStyle = {
  flex: 1,
  padding: "14px",
  borderRadius: "10px",
  border: "1px solid #cbd5e1"
};

const sendBtn = {
  padding: "14px 24px",
  background: "#2563eb",
  color: "white",
  border: "none",
  borderRadius: "10px",
  cursor: "pointer"
};

const voiceBtn = {
  padding: "14px 20px",
  background: "#16a34a",
  color: "white",
  border: "none",
  borderRadius: "10px",
  cursor: "pointer"
};

const stopBtn = {
  padding: "14px 20px",
  background: "#dc2626",
  color: "white",
  border: "none",
  borderRadius: "10px",
  cursor: "pointer"
};

export default MedicalAssistantPage;