from openai import OpenAI
from config import OPENROUTER_API_KEY, MODEL

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)


def summarize_news(articles):
    content = "\n\n".join(
        [f"{a['title']}\n{a['summary']}\n{a['link']}" for a in articles]
    )

    prompt = f"""
You are a professional AI newsletter writer.

Your goal is to create a clean, consistent, and insightful AI newsletter.

STRICT RULES (must follow):
- Use EXACT same heading format for every news item
- Do NOT change headings or structure
- Do NOT add extra emojis beyond defined ones
- Do NOT hallucinate links (ONLY use provided links)
- Avoid generic phrases like "this is important"
- Be specific, concise, and insightful

--------------------------------------

FORMAT (follow exactly):

## 🧠 Top Insight
Write 2-3 lines highlighting the most important AI trend from the articles.

## 🔥 AI News

### 🔹 <Title>

**What happened:**  
Explain clearly in 2-3 lines.

**Why it matters:**  
Explain significance in 1-2 lines.

**Impact:**  
Give practical implication in 1-2 lines.

**Source:**  
<ONLY use the exact link from input>

(repeat same format for each article)

## 📊 Trend Summary
Summarize overall direction of AI in 2-3 lines.

--------------------------------------

QUALITY RULES:
- Keep language simple but sharp
- Avoid repetition across news items
- Each news should add new information
- Maintain professional tone

--------------------------------------

Articles:
{content}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,   # balanced creativity
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "AI Newsletter Agent"
            }
        )

        return response.choices[0].message.content

    except Exception as e:
        print("⚠️ AI failed, fallback mode...", e)

        # fallback (clean structured, no AI)
        fallback = "## 🔥 AI News\n\n"

        for a in articles:
            fallback += f"""
### 🔹 {a['title']}

**What happened:**  
{a['summary']}

**Why it matters:**  
Key update in AI ecosystem.

**Impact:**  
May affect developers and businesses.

**Source:**  
{a['link']}

"""

        fallback += "\n## 📊 Trend Summary\nAI development continues to accelerate across companies."

        return fallback