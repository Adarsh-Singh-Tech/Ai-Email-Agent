from openai import OpenAI
from core.config import OPENROUTER_API_KEY, MODEL

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

def generate_dashboard_insights():
    prompt = """
Create an AI insights dashboard.

Include:
- Best AI tools for developers, data scientists, DevOps
- Market trends
- Opportunities
- Risks

Make it structured and insightful.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content