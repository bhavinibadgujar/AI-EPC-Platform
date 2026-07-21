import { motion } from "framer-motion";

export default function PulseCircle() {
  return (
    <span className="pulse-circle" aria-hidden="true">
      <motion.span
        animate={{ scale: [1, 1.9, 1], opacity: [0.75, 0, 0.75] }}
        transition={{ repeat: Infinity, duration: 1.8, ease: "easeOut" }}
      />
      <span />
    </span>
  );
}
