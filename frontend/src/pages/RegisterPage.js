import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../services/api";

function RegisterPage() {
  const navigate = useNavigate();

  const [full_name, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    try {
      const res = await API.post("/register", {
        full_name,
        email,
        password
      });

      if (res.data.user) {
        alert("Registration successful");
        navigate("/");
      } else {
        alert(res.data.message);
      }
    } catch (err) {
      alert("Registration failed");
    }
  };

  return (
    <div style={{
      height: "100vh",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      background: "linear-gradient(to right, #e0f2fe, #f8fafc)"
    }}>
      <div style={{
        width: "400px",
        padding: "35px",
        background: "white",
        borderRadius: "15px",
        boxShadow: "0 10px 25px rgba(0,0,0,0.1)"
      }}>
        <h2>MedIntel AI Register</h2>

        <input
          type="text"
          placeholder="Full Name"
          value={full_name}
          onChange={(e)=>setFullName(e.target.value)}
          style={{width:"100%",padding:"12px",marginTop:"20px"}}
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
          style={{width:"100%",padding:"12px",marginTop:"15px"}}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
          style={{width:"100%",padding:"12px",marginTop:"15px"}}
        />

        <button
          onClick={handleRegister}
          style={{
            width:"100%",
            padding:"12px",
            marginTop:"20px",
            background:"#16a34a",
            color:"white",
            border:"none",
            cursor:"pointer"
          }}
        >
          Register
        </button>

        <p style={{marginTop:"15px"}}>
          Already have account? <Link to="/">Login</Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;