import { motion } from "framer-motion";

/**
 * SeverityBadge — consistent color-coded severity indicator.
 * severity: "Critical" | "High" | "Medium" | "Low"
 */
export default function SeverityBadge({ severity }) {
  const map = {
    Critical: { cls: "critical", dot: "🔴" },
    High:     { cls: "high",     dot: "🟠" },
    Medium:   { cls: "medium",   dot: "🟡" },
    Low:      { cls: "low",      dot: "🟢" },
    // legacy aliases
    Major:    { cls: "high",     dot: "🟠" },
    Minor:    { cls: "low",      dot: "🟢" },
  };
  const { cls = "medium", dot = "🟡" } = map[severity] ?? {};

  return (
    <span className={`status-pill ${cls}`}>
      {dot} {severity}
    </span>
  );
}
