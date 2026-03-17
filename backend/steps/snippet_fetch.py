import json
import re
import asyncio
import anthropic
from json_repair import repair_json
from models import BooleanQueryResult, Snippet, EntityResult
from prompts import SNIPPET_GENERATION_SYSTEM, SNIPPET_GENERATION_USER, SNIPPET_GENERATION_FILTERED_USER

SNIPPET_COUNT = 100
BATCH_SIZE = 20        # 20 snippets × ~150 tokens ≈ 3k tokens — well within 4096
NOISE_RATIO = 0.40

VALID_SOURCES = {"twitter", "reddit", "linkedin", "news", "instagram", "forum"}


def _parse_snippets(raw: str, id_offset: int = 0) -> list[Snippet]:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```[a-z]*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
    raw = raw.strip()

    start = raw.find("[")
    end = raw.rfind("]") + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON array found in snippet generation response")

    data = json.loads(repair_json(raw[start:end]))
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
        max_tokens=4096,
        system=SNIPPET_GENERATION_SYSTEM,
        messages=[{"role": "user", "content": user_content}]
    )
    return _parse_snippets(response.content[0].text, id_offset=id_offset)


async def run(boolean: BooleanQueryResult, entity: EntityResult,
              client: anthropic.AsyncAnthropic) -> list[Snippet]:
    """Generate 100 snippets across 5 concurrent batches of 20."""
    noise_per_batch = max(1, int(BATCH_SIZE * NOISE_RATIO))
    num_batches = SNIPPET_COUNT // BATCH_SIZE

    def make_prompt() -> str:
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

    # Sequential to stay within Haiku's 10k tokens/min rate limit
    batches = []
    for i in range(num_batches):
        batches.append(await _fetch_batch(make_prompt(), id_offset=i * BATCH_SIZE, client=client))
    return [s for batch in batches for s in batch]


async def run_filtered(boolean: BooleanQueryResult, entity: EntityResult,
                       smart_prompt: str, client: anthropic.AsyncAnthropic) -> list[Snippet]:
    """Generate 100 filtered snippets across 5 sequential batches of 20."""
    num_batches = SNIPPET_COUNT // BATCH_SIZE

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

    batches = []
    for i in range(num_batches):
        batches.append(await _fetch_batch(make_prompt(), id_offset=i * BATCH_SIZE, client=client))
    return [s for batch in batches for s in batch]
