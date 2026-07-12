import { Button, Checkbox, FormControlLabel } from "@mui/material";
import { useState } from "react";
import { FaLock, FaUserAlt } from "react-icons/fa";
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
          <span className="logo-mark">EPC</span>
          <div>
            <h1>EPC AI Copilot</h1>
            <p>Sign in to your project intelligence workspace.</p>
          </div>
        </div>

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

        <div className="login-options">
          <FormControlLabel
            control={
              <Checkbox
                checked={form.remember}
                onChange={(event) => setForm({ ...form, remember: event.target.checked })}
              />
            }
            label="Remember me"
          />
          <a href="/login">Forgot Password?</a>
        </div>

        <Button type="submit" variant="contained" disabled={isSubmitting}>
          {isSubmitting ? "Signing in" : "Login"}
        </Button>
      </form>
    </section>
  );
}
