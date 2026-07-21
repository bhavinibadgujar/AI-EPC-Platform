import { motion } from "framer-motion";
import { FaCheck, FaSpinner } from "react-icons/fa";

const STEPS = [
  "Reading Specification",
  "Extracting Clauses",
  "Comparing Documents",
  "Detecting Deviations",
  "Calculating Risks",
  "Searching Knowledge Base",
  "Generating Recommendations",
  "Building Executive Summary"
];

/**
 * Loader — premium animated loading pipeline.
 * Each step animates in sequentially with a checkmark.
 */
export default function Loader({ label = "Running AI Analysis" }) {
  return (
    <div className="loading-pipeline" role="status" aria-live="polite">
      <div className="loading-pipeline-header">
        <motion.div
          className="pipeline-spinner"
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: 1.4, ease: "linear" }}
        >
          <FaSpinner />
        </motion.div>
        <p>{label}</p>
      </div>

      <div className="pipeline-steps">
        {STEPS.map((step, index) => (
          <motion.div
            className="pipeline-step"
            key={step}
            initial={{ opacity: 0.25, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.14, duration: 0.3 }}
          >
            <motion.i
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: index * 0.14 + 0.1, duration: 0.22, type: "spring" }}
            >
              <FaCheck />
            </motion.i>
            <span>{step}</span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}