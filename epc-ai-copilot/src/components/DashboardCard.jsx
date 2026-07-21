/**
 * DashboardCard — thin alias that forwards to MetricCard.
 * Keeps all existing callsites working without changes.
 */
import MetricCard from "./MetricCard";

export default function DashboardCard(props) {
  return <MetricCard {...props} />;
}
