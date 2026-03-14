import json
import asyncio
import anthropic
from models import Snippet, ScoringResult, EntityResult
from prompts import RELEVANCE_SCORING_SYSTEM, RELEVANCE_SCORING_BATCH_USER

THRESHOLD = 0.80
BATCH_SIZE = 50  # Two concurrent batches of 50 — each fits within 8192 output tokens


async def _score_batch(batch: list[Snippet], intent: str, entity: EntityResult,
                       client: anthropic.AsyncAnthropic) -> list[dict]:
    snippets_json = json.dumps([
        {"id": s.id, "source": s.source, "author": s.author, "text": s.text}
        for s in batch
    ], indent=2)

    user_content = RELEVANCE_SCORING_BATCH_USER.format(
        intent=intent,
        entity_name=entity.entityName,
        entity_type=entity.entityType,
        count=len(batch),
        snippets_json=snippets_json,
    )

    response = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=8192,
        system=RELEVANCE_SCORING_SYSTEM,
        messages=[{"role": "user", "content": user_content}]
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


async def run(snippets: list[Snippet], entity: EntityResult, intent: str,
              iteration: int, client: anthropic.AsyncAnthropic) -> ScoringResult:
    # Split into batches and score concurrently
    batches = [snippets[i:i + BATCH_SIZE] for i in range(0, len(snippets), BATCH_SIZE)]
    batch_results = await asyncio.gather(*[
        _score_batch(batch, intent, entity, client) for batch in batches
    ])

    # Flatten results into a lookup map
    result_map: dict[str, dict] = {}
    for results in batch_results:
        for r in results:
            result_map[r["id"]] = r

    scored_snippets: list[Snippet] = []
    for s in snippets:
        r = result_map.get(s.id, {})
        scored_snippets.append(s.model_copy(update={
            "relevance_score": float(r.get("score", 0.0)),
            "relevance_label": r.get("label", "Irrelevant"),
            "relevance_reason": r.get("reason", ""),
        }))

    relevant_count = sum(
        1 for s in scored_snippets
        if s.relevance_label in ("Relevant", "Somewhat Relevant")
    )
    total = len(scored_snippets)
    precision = relevant_count / total if total > 0 else 0.0

    return ScoringResult(
        snippets=scored_snippets,
        precision=precision,
        threshold=THRESHOLD,
        passed=precision >= THRESHOLD,
        iteration=iteration
    )
