import type { CreateSearchResult } from "../../types";

export function CreateSearchStep({ data }: { data: CreateSearchResult }) {
  return (
    <div className="bg-green-50 border border-green-200 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-lg">✅</div>
        <div className="font-semibold text-green-800 text-sm">Search is live</div>
      </div>
      <div className="space-y-2 text-xs text-green-700">
        <div className="flex items-center justify-between py-1.5 border-b border-green-100">
          <span>Status</span>
          <span className="font-semibold">Collecting data</span>
        </div>
        <div className="flex items-center justify-between py-1.5 border-b border-green-100">
          <span>Precision achieved</span>
          <span className="font-semibold">{Math.round(data.precision_achieved * 100)}%</span>
        </div>
        <div className="flex items-center justify-between py-1.5 border-b border-green-100">
          <span>Smart Search filter</span>
          <span className="font-semibold flex items-center gap-1">
            {data.smart_prompt_used ? "🧠 Active" : "Not applied"}
          </span>
        </div>
        <div className="flex items-center justify-between py-1.5 border-b border-green-100">
          <span>Iterations used</span>
          <span className="font-semibold">{data.iterations_used}</span>
        </div>
        <div className="flex items-center justify-between py-1.5">
          <span>Search ID</span>
          <span className="font-mono font-semibold text-green-600">{data.search_id.slice(0, 8).toUpperCase()}</span>
        </div>
      </div>
    </div>
  );
}
