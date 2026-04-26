import feedparser

KEYWORDS = [
    "AI", "OpenAI", "Google", "Microsoft",
    "LLM", "ChatGPT", "Gemini", "Copilot",
    "machine learning", "deep learning"
]

BLOCKWORDS = [
    "stock", "share price", "earnings", "IPO"
]


def relevance_score(title):
    score = 0
    title_lower = title.lower()

    for k in KEYWORDS:
        if k.lower() in title_lower:
            score += 2

    for b in BLOCKWORDS:
        if b in title_lower:
            score -= 3

    return score


def clean_link(link):
    if "url=" in link:
        return link.split("url=")[-1]
    return link


def deduplicate(articles):
    seen = set()
    unique = []

    for a in articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)

    return unique


def get_ai_news():
    url = "https://news.google.com/rss/search?q=artificial+intelligence"
    feed = feedparser.parse(url)

    scored_articles = []

    for entry in feed.entries:
        score = relevance_score(entry.title)

        if score < 1:
            continue

        scored_articles.append({
            "title": entry.title,
            "link": clean_link(entry.link),
            "summary": entry.summary,
            "score": score
        })

    # sort by relevance
    scored_articles.sort(key=lambda x: x["score"], reverse=True)

    # deduplicate
    scored_articles = deduplicate(scored_articles)

    return scored_articles[:5]