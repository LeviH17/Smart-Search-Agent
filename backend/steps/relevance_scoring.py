import json
import anthropic
from models import Snippet, ScoringResult, EntityResult
from prompts import RELEVANCE_SCORING_SYSTEM, RELEVANCE_SCORING_BATCH_USER

THRESHOLD = 0.80


async def run(snippets: list[Snippet], entity: EntityResult, intent: str,
              iteration: int, client: anthropic.AsyncAnthropic) -> ScoringResult:
    # Build a compact representation for each snippet
    snippets_json = json.dumps([
        {"id": s.id, "source": s.source, "author": s.author, "text": s.text}
        for s in snippets
    ], indent=2)

    user_content = RELEVANCE_SCORING_BATCH_USER.format(
        intent=intent,
        entity_name=entity.entityName,
        entity_type=entity.entityType,
        count=len(snippets),
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

    results = json.loads(raw)

    # Build lookup from id → result
    result_map = {r["id"]: r for r in results}

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
