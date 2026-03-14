import asyncio
import json
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from models import PipelineRequest
from pipeline import run_pipeline

load_dotenv()

app = FastAPI(title="Smart Search Agent")

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:4173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/run-pipeline")
async def run_pipeline_endpoint(request: PipelineRequest):
    queue: asyncio.Queue = asyncio.Queue()

    async def emit(event_type: str, step_id: str, payload: dict, iteration: int = 0):
        await queue.put({
            "event": event_type,
            "step_id": step_id,
            "iteration": iteration,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        })

    async def pipeline_task():
        try:
            await run_pipeline(request, emit)
        except Exception as e:
            await emit("step_error", "pipeline", {"message": str(e), "recoverable": False}, 0)
        finally:
            await queue.put(None)  # sentinel

    async def event_stream():
        task = asyncio.create_task(pipeline_task())
        try:
            while True:
                item = await queue.get()
                if item is None:
                    break
                yield f"event: {item['event']}\ndata: {json.dumps(item)}\n\n"
        finally:
            task.cancel()

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@app.get("/api/health")
async def health():
    return {"status": "ok"}


# Serve built frontend in production
frontend_dist = os.getenv("FRONTEND_DIST") or os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.isdir(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")
