import { Button, Checkbox, FormControlLabel } from "@mui/material";
import { useState } from "react";
import { FaLock, FaRocket, FaUserAlt } from "react-icons/fa";
import { login } from "../services/api";
import FloatingParticles from "../animations/FloatingParticles";
import "../styles/login.css";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "", remember: true });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);
    try {
      await login(form);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="login-page">
      <FloatingParticles />
      <form className="login-card" onSubmit={handleSubmit}>
        <div className="login-brand">
          <div className="login-logo">
            <FaRocket />
          </div>
          <div>
            <h1>EPC Orbit</h1>
            <p>AI Control Tower for EPC Projects</p>
          </div>
        </div>

        <div className="login-fields">
          <label className="input-field">
            <FaUserAlt />
            <input
              value={form.username}
              onChange={(event) => setForm({ ...form, username: event.target.value })}
              placeholder="Username"
              autoComplete="username"
              required
            />
          </label>

          <label className="input-field">
            <FaLock />
            <input
              value={form.password}
              onChange={(event) => setForm({ ...form, password: event.target.value })}
              placeholder="Password"
              type="password"
              autoComplete="current-password"
              required
            />
          </label>
        </div>

        <div className="login-options">
          <FormControlLabel
            control={
              <Checkbox
                checked={form.remember}
                onChange={(event) => setForm({ ...form, remember: event.target.checked })}
                sx={{ color: "#64d4c8", "&.Mui-checked": { color: "#64d4c8" } }}
              />
            }
            label="Remember me"
            sx={{ color: "#a0b5c8" }}
          />
          <a href="/login" style={{ color: "#64d4c8", fontSize: 13 }}>Forgot Password?</a>
        </div>

        <Button
          type="submit"
          variant="contained"
          disabled={isSubmitting}
          fullWidth
          sx={{
            background: "linear-gradient(135deg, #64d4c8, #68a7ff)",
            color: "#060e1a",
            fontWeight: 700,
            py: 1.5,
            borderRadius: 2,
            "&:hover": { background: "linear-gradient(135deg, #5bc0b5, #5a9aff)" }
          }}
        >
          {isSubmitting ? "Signing in to EPC Orbit…" : "Sign in to EPC Orbit"}
        </Button>

        <p className="login-footer">
          EPC Orbit · Enterprise AI Platform for EPC Projects
        </p>
      </form>
    </section>
  );
}
