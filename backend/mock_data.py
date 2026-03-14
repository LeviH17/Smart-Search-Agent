from models import Snippet

# Mock snippets tagged by topic for internal filtering
# Each snippet has a `_topics` field used by snippet_fetch.py (not exposed externally)

MOCK_SNIPPETS: list[dict] = [
    # --- Apple Inc. ---
    {
        "snippet": Snippet(
            id="snip_001", source="twitter", author="CNBC Markets", handle="@CNBCMarkets",
            text="$AAPL just crossed $3.5T market cap again. Tim Cook says Vision Pro pipeline is stronger than ever. #Apple #AAPL",
            published_at="2026-03-12T14:30:00Z", url="https://twitter.com/CNBCMarkets/status/fake001"
        ),
        "topics": ["apple_inc", "tech_general"]
    },
    {
        "snippet": Snippet(
            id="snip_002", source="reddit", author="u/investorwatcher", handle="u/investorwatcher",
            text="Apple's Q1 earnings blew past estimates again. Services revenue hit $26B. The app store is basically a money printer at this point.",
            published_at="2026-03-11T09:15:00Z", url="https://reddit.com/r/stocks/fake002"
        ),
        "topics": ["apple_inc"]
    },
    {
        "snippet": Snippet(
            id="snip_003", source="news", author="The Verge", handle="@verge",
            text="Apple's new M4 MacBook Pro is here and it's absolutely destroying benchmarks. Final Cut Pro render times cut by 40%.",
            published_at="2026-03-10T18:00:00Z", url="https://theverge.com/fake003"
        ),
        "topics": ["apple_inc"]
    },
    {
        "snippet": Snippet(
            id="snip_004", source="twitter", author="Ming-Chi Kuo", handle="@mingchikuo",
            text="My sources indicate Apple iPhone 17 production ramp is ahead of schedule. Expect record shipments in H2 2026. #Apple #iPhone17",
            published_at="2026-03-09T11:00:00Z", url="https://twitter.com/mingchikuo/fake004"
        ),
        "topics": ["apple_inc"]
    },
    {
        "snippet": Snippet(
            id="snip_005", source="reddit", author="u/appledeveloper99", handle="u/appledeveloper99",
            text="Apple's App Store guidelines update is killing indie developers. 30% cut is just too high when Google Play is offering 15% for most apps.",
            published_at="2026-03-08T16:45:00Z", url="https://reddit.com/r/apple/fake005"
        ),
        "topics": ["apple_inc"]
    },
    {
        "snippet": Snippet(
            id="snip_006", source="linkedin", author="Horace Dediu", handle="Horace Dediu",
            text="Apple's installed base has now exceeded 2.3 billion active devices. The loyalty rate among iPhone users remains the highest in consumer electronics at ~92%.",
            published_at="2026-03-07T10:00:00Z", url="https://linkedin.com/fake006"
        ),
        "topics": ["apple_inc"]
    },
    # --- Apple fruit / noise ---
    {
        "snippet": Snippet(
            id="snip_007", source="instagram", author="RecipeWorld", handle="@recipeworld",
            text="🍎 My grandmother's apple pie recipe is finally online! Brown sugar, cinnamon, and Granny Smith apples. So good. Link in bio!",
            published_at="2026-03-12T08:00:00Z", url="https://instagram.com/fake007"
        ),
        "topics": ["apple_fruit", "noise"]
    },
    {
        "snippet": Snippet(
            id="snip_008", source="twitter", author="OrchardLife", handle="@orchardlife",
            text="Apple harvest season is starting early this year due to warmer temps. Upstate NY orchards reporting 20% higher yields. #apple #farming",
            published_at="2026-03-11T07:30:00Z", url="https://twitter.com/orchardlife/fake008"
        ),
        "topics": ["apple_fruit", "noise"]
    },
    # --- Amazon ---
    {
        "snippet": Snippet(
            id="snip_009", source="twitter", author="@logistics_nerd", handle="@logistics_nerd",
            text="Amazon's same-day delivery is expanding to 15 new cities. Their logistics network is genuinely hard to compete with. $AMZN",
            published_at="2026-03-12T13:00:00Z", url="https://twitter.com/logisticsnerd/fake009"
        ),
        "topics": ["amazon_inc"]
    },
    {
        "snippet": Snippet(
            id="snip_010", source="reddit", author="u/primeuser99", handle="u/primeuser99",
            text="Amazon's return policy has gotten so much worse. Used to be seamless, now it takes 2 weeks to get a refund. Considering Walmart+.",
            published_at="2026-03-11T15:00:00Z", url="https://reddit.com/r/amazon/fake010"
        ),
        "topics": ["amazon_inc"]
    },
    {
        "snippet": Snippet(
            id="snip_011", source="news", author="Reuters", handle="Reuters",
            text="Amazon Web Services announced record cloud revenue as enterprise adoption surges. CEO Andy Jassy highlighted AI infrastructure investments.",
            published_at="2026-03-10T12:00:00Z", url="https://reuters.com/fake011"
        ),
        "topics": ["amazon_inc"]
    },
    {
        "snippet": Snippet(
            id="snip_012", source="twitter", author="@climatewatch", handle="@climatewatch",
            text="The Amazon rainforest lost another 2,400 sq km of tree cover last quarter. Deforestation rates continue despite global pledges. #Amazon",
            published_at="2026-03-12T09:00:00Z", url="https://twitter.com/climatewatch/fake012"
        ),
        "topics": ["amazon_rainforest", "noise"]
    },
    {
        "snippet": Snippet(
            id="snip_013", source="forum", author="SmallBizOwner", handle="SmallBizOwner",
            text="Selling on Amazon has become nearly impossible for small businesses. The fees keep going up and they keep prioritizing their own brands.",
            published_at="2026-03-09T14:00:00Z", url="https://forum.fake013"
        ),
        "topics": ["amazon_inc"]
    },
    # --- Tesla ---
    {
        "snippet": Snippet(
            id="snip_014", source="twitter", author="Sawyer Merritt", handle="@SawyerMerritt",
            text="Tesla FSD v13.2 just dropped and the improvement is significant. Highway driving is now genuinely hands-off. $TSLA #Tesla",
            published_at="2026-03-12T17:00:00Z", url="https://twitter.com/sawyermerritt/fake014"
        ),
        "topics": ["tesla"]
    },
    {
        "snippet": Snippet(
            id="snip_015", source="reddit", author="u/teslainvestor", handle="u/teslainvestor",
            text="Tesla's Cybertruck production finally ramping. They shipped 28k units last quarter vs 12k the quarter before. Still losing money per truck though.",
            published_at="2026-03-11T11:00:00Z", url="https://reddit.com/r/tsla/fake015"
        ),
        "topics": ["tesla"]
    },
    {
        "snippet": Snippet(
            id="snip_016", source="news", author="Bloomberg", handle="@bloomberg",
            text="Tesla cuts Model Y prices again in Europe by 4%, intensifying pressure on legacy automakers. The EV price war shows no sign of ending.",
            published_at="2026-03-10T09:00:00Z", url="https://bloomberg.com/fake016"
        ),
        "topics": ["tesla"]
    },
    # --- NVIDIA ---
    {
        "snippet": Snippet(
            id="snip_017", source="twitter", author="Jensen Huang", handle="@JensenHuang",
            text="Blackwell architecture is shipping at scale. Every major cloud provider is deploying GB200 clusters. The AI infrastructure build-out is just getting started.",
            published_at="2026-03-12T16:00:00Z", url="https://twitter.com/jensenhuang/fake017"
        ),
        "topics": ["nvidia"]
    },
    {
        "snippet": Snippet(
            id="snip_018", source="reddit", author="u/airesearcher", handle="u/airesearcher",
            text="NVIDIA's H200 is 2x faster than H100 for LLM inference. But the $40k price tag is insane. AMD MI300X at $20k is looking more attractive.",
            published_at="2026-03-11T13:00:00Z", url="https://reddit.com/r/MachineLearning/fake018"
        ),
        "topics": ["nvidia"]
    },
    {
        "snippet": Snippet(
            id="snip_019", source="news", author="Financial Times", handle="@FT",
            text="Nvidia's market cap briefly overtook Apple's again on Wednesday as AI chip demand continues to surge. $NVDA up 8% this week.",
            published_at="2026-03-12T18:30:00Z", url="https://ft.com/fake019"
        ),
        "topics": ["nvidia", "apple_inc"]
    },
    # --- Generic tech noise ---
    {
        "snippet": Snippet(
            id="snip_020", source="twitter", author="TechCrunch", handle="@TechCrunch",
            text="Big Tech earnings season kicks off next week. All eyes on cloud revenue growth and AI capex guidance.",
            published_at="2026-03-10T10:00:00Z", url="https://techcrunch.com/fake020"
        ),
        "topics": ["tech_general"]
    },
    {
        "snippet": Snippet(
            id="snip_021", source="reddit", author="u/marketwatcher", handle="u/marketwatcher",
            text="The Nasdaq is up 2.3% today driven by tech earnings optimism. Hard to not be bullish right now honestly.",
            published_at="2026-03-11T14:30:00Z", url="https://reddit.com/r/investing/fake021"
        ),
        "topics": ["tech_general", "noise"]
    },
    # --- Elon Musk ---
    {
        "snippet": Snippet(
            id="snip_022", source="twitter", author="Elon Musk", handle="@elonmusk",
            text="xAI's Grok 3 is now the most capable AI model on every benchmark. Open weights coming next month.",
            published_at="2026-03-12T20:00:00Z", url="https://twitter.com/elonmusk/fake022"
        ),
        "topics": ["elon_musk", "tesla"]
    },
    {
        "snippet": Snippet(
            id="snip_023", source="news", author="Wall Street Journal", handle="@WSJ",
            text="Elon Musk's political activities are creating headwinds for Tesla's brand in Europe, according to new polling data from YouGov.",
            published_at="2026-03-11T08:00:00Z", url="https://wsj.com/fake023"
        ),
        "topics": ["elon_musk", "tesla"]
    },
    # --- Microsoft ---
    {
        "snippet": Snippet(
            id="snip_024", source="linkedin", author="Satya Nadella", handle="Satya Nadella",
            text="Microsoft Copilot now has 300M monthly active users across M365. AI is fundamentally changing how people work.",
            published_at="2026-03-10T11:00:00Z", url="https://linkedin.com/fake024"
        ),
        "topics": ["microsoft"]
    },
    {
        "snippet": Snippet(
            id="snip_025", source="reddit", author="u/enterprise_dev", handle="u/enterprise_dev",
            text="Azure OpenAI Service is genuinely good now. We migrated our internal tools from OpenAI API and the reliability is night and day. Plus the SLA actually matters.",
            published_at="2026-03-09T15:00:00Z", url="https://reddit.com/r/azure/fake025"
        ),
        "topics": ["microsoft"]
    },
    # --- Google ---
    {
        "snippet": Snippet(
            id="snip_026", source="twitter", author="Google", handle="@Google",
            text="Gemini 2.5 Ultra is now available in Google AI Studio. 1M token context window, native multimodal, and dramatically improved reasoning.",
            published_at="2026-03-12T15:00:00Z", url="https://twitter.com/google/fake026"
        ),
        "topics": ["google"]
    },
    {
        "snippet": Snippet(
            id="snip_027", source="news", author="The Guardian", handle="@guardian",
            text="Google faces new EU antitrust fine over search advertising dominance. Regulators allege preferential treatment of Google Shopping results.",
            published_at="2026-03-11T10:00:00Z", url="https://theguardian.com/fake027"
        ),
        "topics": ["google"]
    },
    # --- OpenAI ---
    {
        "snippet": Snippet(
            id="snip_028", source="twitter", author="Sam Altman", handle="@sama",
            text="GPT-5 is the biggest leap we've made. It's genuinely a different category of system. Rolling out to Plus users this week.",
            published_at="2026-03-12T12:00:00Z", url="https://twitter.com/sama/fake028"
        ),
        "topics": ["openai"]
    },
    {
        "snippet": Snippet(
            id="snip_029", source="reddit", author="u/aiuser", handle="u/aiuser",
            text="OpenAI's pricing is getting ridiculous. $200/month for ChatGPT Pro? Anthropic Claude is way better value and honestly better at coding tasks.",
            published_at="2026-03-10T20:00:00Z", url="https://reddit.com/r/ChatGPT/fake029"
        ),
        "topics": ["openai"]
    },
    {
        "snippet": Snippet(
            id="snip_030", source="news", author="Bloomberg", handle="@bloomberg",
            text="OpenAI closes $10B funding round at $300B valuation. SoftBank leads the round as AI infrastructure spending accelerates.",
            published_at="2026-03-09T09:00:00Z", url="https://bloomberg.com/fake030"
        ),
        "topics": ["openai"]
    },
]


