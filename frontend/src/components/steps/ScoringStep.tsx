import type { ScoringResult } from "../../types";

export function ScoringStep({ data }: { data: ScoringResult }) {
  const pct = Math.round(data.precision * 100);
  const thresholdPct = Math.round(data.threshold * 100);
  const relevant = data.snippets.filter((s) => s.relevance_label === "Relevant").length;
  const somewhat = data.snippets.filter((s) => s.relevance_label === "Somewhat Relevant").length;
  const irrelevant = data.snippets.filter((s) => s.relevance_label === "Irrelevant").length;

  return (
    <div className="space-y-4">
      {/* Pass/fail badge */}
      <div className="flex items-center gap-3">
        <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-semibold ${data.passed ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}>
          <span>{data.passed ? "✓" : "✗"}</span>
          <span>{data.passed ? "Threshold met" : "Below threshold"}</span>
        </div>
        <span className="text-sm text-gray-500">
          <span className="font-bold text-gray-800">{pct}%</span> precision · target {thresholdPct}%
        </span>
      </div>

      {/* Precision bar with threshold marker */}
      <div>
        <div className="relative w-full h-3 bg-gray-100 rounded-full overflow-visible">
          <div
            className={`h-full rounded-full transition-all ${data.passed ? "bg-green-500" : "bg-red-400"}`}
            style={{ width: `${pct}%` }}
          />
          {/* Threshold marker */}
          <div
            className="absolute top-0 h-full flex flex-col items-center"
            style={{ left: `${thresholdPct}%`, transform: "translateX(-50%)" }}
          >
            <div className="w-0.5 h-full bg-gray-500 opacity-60" />
          </div>
        </div>
        <div className="relative mt-1" style={{ paddingLeft: `${thresholdPct}%` }}>
          <span className="text-xs text-gray-400" style={{ transform: "translateX(-50%)", display: "inline-block" }}>
            {thresholdPct}% target
          </span>
        </div>
      </div>

      {/* Breakdown */}
      <div className="grid grid-cols-3 gap-3">
        <div className="bg-green-50 rounded-lg p-2.5 text-center">
          <div className="text-xl font-bold text-green-700">{relevant}</div>
          <div className="text-xs text-green-600">Relevant</div>
        </div>
        <div className="bg-amber-50 rounded-lg p-2.5 text-center">
          <div className="text-xl font-bold text-amber-700">{somewhat}</div>
          <div className="text-xs text-amber-600">Somewhat Relevant</div>
        </div>
        <div className="bg-red-50 rounded-lg p-2.5 text-center">
          <div className="text-xl font-bold text-red-700">{irrelevant}</div>
          <div className="text-xs text-red-600">Irrelevant</div>
        </div>
      </div>

      {!data.passed && (
        <p className="text-xs text-gray-500 italic">
          Precision is below the 80% threshold — broadening the query and applying a Smart Search filter.
        </p>
      )}
    </div>
  );
}
