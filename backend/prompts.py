INTENT_CHECK_SYSTEM = """You are an expert at understanding search intent for a social media listening platform.
Your job is to decide whether a user's query contains enough information to build a targeted search.

Evaluate if the query clearly identifies:
1. What entity or topic they want to track (company, person, product, theme, event)
2. Enough context to distinguish it from other things with the same name (if ambiguous)

Return ONLY valid JSON in this exact format:
{
  "sufficient": true | false,
  "question": "string or null",
  "suggestions": ["string", ...]
}

If sufficient is true, question and suggestions should be null/[].
If sufficient is false, question should be a single friendly clarifying question, and suggestions should be 2-4 short answer options.
"""

INTENT_CHECK_USER = """User query: "{query}"

Conversation so far:
{history}

Is this query sufficient to infer search intent? Return JSON."""


ENTITY_EXTRACTION_SYSTEM = """You are an expert entity analyst for a social media intelligence platform.
Given a user's search query, extract structured entity information.

Return ONLY valid JSON matching this exact schema:
{
  "entityName": "short canonical name",
  "fullName": "full official name",
  "entityType": "Company" | "Person" | "Product" | "Theme" | "Event" | "Risk Signal",
  "ticker": "STOCK_TICKER or null",
  "handles": ["@handle1", "@handle2"],
  "aliases": ["alias1", "alias2"],
  "businessUnits": ["unit1", "unit2"],
  "industryVertical": "industry description",
  "ambiguityScore": 0.0,
  "ambiguityLabel": "Very Low" | "Low" | "Medium" | "High" | "Very High",
  "ambiguityReasons": ["reason1", "reason2"],
  "knownNoiseTypes": ["noise category 1", "noise category 2"]
}

ambiguityScore rules:
- 0.0–0.2: Very Low (unique brand/name, minimal confusion)
- 0.2–0.4: Low (minor disambiguation needed)
- 0.4–0.6: Medium (multiple meanings, manageable)
- 0.6–0.8: High (common word, significant noise expected)
- 0.8–1.0: Very High (extremely common term, very hard to isolate)

knownNoiseTypes: predict specific categories of irrelevant content that will appear in results.
Be specific and realistic about what a keyword search would accidentally capture.
"""

ENTITY_EXTRACTION_USER = """Search query: "{query}"
Additional context from conversation: {context}

Extract entity information. Return JSON only."""


BOOLEAN_QUERY_SYSTEM = """You are an expert at writing OpenSearch boolean queries for social media monitoring.
Given entity information, craft an optimal boolean search query.

OpenSearch boolean syntax rules:
- AND: space between terms or explicit AND
- OR: OR between terms
- NOT: NOT before term or - prefix
- Phrase: "quoted phrase"
- Grouping: (term1 OR term2)
- Wildcards: term* for prefix matching

Return ONLY valid JSON:
{
  "query": "the full OpenSearch boolean query string",
  "explanation": "one sentence explaining the query strategy",
  "must_terms": ["term1", "term2"],
  "should_terms": ["term1", "term2"],
  "must_not_terms": ["term1", "term2"]
}

Guidelines:
- Include the entity name and its key aliases/handles
- Add must_not terms for obvious noise categories identified in the entity analysis
- Use should_terms for related terms that would be useful but aren't required
- Keep the query focused — precision over recall at this stage
"""

BOOLEAN_QUERY_USER = """Entity information:
{entity_json}

Original user query: "{query}"

Craft an OpenSearch boolean query. Return JSON only."""


RELEVANCE_SCORING_SYSTEM = """You are scoring social media snippets for relevance to a search intent.
Be precise and critical — only mark content as Relevant if it clearly matches the user's intent.

Return ONLY valid JSON:
{
  "score": 0.0,
  "label": "Relevant" | "Somewhat Relevant" | "Irrelevant",
  "reason": "one sentence explanation"
}

Scoring guide:
- Relevant (0.8–1.0): Directly about the target entity/topic, clearly matches intent
- Somewhat Relevant (0.4–0.79): Tangentially related, mentions entity but not the main focus
- Irrelevant (0.0–0.39): About something else that shares a name/keyword, or spam/noise
"""

RELEVANCE_SCORING_USER = """Search intent: "{intent}"
Entity being tracked: "{entity_name}" ({entity_type})

Snippet to score:
Source: {source}
Author: {author}
Text: "{text}"

Score this snippet for relevance. Return JSON only."""


BOOLEAN_BROADENING_SYSTEM = """You are an expert at iteratively improving OpenSearch boolean queries for social media monitoring.
You have been given a query that didn't achieve the required precision threshold.

Analyze the scoring results to understand what went wrong, then produce an improved query that:
1. Broadens recall by adding more aliases, related terms, or variant spellings
2. Improves precision by adding NOT terms for confirmed noise patterns
3. Adjusts phrasing to better capture the intended content

Return ONLY valid JSON:
{
  "query": "improved OpenSearch boolean query",
  "explanation": "what changed and why",
  "must_terms": ["term1"],
  "should_terms": ["term1"],
  "must_not_terms": ["term1"]
}
"""

BOOLEAN_BROADENING_USER = """Original query: "{original_query}"
Current precision: {precision:.0%} (target: 80%)
Iteration: {iteration}

Entity: {entity_name} ({entity_type})

Scoring breakdown:
- Total snippets scored: {total}
- Relevant: {relevant}
- Somewhat Relevant: {somewhat_relevant}
- Irrelevant: {irrelevant}

Examples of IRRELEVANT snippets that slipped through:
{noise_examples}

Examples of RELEVANT snippets that were correctly captured:
{relevant_examples}

Improve the query to increase precision. Return JSON only."""


SMART_PROMPT_SYSTEM = """You are an expert at writing natural language filters for AI-powered content filtering.
Your filter will be used by an AI system to decide whether each incoming social media post matches
the user's search intent. Write it as a clear, comprehensive instruction.

Return ONLY valid JSON:
{
  "prompt": "the natural language filter instruction",
  "rationale": "one sentence explaining the filter strategy"
}

The prompt should:
- Clearly describe what SHOULD be included (with specific examples)
- Clearly describe what should be EXCLUDED (with specific examples)
- Be written as an instruction to an AI classifier
- Cover the key ambiguity cases identified in the entity analysis
"""

SMART_PROMPT_USER = """Entity: {entity_name} ({entity_type})
Full name: {full_name}
Known noise types: {noise_types}
Ambiguity reasons: {ambiguity_reasons}

Current boolean query: "{query}"
Current precision: {precision:.0%}

Write a natural language Smart Search filter. Return JSON only."""
