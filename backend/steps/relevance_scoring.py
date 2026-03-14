import json
import asyncio
import anthropic
from models import Snippet, ScoringResult, EntityResult
from prompts import RELEVANCE_SCORING_SYSTEM, RELEVANCE_SCORING_USER

THRESHOLD = 0.80
BATCH_SIZE = 20  # max concurrent Haiku calls per batch


async def _score_snippet(snippet: Snippet, intent: str, entity: EntityResult,
                          client: anthropic.AsyncAnthropic) -> Snippet:
    user_content = RELEVANCE_SCORING_USER.format(
        intent=intent,
        entity_name=entity.entityName,
        entity_type=entity.entityType,
        source=snippet.source,
        author=snippet.author,
        text=snippet.text
    )

    response = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=RELEVANCE_SCORING_SYSTEM,
        messages=[{"role": "user", "content": user_content}]
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(raw)
    return snippet.model_copy(update={
        "relevance_score": float(data.get("score", 0.0)),
        "relevance_label": data.get("label", "Irrelevant"),
        "relevance_reason": data.get("reason", "")
    })


async def run(snippets: list[Snippet], entity: EntityResult, intent: str,
              iteration: int, client: anthropic.AsyncAnthropic) -> ScoringResult:
    # Score in batches to avoid rate limits
    scored_snippets: list[Snippet] = []
    for i in range(0, len(snippets), BATCH_SIZE):
        batch = snippets[i:i + BATCH_SIZE]
        tasks = [_score_snippet(s, intent, entity, client) for s in batch]
        results = await asyncio.gather(*tasks)
        scored_snippets.extend(results)

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
