import json
from json_repair import repair_json
import anthropic
from models import PipelineRequest, EntityResult
from prompts import ENTITY_EXTRACTION_SYSTEM, ENTITY_EXTRACTION_USER


async def run(request: PipelineRequest, client: anthropic.AsyncAnthropic) -> EntityResult:
    context = ""
    for msg in request.conversation_history:
        if msg.get("role") == "user":
            context += msg.get("content", "") + " "

    user_content = ENTITY_EXTRACTION_USER.format(
        query=request.query,
        context=context.strip() or "None"
    )

    response = await client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=ENTITY_EXTRACTION_SYSTEM,
        messages=[{"role": "user", "content": user_content}]
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(repair_json(raw))
    return EntityResult(**data)
