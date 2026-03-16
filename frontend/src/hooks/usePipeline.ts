import { useState, useRef, useCallback } from "react";
import type {
  PipelineState,
  PipelineStatus,
  StepState,
  ChatMessage,
  StepResultData,
  EntityResult,
  BooleanQueryResult,
} from "../types";

function makeId() {
  return Math.random().toString(36).slice(2);
}

const INITIAL_PIPELINE: PipelineState = {
  status: "idle",
  steps: [],
  pipelineDone: null,
};

export function usePipeline() {
  const [pipeline, setPipeline] = useState<PipelineState>(INITIAL_PIPELINE);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const historyRef = useRef<{ role: string; content: string }[]>([]);
  const abortRef = useRef<AbortController | null>(null);
  const pendingEntityRef = useRef<EntityResult | null>(null);
  const pendingBooleanRef = useRef<BooleanQueryResult | null>(null);
  const originalQueryRef = useRef<string>("");

  const addMessage = useCallback((role: ChatMessage["role"], content: string, suggestions?: string[]) => {
    const msg: ChatMessage = { id: makeId(), role, content, suggestions, timestamp: Date.now() };
    setMessages((prev) => [...prev, msg]);
    return msg;
  }, []);

  const upsertStep = useCallback((
    stepId: string,
    iteration: number,
    update: Partial<StepState>
  ) => {
    setPipeline((prev) => {
      const key = `${stepId}__${iteration}`;
      const existing = prev.steps.find((s) => s.stepId === key);
      if (existing) {
        return {
          ...prev,
          steps: prev.steps.map((s) => s.stepId === key ? { ...s, ...update } : s),
        };
      }
      const newStep: StepState = {
        stepId: key,
        label: update.label ?? stepId,
        description: update.description ?? "",
        status: "pending",
        result: null,
        errorMessage: null,
        iteration,
        startedAt: null,
        completedAt: null,
        ...update,
      };
      return { ...prev, steps: [...prev.steps, newStep] };
    });
  }, []);

  const processSSELine = useCallback((eventType: string, dataStr: string) => {
    let data: Record<string, unknown>;
    try {
      data = JSON.parse(dataStr);
    } catch {
      return;
    }

    const stepId = data.step_id as string;
    const iteration = (data.iteration as number) ?? 0;
    const payload = data.payload as Record<string, unknown>;

    switch (eventType) {
      case "step_start": {
        upsertStep(stepId, iteration, {
          label: payload.label as string,
          description: payload.description as string,
          status: "running",
          startedAt: Date.now(),
        });
        setPipeline((prev) => ({ ...prev, status: "running" as PipelineStatus }));
        break;
      }

      case "step_complete": {
        const resultType = payload.result_type as StepResultData["resultType"];
        const resultData = payload.data;
        upsertStep(stepId, iteration, {
          status: "done",
          completedAt: Date.now(),
          result: { resultType, data: resultData } as StepResultData,
        });
        break;
      }

      case "step_error": {
        upsertStep(stepId, iteration, {
          status: "failed",
          completedAt: Date.now(),
          errorMessage: (payload.message as string) ?? "Unknown error",
        });
        setIsLoading(false);
        break;
      }

      case "clarification_needed": {
        const question = payload.message as string;
        const suggestions = (payload.suggestions as string[]) ?? [];
        addMessage("assistant", question, suggestions);
        setPipeline((prev) => ({ ...prev, status: "clarifying" as PipelineStatus }));
        setIsLoading(false);
        break;
      }

      case "boolean_confirm_needed": {
        pendingEntityRef.current = payload.entity as EntityResult;
        pendingBooleanRef.current = payload.boolean as BooleanQueryResult;
        setPipeline((prev) => ({ ...prev, status: "awaiting_boolean" as PipelineStatus }));
        setIsLoading(false);
        break;
      }

      case "pipeline_done": {
        const success = payload.success as boolean;
        const iterations_used = payload.iterations_used as number;
        const final_precision = payload.final_precision as number;
        setPipeline((prev) => ({
          ...prev,
          status: (success ? "done" : "error") as PipelineStatus,
          pipelineDone: { success, iterations_used, final_precision },
        }));
        setIsLoading(false);
        break;
      }
    }
  }, [upsertStep, addMessage]);

  const _fireRequest = useCallback(async (body: string) => {
    abortRef.current?.abort();
    abortRef.current = new AbortController();

    let buffer = "";
    let currentEvent = "message";

    try {
      const apiBase = import.meta.env.VITE_API_URL ?? "";
      const response = await fetch(`${apiBase}/api/run-pipeline`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body,
        signal: abortRef.current.signal,
      });

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() ?? "";

        for (const line of lines) {
          if (line.startsWith("event: ")) {
            currentEvent = line.slice(7).trim();
          } else if (line.startsWith("data: ")) {
            processSSELine(currentEvent, line.slice(6));
            currentEvent = "message";
          }
        }
      }
    } catch (err: unknown) {
      if (err instanceof Error && err.name !== "AbortError") {
        setIsLoading(false);
        setPipeline((prev) => ({ ...prev, status: "error" }));
      }
    }
  }, [processSSELine]);

  const runPipeline = useCallback(async (userMessage: string) => {
    historyRef.current = [
      ...historyRef.current,
      { role: "user", content: userMessage },
    ];
    originalQueryRef.current = userMessage;

    addMessage("user", userMessage);
    setIsLoading(true);
    setPipeline((prev) => ({
      ...prev,
      status: "running",
      steps: prev.status === "idle" ? [] : prev.steps,
      pipelineDone: null,
    }));

    await _fireRequest(JSON.stringify({
      query: userMessage,
      conversation_history: historyRef.current.slice(0, -1),
    }));
  }, [addMessage, _fireRequest]);

  const confirmBoolean = useCallback(async (editedQuery: string) => {
    if (!pendingEntityRef.current || !pendingBooleanRef.current) return;

    const booleanOverride = { ...pendingBooleanRef.current, query: editedQuery };

    setIsLoading(true);
    setPipeline((prev) => ({ ...prev, status: "running" }));

    await _fireRequest(JSON.stringify({
      query: originalQueryRef.current,
      conversation_history: historyRef.current,
      entity_override: pendingEntityRef.current,
      boolean_override: booleanOverride,
    }));
  }, [_fireRequest]);

  const sendMessage = useCallback((text: string) => {
    runPipeline(text);
  }, [runPipeline]);

  const reset = useCallback(() => {
    abortRef.current?.abort();
    historyRef.current = [];
    pendingEntityRef.current = null;
    pendingBooleanRef.current = null;
    originalQueryRef.current = "";
    setPipeline(INITIAL_PIPELINE);
    setMessages([]);
    setIsLoading(false);
  }, []);

  const awaitingBoolean = pipeline.status === "awaiting_boolean";

  return { pipeline, messages, isLoading, sendMessage, confirmBoolean, awaitingBoolean, reset };
}
