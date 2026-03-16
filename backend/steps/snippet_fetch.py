import json
import re
import asyncio
import anthropic
from models import BooleanQueryResult, Snippet, EntityResult
from prompts import SNIPPET_GENERATION_SYSTEM, SNIPPET_GENERATION_USER, SNIPPET_GENERATION_FILTERED_USER

SNIPPET_COUNT = 100
BATCH_SIZE = 50        # Each batch fits safely within 16k output tokens
NOISE_RATIO = 0.40     # 40% noise in initial fetch

VALID_SOURCES = {"twitter", "reddit", "linkedin", "news", "instagram", "forum"}


def _parse_snippets(raw: str, id_offset: int = 0) -> list[Snippet]:
    """Extract JSON array from Claude response and parse into Snippet objects."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```[a-z]*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
    raw = raw.strip()

    start = raw.find("[")
    end = raw.rfind("]") + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON array found in snippet generation response")
    data = json.loads(raw[start:end])

    snippets = []
    for i, item in enumerate(data):
        item["id"] = f"snip_{id_offset + i + 1:03d}"
        if item.get("source") not in VALID_SOURCES:
            item["source"] = "forum"
        item["relevance_score"] = None
        item["relevance_label"] = None
        item["relevance_reason"] = None
        snippets.append(Snippet(**item))
    return snippets


async def _fetch_batch(user_content: str, id_offset: int,
                       client: anthropic.AsyncAnthropic) -> list[Snippet]:
    response = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=8192,
        system=SNIPPET_GENERATION_SYSTEM,
        messages=[{"role": "user", "content": user_content}]
    )
    return _parse_snippets(response.content[0].text, id_offset=id_offset)


async def run(boolean: BooleanQueryResult, entity: EntityResult,
              client: anthropic.AsyncAnthropic) -> list[Snippet]:
    """Generate mock snippets in two concurrent batches of 50."""
    noise_per_batch = int(BATCH_SIZE * NOISE_RATIO)

    def make_prompt(batch_num: int) -> str:
        return SNIPPET_GENERATION_USER.format(
            count=BATCH_SIZE,
            noise_count=noise_per_batch,
            entity_name=entity.entityName,
            full_name=entity.fullName,
            entity_type=entity.entityType,
            industry=entity.industryVertical,
            handles=", ".join(entity.handles) or "None",
            noise_types=", ".join(entity.knownNoiseTypes) or "None",
            ambiguity_reasons=", ".join(entity.ambiguityReasons) or "None",
            boolean_query=boolean.query,
        )

    batch1, batch2 = await asyncio.gather(
        _fetch_batch(make_prompt(1), id_offset=0, client=client),
        _fetch_batch(make_prompt(2), id_offset=BATCH_SIZE, client=client),
    )
    return batch1 + batch2


async def run_filtered(boolean: BooleanQueryResult, entity: EntityResult,
                       smart_prompt: str, client: anthropic.AsyncAnthropic) -> list[Snippet]:
    """Generate filtered snippets in two concurrent batches of 50."""
    def make_prompt() -> str:
        return SNIPPET_GENERATION_FILTERED_USER.format(
            count=BATCH_SIZE,
            entity_name=entity.entityName,
            full_name=entity.fullName,
            entity_type=entity.entityType,
            industry=entity.industryVertical,
            boolean_query=boolean.query,
            smart_prompt=smart_prompt,
        )

    batch1, batch2 = await asyncio.gather(
        _fetch_batch(make_prompt(), id_offset=0, client=client),
        _fetch_batch(make_prompt(), id_offset=BATCH_SIZE, client=client),
    )
    return batch1 + batch2
