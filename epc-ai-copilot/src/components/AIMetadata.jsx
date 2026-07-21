/**
 * AIMetadata
 * Displays AI processing metadata beneath AI-generated content.
 */

export default function AIMetadata({
  generated = "2 minutes ago",
  source,
  page,
}) {
  return (
    <div className="ai-metadata" aria-label="AI processing metadata">
      <span>AI Generated</span>

      <span>Analysis Status: Ready</span>

      <span>Updated: {generated}</span>

      {source && (
        <span>
          Source: {source}
          {page ? ` • Page ${page}` : ""}
        </span>
      )}
    </div>
  );
}