import { motion } from "framer-motion";

export default function DashboardCard({ title, value, change, icon, tone = "blue" }) {
  return (
    <motion.article
      className={`metric-card metric-card-${tone}`}
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -6 }}
      transition={{ duration: 0.28 }}
    >
      <div className="metric-card-top">
        <span className="metric-icon">{icon}</span>
        {change && <span className="metric-change">{change}</span>}
      </div>
      <span className="metric-title">{title}</span>
      <strong>{value}</strong>
    </motion.article>
  );
}
