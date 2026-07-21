import { motion } from "framer-motion";
import PulseCircle from "../animations/PulseCircle";

export default function AIStatus() {
  return (
    <section className="ai-status-panel" aria-label="AI system status">
      <div className="ai-status-copy">
        <span className="section-label">AI Operations</span>

        <h3>Real-time EPC intelligence is active</h3>

        <p>
          Monitoring project compliance, procurement, schedule risk and
          commissioning activities across connected project data.
        </p>
      </div>

      <motion.div
        className="ai-status-indicator"
        initial={{ opacity: 0, scale: 0.92 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.35 }}
      >
        <PulseCircle />
        <span>System Online</span>
      </motion.div>
    </section>
  );
}