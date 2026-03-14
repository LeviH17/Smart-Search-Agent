import json
import anthropic
from models import BooleanQueryResult, EntityResult, ScoringResult, SmartPromptResult
from prompts import SMART_PROMPT_SYSTEM, SMART_PROMPT_USER


async def run(boolean: BooleanQueryResult, entity: EntityResult,
              scoring: ScoringResult, client: anthropic.AsyncAnthropic) -> SmartPromptResult:

    user_content = SMART_PROMPT_USER.format(
        entity_name=entity.entityName,
        entity_type=entity.entityType,
        full_name=entity.fullName,
        noise_types=", ".join(entity.knownNoiseTypes) or "None identified",
        ambiguity_reasons=", ".join(entity.ambiguityReasons) or "None identified",
        query=boolean.query,
        precision=scoring.precision
    )

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SMART_PROMPT_SYSTEM,
        messages=[{"role": "user", "content": user_content}]
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(raw)
    return SmartPromptResult(**data)
