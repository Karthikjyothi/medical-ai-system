import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../services/api";

function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const res = await API.post("/login", {
        email,
        password
      });

      if (res.data.user) {
        localStorage.setItem("user", JSON.stringify(res.data.user));
        navigate("/dashboard");
      } else {
        alert(res.data.message);
      }
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <div style={{
      height: "100vh",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      background: "linear-gradient(to right, #dbeafe, #f0f9ff)"
    }}>
      <div style={{
        width: "400px",
        padding: "35px",
        background: "white",
        borderRadius: "15px",
        boxShadow: "0 10px 25px rgba(0,0,0,0.1)"
      }}>
        <h2>MedIntel AI Login</h2>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
          style={{width:"100%",padding:"12px",marginTop:"20px"}}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
          style={{width:"100%",padding:"12px",marginTop:"15px"}}
        />

        <button
          onClick={handleLogin}
          style={{
            width:"100%",
            padding:"12px",
            marginTop:"20px",
            background:"#2563eb",
            color:"white",
            border:"none",
            cursor:"pointer"
          }}
        >
          Login
        </button>

        <p style={{marginTop:"15px"}}>
          New user? <Link to="/register">Register Here</Link>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;