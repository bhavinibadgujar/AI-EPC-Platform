import { motion } from "framer-motion";

/**
 * Enterprise KPI Card
 */

export default function MetricCard({
  title,
  value,
  change,
  description,
  icon,
  tone = "blue",
  trend = "neutral",
}) {
  const trendColor =
    trend === "up"
      ? "var(--c-green)"
      : trend === "down"
      ? "var(--c-critical)"
      : "var(--c-text-muted)";

  return (
    <motion.article
      className={`kpi-card kpi-card-${tone}`}
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{
        y: -6,
        scale: 1.02,
        transition: { duration: 0.18 }
      }}
      transition={{
        duration: 0.35,
        ease: "easeOut"
      }}
    >
      <div className="kpi-card-top">
        <span className="kpi-icon">
          {icon}
        </span>

        {change && (
          <span
            className="kpi-change"
            style={{ color: trendColor }}
          >
            {change}
          </span>
        )}
      </div>

      <span className="kpi-title">
        {title}
      </span>

      <strong className="kpi-value">
        {value}
      </strong>

      {description && (
        <p className="kpi-description">
          {description}
        </p>
      )}
    </motion.article>
  );
}