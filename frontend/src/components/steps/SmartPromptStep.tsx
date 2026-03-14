import type { SmartPromptResult } from "../../types";

export function SmartPromptStep({ data }: { data: SmartPromptResult }) {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <span className="text-base">🧠</span>
        <span className="text-xs font-semibold text-blue-800">Smart Search Filter</span>
        <span className="text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full font-medium">Active</span>
      </div>
      <div className="bg-blue-50 border border-blue-100 rounded-lg p-3">
        <p className="text-sm text-blue-900 leading-relaxed italic">{data.prompt}</p>
      </div>
      <p className="text-xs text-gray-400">{data.rationale}</p>
    </div>
  );
}
