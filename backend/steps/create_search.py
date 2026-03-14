import uuid
from datetime import datetime, timezone
from models import BooleanQueryResult, ScoringResult, CreateSearchResult
from typing import Optional


def run(boolean: BooleanQueryResult, scoring: ScoringResult,
        iterations_used: int, smart_prompt: Optional[str] = None) -> CreateSearchResult:
    return CreateSearchResult(
        search_id=str(uuid.uuid4()),
        label=f"Search #{str(uuid.uuid4())[:8].upper()}",
        query_used=boolean.query,
        smart_prompt_used=smart_prompt,
        precision_achieved=scoring.precision,
        iterations_used=iterations_used,
        created_at=datetime.now(timezone.utc).isoformat()
    )
