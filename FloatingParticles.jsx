import { motion } from "framer-motion";

export default function FloatingParticles() {
  return (
    <div className="floating-particles" aria-hidden="true">
      {[0, 1, 2, 3, 4].map((item) => (
        <motion.span
          key={item}
          animate={{ y: [0, -18, 0], opacity: [0.2, 0.52, 0.2] }}
          transition={{ repeat: Infinity, duration: 4 + item, delay: item * 0.35 }}
        />
      ))}
    </div>
  );
}
