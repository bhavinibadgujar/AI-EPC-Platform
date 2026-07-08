import { motion } from "framer-motion";

export default function Loader({ label = "Loading intelligence" }) {
  return (
    <div className="loader" role="status" aria-live="polite">
      <motion.span
        animate={{ rotate: 360 }}
        transition={{ repeat: Infinity, duration: 1.1, ease: "linear" }}
      />
      <p>{label}</p>
    </div>
  );
}
