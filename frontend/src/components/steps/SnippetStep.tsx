import type { Snippet } from "../../types";

const SOURCE_ICONS: Record<string, string> = {
  twitter: "𝕏",
  reddit: "🔴",
  linkedin: "in",
  news: "📰",
  instagram: "📸",
  forum: "💬",
};

const LABEL_COLORS: Record<string, string> = {
  Relevant: "bg-green-100 text-green-700 border-green-200",
  "Somewhat Relevant": "bg-amber-100 text-amber-700 border-amber-200",
  Irrelevant: "bg-red-100 text-red-700 border-red-200",
};

function SnippetCard({ snippet }: { snippet: Snippet }) {
  const icon = SOURCE_ICONS[snippet.source] ?? "📄";
  const hasScore = snippet.relevance_score !== null;
  const labelClass = snippet.relevance_label ? LABEL_COLORS[snippet.relevance_label] : "";

  return (
    <div className={`bg-white border rounded-xl p-3.5 flex-shrink-0 w-72 ${hasScore && snippet.relevance_label === "Irrelevant" ? "opacity-50" : ""}`}>
      <div className="flex items-center gap-2 mb-2">
        <span className="text-sm w-5 text-center">{icon}</span>
        <span className="text-xs font-medium text-gray-500 capitalize">{snippet.source}</span>
        <span className="text-xs text-gray-400">·</span>
        <span className="text-xs text-gray-400 truncate">{snippet.handle}</span>
        {hasScore && snippet.relevance_label && (
          <span className={`ml-auto text-xs px-2 py-0.5 rounded-full border font-medium ${labelClass}`}>
            {snippet.relevance_label}
          </span>
        )}
      </div>
      <p className="text-xs text-gray-700 leading-relaxed line-clamp-3 mb-2">{snippet.text}</p>
      {snippet.relevance_reason && (
        <p className="text-xs text-gray-400 italic line-clamp-1">{snippet.relevance_reason}</p>
      )}
      <div className="flex items-center justify-between mt-2">
        <span className="text-xs text-gray-300">{snippet.published_at.slice(0, 10)}</span>
        {hasScore && (
          <div className="flex items-center gap-1">
            <div className="w-12 h-1.5 bg-gray-100 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full ${(snippet.relevance_score ?? 0) >= 0.8 ? "bg-green-500" : (snippet.relevance_score ?? 0) >= 0.5 ? "bg-amber-400" : "bg-red-400"}`}
                style={{ width: `${Math.round((snippet.relevance_score ?? 0) * 100)}%` }}
              />
            </div>
            <span className="text-xs text-gray-400">{Math.round((snippet.relevance_score ?? 0) * 100)}%</span>
          </div>
        )}
      </div>
    </div>
  );
}

export function SnippetStep({ data }: { data: Snippet[] }) {
  return (
    <div>
      <div className="text-xs text-gray-400 mb-2">{data.length} result{data.length !== 1 ? "s" : ""} fetched</div>
      <div className="flex gap-3 overflow-x-auto pb-2">
        {data.map((s) => (
          <SnippetCard key={s.id} snippet={s} />
        ))}
      </div>
    </div>
  );
}
