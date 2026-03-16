import json
import anthropic
from models import BooleanQueryResult, ScoringResult, EntityResult
from prompts import BOOLEAN_BROADENING_SYSTEM


async def run(current_boolean: BooleanQueryResult, scoring: ScoringResult,
              entity: EntityResult, iteration: int,
              client: anthropic.AsyncAnthropic) -> BooleanQueryResult:

    noise_snippets = [s for s in scoring.snippets if s.relevance_label == "Irrelevant"]
    relevant_snippets = [s for s in scoring.snippets if s.relevance_label == "Relevant"]
    somewhat_relevant = sum(1 for s in scoring.snippets if s.relevance_label == "Somewhat Relevant")

    noise_examples = "\n".join(
        f'- "{s.text[:150]}..." (reason: {s.relevance_reason})'
        for s in noise_snippets[:10]
    ) or "None"

    relevant_examples = "\n".join(
        f'- "{s.text[:150]}..."'
        for s in relevant_snippets[:10]
    ) or "None"

    # Build prompt as an f-string to avoid .format() choking on braces in snippet text
    precision_pct = f"{scoring.precision:.0%}"
    user_content = (
        f'Original query: "{current_boolean.query}"\n'
        f"Current precision: {precision_pct} (target: 80%)\n"
        f"Iteration: {iteration + 1}\n"
        f"\n"
        f"Entity: {entity.entityName} ({entity.entityType})\n"
        f"\n"
        f"Scoring breakdown:\n"
        f"- Total snippets scored: {len(scoring.snippets)}\n"
        f"- Relevant: {sum(1 for s in scoring.snippets if s.relevance_label == 'Relevant')}\n"
        f"- Somewhat Relevant: {somewhat_relevant}\n"
        f"- Irrelevant: {len(noise_snippets)}\n"
        f"\n"
        f"Examples of IRRELEVANT snippets that slipped through:\n"
        f"{noise_examples}\n"
        f"\n"
        f"Examples of RELEVANT snippets that were correctly captured:\n"
        f"{relevant_examples}\n"
        f"\n"
        f"Improve the query to increase precision. Return JSON only."
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
