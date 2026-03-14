from models import BooleanQueryResult, Snippet, EntityResult
from mock_data import get_snippets_for_query, get_filtered_snippets


async def run(boolean: BooleanQueryResult, entity: EntityResult) -> list[Snippet]:
    """Fetch mock snippets matching the boolean query."""
    return get_snippets_for_query(entity.entityName, count=10)


async def run_filtered(boolean: BooleanQueryResult, entity: EntityResult, smart_prompt: str) -> list[Snippet]:
    """Fetch mock snippets with smart prompt filter applied."""
    return get_filtered_snippets(entity.entityName, smart_prompt, count=10)
