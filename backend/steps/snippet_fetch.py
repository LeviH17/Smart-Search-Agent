import json
import re
import anthropic
from models import BooleanQueryResult, Snippet, EntityResult
from prompts import SNIPPET_GENERATION_SYSTEM, SNIPPET_GENERATION_USER, SNIPPET_GENERATION_FILTERED_USER

SNIPPET_COUNT = 100


def _parse_snippets(raw: str) -> list[Snippet]:
    """Extract JSON array from Claude response and parse into Snippet objects."""
    # Strip markdown code fences if present
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```[a-z]*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
    raw = raw.strip()

    data = json.loads(raw)
    snippets = []
    for i, item in enumerate(data):
        # Ensure unique IDs
        item["id"] = item.get("id") or f"snip_{i+1:03d}"
        # Null out scoring fields — they get populated by relevance_scoring step
        item["relevance_score"] = None
        item["relevance_label"] = None
        item["relevance_reason"] = None
        snippets.append(Snippet(**item))
    return snippets


async def run(boolean: BooleanQueryResult, entity: EntityResult,
              client: anthropic.AsyncAnthropic) -> list[Snippet]:
    """Generate mock snippets via Claude based on the entity and boolean query."""
    user_content = SNIPPET_GENERATION_USER.format(
        count=SNIPPET_COUNT,
        entity_name=entity.entityName,
        full_name=entity.fullName,
        entity_type=entity.entityType,
        industry=entity.industryVertical,
        handles=", ".join(entity.handles) or "None",
        noise_types=", ".join(entity.knownNoiseTypes) or "None",
        ambiguity_reasons=", ".join(entity.ambiguityReasons) or "None",
        boolean_query=boolean.query,
    )

    response = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=16000,
        system=SNIPPET_GENERATION_SYSTEM,
        messages=[{"role": "user", "content": user_content}]
    )

    return _parse_snippets(response.content[0].text)


async def run_filtered(boolean: BooleanQueryResult, entity: EntityResult,
                       smart_prompt: str, client: anthropic.AsyncAnthropic) -> list[Snippet]:
    """Generate filtered mock snippets — high relevance, noise removed."""
    user_content = SNIPPET_GENERATION_FILTERED_USER.format(
        count=SNIPPET_COUNT,
        entity_name=entity.entityName,
        full_name=entity.fullName,
        entity_type=entity.entityType,
        industry=entity.industryVertical,
        boolean_query=boolean.query,
        smart_prompt=smart_prompt,
    )

    response = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=16000,
        system=SNIPPET_GENERATION_SYSTEM,
        messages=[{"role": "user", "content": user_content}]
    )

    return _parse_snippets(response.content[0].text)
