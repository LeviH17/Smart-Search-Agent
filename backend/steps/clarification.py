import json
from json_repair import repair_json
import anthropic
from models import PipelineRequest
from prompts import INTENT_CHECK_SYSTEM, INTENT_CHECK_USER


async def check(request: PipelineRequest, client: anthropic.AsyncAnthropic) -> tuple[bool, str, list[str]]:
    """
    Returns (needs_clarification, question, suggestions).
    If needs_clarification is False, question is empty string.
    """
    history_str = ""
    for msg in request.conversation_history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        history_str += f"{role}: {content}\n"

    user_content = INTENT_CHECK_USER.format(
        query=request.query,
        history=history_str or "None"
    )

    response = await client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        system=INTENT_CHECK_SYSTEM,
        messages=[{"role": "user", "content": user_content}]
    )

    raw = response.content[0].text.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(repair_json(raw))
    sufficient = data.get("sufficient", True)
    question = data.get("question") or ""
    suggestions = data.get("suggestions") or []

    return (not sufficient), question, suggestions
