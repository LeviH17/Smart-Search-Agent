import json
import anthropic
from models import BooleanQueryResult, ScoringResult, EntityResult
from prompts import BOOLEAN_BROADENING_SYSTEM, BOOLEAN_BROADENING_USER


async def run(current_boolean: BooleanQueryResult, scoring: ScoringResult,
              entity: EntityResult, iteration: int,
              client: anthropic.AsyncAnthropic) -> BooleanQueryResult:

    noise_snippets = [s for s in scoring.snippets if s.relevance_label == "Irrelevant"]
    relevant_snippets = [s for s in scoring.snippets if s.relevance_label == "Relevant"]

    noise_examples = "\n".join(
        f'- "{s.text[:120]}..." (reason: {s.relevance_reason})'
        for s in noise_snippets[:3]
    ) or "None"

    relevant_examples = "\n".join(
        f'- "{s.text[:120]}..."'
        for s in relevant_snippets[:3]
    ) or "None"

    somewhat_relevant = sum(1 for s in scoring.snippets if s.relevance_label == "Somewhat Relevant")

    user_content = BOOLEAN_BROADENING_USER.format(
        original_query=current_boolean.query,
        precision=scoring.precision,
        iteration=iteration + 1,
        entity_name=entity.entityName,
        entity_type=entity.entityType,
        total=len(scoring.snippets),
        relevant=sum(1 for s in scoring.snippets if s.relevance_label == "Relevant"),
        somewhat_relevant=somewhat_relevant,
        irrelevant=len(noise_snippets),
        noise_examples=noise_examples,
        relevant_examples=relevant_examples
    )

    response = await client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=BOOLEAN_BROADENING_SYSTEM,
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
