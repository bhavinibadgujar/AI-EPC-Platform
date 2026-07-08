import { motion } from "framer-motion";
import PulseCircle from "../animations/PulseCircle";

export default function AIStatus() {
  return (
    <section className="ai-status-panel" aria-label="AI status">
      <div className="ai-status-copy">
        <span className="section-label">AI Status</span>
        <h3>Copilot online and monitoring project signals</h3>
        <p>18 agents active across specification review, procurement risk, and commissioning readiness.</p>
      </div>

      <motion.div
        className="ai-status-indicator"
        initial={{ opacity: 0, scale: 0.92 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.35 }}
      >
        <PulseCircle />
        <span>Online</span>
      </motion.div>
    </section>
  );
}
