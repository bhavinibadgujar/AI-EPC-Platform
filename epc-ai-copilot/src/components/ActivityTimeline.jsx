import { motion } from "framer-motion";

export default function ActivityTimeline({ items = [] }) {
  return (
    <div className="activity-timeline">
      {items.map((item, index) => (
        <motion.article
          className="timeline-item"
          key={`${item.title}-${item.time}-${index}`}
          initial={{ opacity: 0, x: -16 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{
            delay: index * 0.06,
            duration: 0.3,
          }}
        >
          <span
            className={`timeline-dot timeline-dot-${item.type}`}
            aria-hidden="true"
          />

          <div className="timeline-content">
            <strong>{item.title}</strong>

            <p>{item.detail}</p>
          </div>

          <time dateTime={item.time}>{item.time}</time>
        </motion.article>
      ))}
    </div>
  );
}