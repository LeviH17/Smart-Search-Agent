import json
import anthropic
from models import EntityResult, BooleanQueryResult
from prompts import BOOLEAN_QUERY_SYSTEM, BOOLEAN_QUERY_USER


async def run(entity: EntityResult, query: str, client: anthropic.AsyncAnthropic) -> BooleanQueryResult:
    entity_json = entity.model_dump_json(indent=2)

    user_content = BOOLEAN_QUERY_USER.format(
        entity_json=entity_json,
        query=query
    )

    response = await client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=BOOLEAN_QUERY_SYSTEM,
        messages=[{"role": "user", "content": user_content}]
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(raw)
    return BooleanQueryResult(**data)
