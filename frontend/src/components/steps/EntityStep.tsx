import type { EntityResult } from "../../types";

const AMBIGUITY_COLORS: Record<string, string> = {
  "Very Low": "bg-green-500",
  Low: "bg-green-400",
  Medium: "bg-amber-400",
  High: "bg-orange-500",
  "Very High": "bg-red-500",
};

const AMBIGUITY_TEXT: Record<string, string> = {
  "Very Low": "text-green-700",
  Low: "text-green-600",
  Medium: "text-amber-700",
  High: "text-orange-700",
  "Very High": "text-red-700",
};

export function EntityStep({ data }: { data: EntityResult }) {
  const barWidth = `${Math.round(data.ambiguityScore * 100)}%`;
  const barColor = AMBIGUITY_COLORS[data.ambiguityLabel] ?? "bg-gray-400";
  const labelColor = AMBIGUITY_TEXT[data.ambiguityLabel] ?? "text-gray-700";

  return (
    <div className="space-y-4">
      {/* Top row: name + type */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <div className="text-xs text-gray-400 uppercase tracking-wide mb-1">Full Name</div>
          <div className="text-sm font-semibold text-gray-900">{data.fullName}</div>
        </div>
        <div>
          <div className="text-xs text-gray-400 uppercase tracking-wide mb-1">Type</div>
          <span className="inline-block text-xs font-medium px-2.5 py-1 rounded-full bg-blue-100 text-blue-700">
            {data.entityType}
          </span>
        </div>
      </div>

      {/* Ticker + Industry */}
      <div className="grid grid-cols-2 gap-4">
        {data.ticker && (
          <div>
            <div className="text-xs text-gray-400 uppercase tracking-wide mb-1">Ticker</div>
            <span className="inline-block text-xs font-mono font-bold px-2.5 py-1 rounded bg-gray-100 text-gray-800">
              {data.ticker}
            </span>
          </div>
        )}
        <div className={data.ticker ? "" : "col-span-2"}>
          <div className="text-xs text-gray-400 uppercase tracking-wide mb-1">Industry</div>
          <div className="text-sm text-gray-700">{data.industryVertical}</div>
        </div>
      </div>

      {/* Handles + Aliases */}
      {(data.handles.length > 0 || data.aliases.length > 0) && (
        <div className="grid grid-cols-2 gap-4">
          {data.handles.length > 0 && (
            <div>
              <div className="text-xs text-gray-400 uppercase tracking-wide mb-1">Handles / Aliases</div>
              <div className="flex flex-wrap gap-1.5">
                {data.handles.map((h) => (
                  <span key={h} className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-mono">
                    {h}
                  </span>
                ))}
                {data.aliases.map((a) => (
                  <span key={a} className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                    {a}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Business Units */}
      {data.businessUnits.length > 0 && (
        <div>
          <div className="text-xs text-gray-400 uppercase tracking-wide mb-1">Business Units</div>
          <div className="flex flex-wrap gap-1.5">
            {data.businessUnits.map((u) => (
              <span key={u} className="text-xs px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100">
                {u}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Ambiguity Score */}
      <div>
        <div className="flex items-center justify-between mb-1.5">
          <div className="text-xs text-gray-400 uppercase tracking-wide">Ambiguity Score</div>
          <span className={`text-xs font-semibold ${labelColor}`}>{data.ambiguityLabel}</span>
        </div>
        <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
          <div className={`h-full rounded-full transition-all ${barColor}`} style={{ width: barWidth }} />
        </div>
        <div className="text-xs text-gray-400 mt-1">{Math.round(data.ambiguityScore * 100)}%</div>
        {data.ambiguityReasons.length > 0 && (
          <ul className="mt-2 space-y-0.5">
            {data.ambiguityReasons.map((r, i) => (
              <li key={i} className="text-xs text-gray-500 flex items-start gap-1.5">
                <span className="mt-0.5 text-gray-300">↳</span>{r}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Known Noise Risks */}
      {data.knownNoiseTypes.length > 0 && (
        <div>
          <div className="text-xs text-gray-400 uppercase tracking-wide mb-1.5">Known Noise Risks</div>
          <div className="space-y-1">
            {data.knownNoiseTypes.map((n, i) => (
              <div key={i} className="flex items-center gap-2 text-xs text-red-600">
                <span>⚠</span>
                <span>{n}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
