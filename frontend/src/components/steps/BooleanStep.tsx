import { useState } from "react";
import type { BooleanQueryResult } from "../../types";

interface Props {
  data: BooleanQueryResult;
  awaitingConfirm?: boolean;
  onConfirm?: (query: string) => void;
}

export function BooleanStep({ data, awaitingConfirm, onConfirm }: Props) {
  const [editedQuery, setEditedQuery] = useState(data.query);

  return (
    <div className="space-y-3">
      {/* Query */}
      <div>
        <div className="text-xs text-gray-400 uppercase tracking-wide mb-1.5">OpenSearch Boolean Query</div>
        {awaitingConfirm ? (
          <textarea
            className="w-full bg-gray-950 rounded-lg p-3 font-mono text-xs text-green-400 leading-relaxed resize-y min-h-[80px] border border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-400"
            value={editedQuery}
            onChange={(e) => setEditedQuery(e.target.value)}
            spellCheck={false}
          />
        ) : (
          <div className="bg-gray-950 rounded-lg p-3 font-mono text-xs text-green-400 leading-relaxed overflow-x-auto whitespace-pre-wrap break-all">
            {data.query}
          </div>
        )}
      </div>

      {/* Explanation */}
      <p className="text-xs text-gray-500 italic">{data.explanation}</p>

      {/* Term breakdown */}
      <div className="grid grid-cols-3 gap-2">
        {data.must_terms.length > 0 && (
          <div>
            <div className="text-xs font-medium text-gray-500 mb-1">MUST include</div>
            <div className="space-y-1">
              {data.must_terms.map((t) => (
                <span key={t} className="block text-xs px-2 py-0.5 rounded bg-green-50 text-green-700 border border-green-100 font-mono truncate">
                  {t}
                </span>
              ))}
            </div>
          </div>
        )}
        {data.should_terms.length > 0 && (
          <div>
            <div className="text-xs font-medium text-gray-500 mb-1">SHOULD include</div>
            <div className="space-y-1">
              {data.should_terms.map((t) => (
                <span key={t} className="block text-xs px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-100 font-mono truncate">
                  {t}
                </span>
              ))}
            </div>
          </div>
        )}
        {data.must_not_terms.length > 0 && (
          <div>
            <div className="text-xs font-medium text-gray-500 mb-1">MUST NOT include</div>
            <div className="space-y-1">
              {data.must_not_terms.map((t) => (
                <span key={t} className="block text-xs px-2 py-0.5 rounded bg-red-50 text-red-700 border border-red-100 font-mono truncate">
                  {t}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Confirm button */}
      {awaitingConfirm && onConfirm && (
        <button
          onClick={() => onConfirm(editedQuery.trim() || data.query)}
          className="w-full mt-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
        >
          Continue with this query →
        </button>
      )}
    </div>
  );
}
