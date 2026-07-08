import { motion } from "framer-motion";

export default function ActivityTimeline({ items }) {
  return (
    <div className="activity-timeline">
      {items.map((item, index) => (
        <motion.div
          className="timeline-item"
          key={`${item.title}-${item.time}`}
          initial={{ opacity: 0, x: -14 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.06 }}
        >
          <span className={`timeline-dot timeline-dot-${item.type}`} />
          <div>
            <strong>{item.title}</strong>
            <p>{item.detail}</p>
          </div>
          <time>{item.time}</time>
        </motion.div>
      ))}
    </div>
  );
}