def get_snippets_for_query(entity_name: str, count: int = 10) -> list[Snippet]:
    """
    Return mock snippets relevant to the entity name.
    Includes some noise snippets to make scoring interesting.
    """
    name_lower = entity_name.lower()

    # Map entity names to topic tags
    topic_map = {
        "apple": ["apple_inc", "apple_fruit", "tech_general"],
        "amazon": ["amazon_inc", "amazon_rainforest", "tech_general"],
        "tesla": ["tesla", "elon_musk"],
        "nvidia": ["nvidia", "tech_general"],
        "microsoft": ["microsoft", "tech_general"],
        "google": ["google", "tech_general"],
        "openai": ["openai", "tech_general"],
        "elon": ["elon_musk", "tesla"],
        "musk": ["elon_musk", "tesla"],
    }

    relevant_topics = set()
    for key, topics in topic_map.items():
        if key in name_lower:
            relevant_topics.update(topics)

    if not relevant_topics:
        # fallback: return tech general + a few random ones
        relevant_topics = {"tech_general"}

    matching = [
        item["snippet"] for item in MOCK_SNIPPETS
        if any(t in relevant_topics for t in item["topics"])
    ]

    return matching[:count]


def get_filtered_snippets(entity_name: str, smart_prompt: str, count: int = 10) -> list[Snippet]:
    """
    Return snippets filtered by the smart prompt (mock: exclude obvious noise topics).
    """
    all_snippets = get_snippets_for_query(entity_name, count=20)
    noise_keywords = ["fruit", "orchard", "pie", "recipe", "rainforest",
                      "deforestation", "river", "farming", "harvest"]

    filtered = [
        s for s in all_snippets
        if not any(kw in s.text.lower() for kw in noise_keywords)
    ]
    return filtered[:count]
