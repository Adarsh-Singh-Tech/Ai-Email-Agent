<div align="center">

# 📧 AI Email Agent

### *Intelligent news curation, AI-powered summarization, and automated newsletter delivery — fully automated.*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-LLM_Backend-8B5CF6?style=flat-square)](https://openrouter.ai)
[![Gmail SMTP](https://img.shields.io/badge/Gmail-SMTP_Delivery-EA4335?style=flat-square&logo=gmail&logoColor=white)](https://support.google.com/mail)
[![RSS Feeds](https://img.shields.io/badge/RSS-News_Fetching-FFA500?style=flat-square&logo=rss&logoColor=white)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()
[![Automation](https://img.shields.io/badge/Automation-Email_Pipeline-10B981?style=flat-square)]()

<br/>

> **Fetches AI news. Filters the noise. Summarizes with LLMs.**
> **Delivers a clean, professional newsletter to your inbox — on autopilot.**

<br/>

[Overview](#-project-overview) · [Features](#-features) · [How It Works](#-how-it-works) · [Architecture](#-architecture) · [Setup](#-setup-instructions) · [Configuration](#-configuration) · [Run](#-how-to-run) · [Roadmap](#-upgrade-roadmap) · [Challenges](#-challenges-faced)

</div>

---

## 🚀 Project Overview

**AI Email Agent** is a Python-based, fully automated email intelligence system that monitors the AI/ML landscape, curates the most relevant news, summarizes it using large language models, and delivers a structured newsletter-style digest directly to your inbox.

Built for engineers, researchers, and AI enthusiasts who want to stay current without spending hours browsing feeds, this project replaces the manual "read everything and figure out what matters" workflow with an end-to-end pipeline that runs on a schedule and delivers only what is worth reading.

### The core problem it solves

The volume of AI-related content published daily — research papers, product announcements, industry news, opinion pieces — is far beyond what any individual can process. Most content is noise. The signal is buried. This system extracts the signal, summarizes it intelligibly, and delivers it formatted as a professional newsletter.

### What makes it different

- Not a simple RSS-to-email forwarder — every item passes through a relevance scoring and deduplication filter before reaching the AI summarization layer
- Summaries are structured, not just truncations — the prompt engineering layer ensures each summary includes context, significance, and key takeaways
- Architecture is explicitly designed with a `core/` and `upgrade/` separation, keeping the working system stable while future capabilities are developed in isolation

---

## ✨ Features

| Feature | Description |
|---|---|
| 📡 **RSS Feed Aggregation** | Fetches content from multiple configurable AI/ML news sources simultaneously |
| 🎯 **Relevance Scoring** | Each item is scored against configurable keyword sets — low-relevance items are filtered before summarization |
| 🔁 **Deduplication** | URL and title-based deduplication prevents the same story from appearing across multiple sources |
| 🗑️ **Noise Removal** | Strips promotional content, generic filler articles, and low-information items |
| 🧠 **AI Summarization** | LLM-generated summaries via OpenRouter API with structured prompt engineering |
| 🔄 **Model Fallback** | Automatic fallback to secondary models if the primary model is unavailable or fails |
| 📨 **Gmail SMTP Delivery** | Reliable email delivery via Gmail's SMTP layer with App Password authentication |
| 🎨 **HTML Newsletter Formatting** | Clean, structured HTML email layout with sections, headlines, and readable typography |
| 🧩 **Modular Upgrade System** | Future features (dashboard, analytics, export) are isolated in a separate `upgrade/` module — the core system remains stable |

---

## 🧠 How It Works

The system operates as a sequential pipeline. Each stage has a defined input, output, and failure behavior.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      AI Email Agent Pipeline                        │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  STAGE 1 — News Fetching  (news_fetcher.py)                  │  │
│  │  Sources: RSS feeds (TechCrunch AI, ArXiv, Wired, VentureBeat│  │
│  │  Output:  Raw article list  {title, url, summary, published}  │  │
│  └────────────────────────────┬─────────────────────────────────┘  │
│                               │  Raw articles (unfiltered)         │
│                               ▼                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  STAGE 2 — Smart Filtering  (news_fetcher.py)                │  │
│  │  · Relevance scoring against keyword config                   │  │
│  │  · URL + title deduplication                                  │  │
│  │  · Noise removal (promotional, low-info articles)             │  │
│  │  Output:  Filtered, ranked article list                       │  │
│  └────────────────────────────┬─────────────────────────────────┘  │
│                               │  Filtered articles (top N)         │
│                               ▼                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  STAGE 3 — AI Summarization  (ai_utils.py)                   │  │
│  │  · Structured prompt: context + significance + takeaway       │  │
│  │  · Primary model via OpenRouter API                           │  │
│  │  · Auto-fallback to secondary model on failure                │  │
│  │  Output:  Article objects with AI-generated summaries          │  │
│  └────────────────────────────┬─────────────────────────────────┘  │
│                               │  Summarized articles               │
│                               ▼                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  STAGE 4 — Newsletter Assembly  (email_utils.py)             │  │
│  │  · HTML template rendering                                    │  │
│  │  · Section grouping by topic/source                           │  │
│  │  · Typography, spacing, and mobile-friendly layout            │  │
│  │  Output:  Complete HTML email body                            │  │
│  └────────────────────────────┬─────────────────────────────────┘  │
│                               │  Rendered HTML                     │
│                               ▼                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  STAGE 5 — Gmail SMTP Delivery  (email_utils.py)             │  │
│  │  · MIME email construction (HTML + plain text fallback)       │  │
│  │  · Gmail SMTP with App Password authentication                │  │
│  │  · Delivery confirmation + error logging                      │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Config layer: config.py  ──────────────────────── all stages      │
└─────────────────────────────────────────────────────────────────────┘
```

### Stage-by-stage explanation

**Stage 1 — News Fetching:** `news_fetcher.py` polls a configurable list of RSS feed URLs using the `feedparser` library. Each feed is parsed into a normalized article schema: `{title, url, raw_summary, published_date, source}`. Network failures on individual feeds are caught and logged without halting the pipeline.

**Stage 2 — Smart Filtering:** The raw article list passes through three filters in sequence. The relevance scorer assigns each article a score from 0–100 based on keyword presence in the title and description. Items below the configurable threshold are dropped. The deduplicator removes items sharing a URL or a title similarity above a defined threshold. The noise filter removes items matching known low-value patterns (sponsored, listicle-heavy, non-technical content).

**Stage 3 — AI Summarization:** The filtered articles are sent to the OpenRouter API with a structured system prompt that instructs the model to produce a three-part summary: (1) what happened, (2) why it matters, and (3) one key takeaway. If the primary model returns an error or malformed output, the system automatically retries with a fallback model defined in `config.py`.

**Stage 4 — Newsletter Assembly:** `email_utils.py` takes the summarized article list and renders it into a complete HTML email using inline styles for maximum email client compatibility. Articles are grouped by section, each with a headline, source attribution, publication date, AI summary, and "Read full article" link.

**Stage 5 — Gmail SMTP Delivery:** The rendered HTML is wrapped in a `MIMEMultipart` message with a plain-text fallback. The system authenticates with Gmail's SMTP server using a Gmail App Password (not your account password) and delivers the email to the configured recipient list.

---

## 🏗 Architecture

The project is deliberately split into two distinct zones: a stable working core and an isolated upgrade path.

```
ai-email-agent/
│
├── core/                          # CURRENT WORKING SYSTEM
│   ├── main.py                    # Pipeline orchestrator — runs all stages in sequence
│   ├── news_fetcher.py            # RSS feed fetching, filtering, deduplication
│   ├── ai_utils.py                # OpenRouter API, summarization, model fallback
│   ├── email_utils.py             # HTML assembly, SMTP delivery, MIME construction
│   └── config.py                  # All configurable parameters — feeds, keys, thresholds
│
├── upgrade/                       # FUTURE FEATURES — isolated, not imported by core
│   │
│   ├── dashboard/
│   │   ├── dashboard_utils.py     # Data preparation for web dashboard
│   │   └── dashboard_api.py       # FastAPI endpoints for dashboard backend
│   │
│   ├── export/
│   │   └── export_utils.py        # CSV / JSON / PDF export of newsletter data
│   │
│   └── analytics/
│       └── analytics_utils.py     # Open rate tracking, click analytics, trend analysis
│
├── requirements.txt               # Pinned dependencies
└── README.md
```

### Design decision: why `core/` and `upgrade/` are separated

This separation is intentional and has real engineering value.

The `core/` directory contains a tested, working system with no experimental dependencies. It can be cloned and run in under 15 minutes. Changes to `upgrade/` modules have zero risk of breaking the email pipeline.

The `upgrade/` directory is a staging zone. Features are built and tested here without any import relationship to `core/`. When an upgrade module is proven stable, it is promoted into `core/` through an explicit integration step — never by gradual coupling.

This mirrors the trunk-based development pattern used by teams who need to ship reliably while building new capability in parallel.

### Core module responsibilities

| Module | Responsibility |
|---|---|
| `main.py` | Orchestrates the full pipeline. Calls fetcher → filter → summarize → assemble → send. Entry point for all execution. |
| `config.py` | Single source of truth for all configuration: RSS feed URLs, API keys, recipient list, filter thresholds, model names, email styling parameters. |
| `news_fetcher.py` | Feed polling, article normalization, relevance scoring, deduplication, noise filtering. |
| `ai_utils.py` | OpenRouter API client, prompt construction, model fallback logic, response parsing and validation. |
| `email_utils.py` | HTML newsletter template, MIME message construction, Gmail SMTP authentication, delivery with retry. |

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.10 or higher
- A Gmail account with 2-Step Verification enabled
- An [OpenRouter](https://openrouter.ai) account and API key

### Step 1 — Clone the repository

```bash
git clone https://github.com/yourusername/ai-email-agent.git
cd ai-email-agent
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# ─────────────────────────────────────────────
# OpenRouter Configuration
# ─────────────────────────────────────────────
OPENROUTER_API_KEY=your_openrouter_api_key_here
PRIMARY_MODEL=openai/gpt-4o-mini
FALLBACK_MODEL=mistralai/mistral-7b-instruct

# ─────────────────────────────────────────────
# Gmail SMTP Configuration
# ─────────────────────────────────────────────
GMAIL_ADDRESS=your.email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# ─────────────────────────────────────────────
# Email Delivery
# ─────────────────────────────────────────────
RECIPIENT_EMAILS=recipient1@email.com,recipient2@email.com
EMAIL_SUBJECT=Your Daily AI Intelligence Briefing
```

### Step 5 — Review feed configuration

Open `core/config.py` and verify the RSS feed list. Default feeds included:

```python
RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.wired.com/feed/category/artificial-intelligence/latest/rss",
    "https://rss.arxiv.org/rss/cs.AI",
    "https://openai.com/blog/rss.xml",
]
```

Add, remove, or replace feeds to match your interests.

---

## 🔐 Configuration

### Obtaining a Gmail App Password

Gmail requires an App Password for programmatic SMTP access. Your regular account password will not work.

**Step 1:** Enable 2-Step Verification on your Google account.
Go to [myaccount.google.com/security](https://myaccount.google.com/security) → 2-Step Verification → Enable.

**Step 2:** Generate an App Password.
Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
Select app: **Mail** · Select device: **Other (Custom name)** → Enter "AI Email Agent" · Click **Generate**.

**Step 3:** Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`) into your `.env` file as `GMAIL_APP_PASSWORD`.

> ⚠️ Store your App Password securely. Never commit it to version control. The `.gitignore` in this repository excludes `.env` by default.

---

### Obtaining an OpenRouter API Key

**Step 1:** Create an account at [openrouter.ai](https://openrouter.ai).

**Step 2:** Navigate to **Keys** in your dashboard.

**Step 3:** Click **Create Key** → name it "AI Email Agent" → copy the key.

**Step 4:** Add credits to your account (minimum $1 recommended — GPT-4o-mini runs at ~$0.002 per newsletter generation).

**Step 5:** Add the key to your `.env` file as `OPENROUTER_API_KEY`.

---

### Full configuration reference

All parameters are adjustable in `core/config.py`:

```python
# Filtering thresholds
RELEVANCE_SCORE_THRESHOLD = 40      # 0–100. Items below this are dropped.
MAX_ARTICLES_PER_RUN = 10           # Maximum articles to summarize per run
DEDUP_TITLE_SIMILARITY = 0.85       # Cosine similarity threshold for title dedup

# Summarization
MAX_SUMMARY_TOKENS = 200            # Token limit per article summary
SUMMARY_TEMPERATURE = 0.3           # Lower = more factual, less creative

# Email layout
EMAIL_ARTICLES_PER_SECTION = 5      # Articles before a visual section break
INCLUDE_PLAIN_TEXT_FALLBACK = True  # Generate plain text version alongside HTML
```

---

## ▶️ How to Run

### Run once (immediate delivery)

```bash
cd core
python main.py
```

The terminal will display pipeline progress:

```
[INFO]  Fetching feeds...          6 feeds polled, 47 articles retrieved
[INFO]  Filtering...               47 → 12 articles after relevance + dedup
[INFO]  Summarizing...             Article 1/12: "OpenAI releases..."
[INFO]  Summarizing...             Article 2/12: "Google DeepMind..."
...
[INFO]  Assembling newsletter...   HTML rendered (14,203 bytes)
[INFO]  Sending email...           Delivered to 2 recipient(s)
[SUCCESS] Pipeline complete.       Total runtime: 47.3s
```

### Schedule with cron (Linux / macOS)

To run every morning at 7:00 AM:

```bash
crontab -e
```

Add the following line:

```
0 7 * * * /path/to/venv/bin/python /path/to/ai-email-agent/core/main.py >> /path/to/logs/agent.log 2>&1
```

### Schedule with Task Scheduler (Windows)

1. Open **Task Scheduler** → **Create Basic Task**
2. Set trigger: **Daily** at your preferred time
3. Set action: **Start a program**
4. Program: `C:\path\to\venv\Scripts\python.exe`
5. Arguments: `C:\path\to\ai-email-agent\core\main.py`

### Run with Docker (optional)

```bash
docker build -t ai-email-agent .
docker run --env-file .env ai-email-agent
```

---

## 📩 Sample Output Description

The delivered email is a structured HTML newsletter with the following layout.

**Header section:** A clean masthead displaying the newsletter title, generation timestamp, and article count for the current edition.

**Summary statistics bar:** Three inline metrics — total sources polled, articles after filtering, and AI summaries generated — give the reader confidence that active curation happened.

**Article cards:** Each article is rendered as a card containing:
- Article headline (linked to source)
- Source name and publication timestamp
- AI-generated summary in three parts: *What happened* · *Why it matters* · *Key takeaway*
- "Read full article →" call to action

**Section dividers:** After every 5 articles, a visual divider with a subtle section label separates content blocks, making long editions scannable.

**Footer:** Unsubscribe notice, generation metadata (model used, runtime), and a link to the repository.

**Plain-text fallback:** A readable plain-text version is included for email clients that do not render HTML, and for deliverability scoring purposes.

---

## 📊 Upgrade Roadmap

The `upgrade/` directory contains the scaffolding for three planned feature modules. Each is developed in isolation from the working core system.

---

### 📊 Module 1 — Dashboard (`upgrade/dashboard/`)

**Status:** In development · **Dependencies:** FastAPI, Jinja2, SQLite

A web-based dashboard that visualizes newsletter generation history, article metrics, and delivery status.

| File | Purpose |
|---|---|
| `dashboard_utils.py` | Queries the local SQLite run history database, formats data for display |
| `dashboard_api.py` | FastAPI application with endpoints: `/runs`, `/articles`, `/stats`, `/preview/{run_id}` |

**Planned features:** Run history with timestamps and article counts · Per-article relevance score visualization · Newsletter preview rendering · Source-level feed performance metrics.

**Estimated promotion to `core/`:** v1.2.0

---

### 📤 Module 2 — Export (`upgrade/export/`)

**Status:** Scaffolded · **Dependencies:** pandas, reportlab, openpyxl

Enables export of newsletter data in structured formats for archival, analysis, or sharing.

| File | Purpose |
|---|---|
| `export_utils.py` | Handles CSV, JSON, and PDF export of article data and summaries |

**Planned export formats:** CSV (article list with relevance scores and summaries) · JSON (full structured pipeline output) · PDF (print-formatted newsletter edition).

**Estimated promotion to `core/`:** v1.3.0

---

### 📈 Module 3 — Analytics (`upgrade/analytics/`)

**Status:** Scaffolded · **Dependencies:** SQLite, matplotlib

Tracks newsletter performance and content trends over time.

| File | Purpose |
|---|---|
| `analytics_utils.py` | Aggregates run data, computes trend metrics, generates insight summaries |

**Planned features:** Source reliability tracking · Keyword trend analysis · Email delivery success rate tracking · Summarization model performance comparison.

**Estimated promotion to `core/`:** v1.4.0

---

## ⚠️ Challenges Faced

### Challenge 1 — OpenRouter API model failures

**What happened:** The initial implementation used a single hardcoded model (`gpt-4`). OpenRouter's model availability fluctuates — certain models return `503 Service Unavailable` or `model_not_found` errors during high-demand periods. When the model failed, the entire summarization stage failed and the pipeline stopped with no email delivered.

### Challenge 2 — Gmail SMTP authentication rejections

**What happened:** Initial implementation attempted SMTP authentication using the Gmail account password directly. Google's security policies block this entirely — the server rejected authentication with `(534, '5.7.9 Application-specific password required')`. Google deprecated "Less secure app access" in 2022, making this error non-obvious for developers encountering it for the first time.

### Challenge 3 — Poor summarization quality

**What happened:** Early prompt versions sent article titles and raw RSS descriptions to the model with a simple "summarize this" instruction. Output was inconsistent — sometimes a single sentence, sometimes a full paragraph, sometimes a list. The unstructured output could not be rendered cleanly in the HTML newsletter template.

### Challenge 4 — Noisy news filtering

**What happened:** Without relevance filtering, RSS feeds returned a mix of genuinely useful AI news alongside product reviews, sponsored posts, generic tech opinion pieces, and articles that mentioned "AI" only tangentially. Sending all of this to the summarization layer wasted API tokens and degraded newsletter quality significantly.

### Challenge 5 — HTML email rendering inconsistency

**What happened:** Initial HTML templates used `<style>` blocks and CSS classes. Most email clients — Outlook in particular, but also Gmail in some rendering modes — strip or ignore `<style>` blocks entirely. The newsletter rendered perfectly in a browser preview and completely unstyled in production email clients.

---

## ✅ Solutions Implemented

### Solution 1 — Model fallback chain

A fallback sequence was implemented in `ai_utils.py`. If the primary model returns any error, the system automatically retries with the fallback model from `config.py`. If both fail, the pipeline logs the failure and sends the newsletter with unprocessed article descriptions rather than halting entirely.

```python
# ai_utils.py — simplified fallback logic
def summarize_with_fallback(article: dict) -> str:
    for model in [config.PRIMARY_MODEL, config.FALLBACK_MODEL]:
        try:
            response = call_openrouter(article, model)
            if response and len(response) > 50:
                return response
        except Exception as e:
            logging.warning(f"Model {model} failed: {e}. Trying next.")
    return article.get("raw_summary", "Summary unavailable.")
```

### Solution 2 — Gmail App Password authentication

The SMTP authentication was updated to use Gmail App Passwords exclusively. A startup validation check was added to `main.py` that verifies the App Password environment variable is set and non-empty before any network operations are attempted.

```python
# email_utils.py — correct SMTP authentication
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(config.GMAIL_ADDRESS, config.GMAIL_APP_PASSWORD)
    server.send_message(msg)
```

### Solution 3 — Structured prompt engineering

The summarization prompt was redesigned with an explicit three-section output format contract. The response parser validates that all three sections are present before accepting the output — malformed responses trigger a retry.

```python
SYSTEM_PROMPT = """You are a concise AI news analyst writing for a technical audience.
For each article, produce exactly three labeled sections:

WHAT HAPPENED: One sentence describing the development factually.
WHY IT MATTERS: One sentence explaining the significance to the AI field.
KEY TAKEAWAY: One actionable or notable insight for practitioners.

Do not add any other text, headers, or commentary outside these three sections."""
```

### Solution 4 — Relevance scoring and deduplication

A two-stage filter was implemented before the summarization stage. The relevance scorer computes a weighted keyword match score for each article based on title (weighted 2x) and description (weighted 1x). The deduplicator uses URL normalization as a first pass, then applies title token overlap comparison to catch rephrased versions of the same story from different sources.

**Result:** Average article count dropped from ~45 raw to ~10–12 filtered per run, with no meaningful reduction in newsletter information value.

### Solution 5 — Inline CSS HTML formatting

All CSS was converted from `<style>` blocks to inline `style=""` attributes. A Python helper function handles the inline style injection during template rendering, producing consistent output across Gmail, Outlook, Apple Mail, and mobile clients.

```python
# email_utils.py — inline style approach for email client compatibility
ARTICLE_CARD_STYLE = (
    "background:#ffffff;"
    "border:1px solid #e8e8e8;"
    "border-radius:8px;"
    "padding:20px 24px;"
    "margin-bottom:16px;"
    "font-family:Arial,sans-serif;"
)
```

---

## 🧭 Development Phases

### Phase 1 — Basic email sender

**Goal:** Send a hardcoded email via Python.
**Deliverable:** A working script that authenticates with Gmail SMTP and sends a plain-text email to a configured recipient.
**Key learning:** Gmail App Password requirement identified and resolved. SMTP with SSL vs TLS differences documented.

### Phase 2 — AI summarization

**Goal:** Take a single article URL and return an AI-generated summary via OpenRouter.
**Deliverable:** `ai_utils.py` with a working `summarize_article()` function tested with real article content.
**Key learning:** Prompt structure has an outsized impact on output consistency. Structured output format contracts produce reliable, parseable summaries.

### Phase 3 — Smart filtering

**Goal:** Pull 40+ articles from RSS feeds and return only the 10 most relevant.
**Deliverable:** `news_fetcher.py` with full fetch, score, deduplicate, and filter pipeline.
**Key learning:** Simple keyword scoring is surprisingly effective. The deduplication step is essential — 20–30% of articles across different feeds are the same story.

### Phase 4 — Newsletter formatting

**Goal:** Combine filtered, summarized articles into a readable HTML email.
**Deliverable:** `email_utils.py` with HTML template, inline CSS, and MIME construction. Full end-to-end pipeline operational.
**Key learning:** Email HTML is a distinct discipline from web HTML. Inline styles are mandatory. Table-based layouts outperform flexbox in email client compatibility.

### Phase 5 — Modular upgrade system

**Goal:** Establish a clean architecture separating the stable working system from future capabilities.
**Deliverable:** `upgrade/` directory with dashboard, analytics, and export scaffolding. `core/` hardened and fully documented.
**Key learning:** Isolating experimental code from production code from the beginning prevents the gradual coupling that makes future refactoring painful.

---

## 📦 Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.10+ | Core runtime |
| **feedparser** | 6.0.11 | RSS feed parsing |
| **requests** | 2.31.0 | HTTP client for API calls |
| **openai** | 1.30.1 | OpenRouter API client (OpenAI-compatible interface) |
| **python-dotenv** | 1.0.1 | Environment variable management |
| **smtplib** | stdlib | Gmail SMTP delivery (Python standard library) |
| **email** | stdlib | MIME message construction (Python standard library) |
| **FastAPI** | 0.111.0 | Dashboard API backend (upgrade module) |
| **SQLite** | stdlib | Run history storage (upgrade module) |
| **pandas** | 2.2.2 | Export data handling (upgrade module) |

---

## 🔮 Future Enhancements

| Enhancement | Priority | Description |
|---|---|---|
| **Built-in scheduler** | High | Native scheduling so the agent runs autonomously without external cron configuration |
| **Multi-topic support** | High | Multiple topic profiles (AI, cybersecurity, finance) each with dedicated feeds and recipient groups |
| **Web dashboard** | Medium | Browser-based view of run history, article metrics, and newsletter previews (see `upgrade/dashboard`) |
| **Open rate tracking** | Medium | Embedded tracking to measure which newsletters are opened |
| **Sentiment tagging** | Medium | Tag each article as positive/negative/neutral relative to the AI field |
| **Vector-based relevance scoring** | Low | Replace keyword scoring with embedding-based semantic similarity for higher-precision filtering |
| **Telegram / Slack delivery** | Low | Alternative delivery channels alongside email |
| **Interactive digest** | Low | Allow recipients to reply with preferences to tune future editions |

---

## 🤝 Contribution Guidelines

Contributions are welcome. The project maintains a clean separation between `core/` (stable, tested) and `upgrade/` (experimental), and contributions should respect this boundary.

### What contributions are most useful

- New RSS feed sources for the `config.py` default list
- Improved prompt templates in `ai_utils.py`
- Progress on dashboard, analytics, or export upgrade modules
- HTML template improvements with broader email client compatibility
- Unit test coverage for filtering logic in `news_fetcher.py`

### Contribution process

```bash
# Fork the repository and clone your fork
git clone https://github.com/yourusername/ai-email-agent.git
cd ai-email-agent

# Create a feature branch
git checkout -b feature/your-feature-name

# Install dependencies and test
pip install -r requirements.txt
python core/main.py

# Commit with a descriptive message
git commit -m "feat: add embedding-based relevance scoring to news_fetcher"

# Push and open a pull request
git push origin feature/your-feature-name
```

### Branch naming conventions

| Prefix | Usage |
|---|---|
| `feat/` | New feature or capability |
| `fix/` | Bug fix |
| `docs/` | Documentation update |
| `upgrade/` | Work on upgrade module features |
| `refactor/` | Code restructuring without behavior change |

### Code style

- Follow PEP 8 for all Python code
- All public functions must include docstrings
- Environment variables must never be hardcoded — always use `config.py` or `.env`
- New features in `upgrade/` must not import from `core/` until formally promoted through an integration step

---

## 📄 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2026 Adarsh Singh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

---

# 🔥 Step 4: Add one more line (top of README)

Near project description, add:

```md id="tt3qyk"
👉 Includes real email preview (.eml) with local viewer support
View raw load (file:///private/var/folders/fj/10t080jn6kg8fgrp1xz91pkc0000gn/T/tmpm0r7y462.html)
---

## 📜 Documentation & Policies

- 📄 [License](Project_Policies.md) — Terms of use and permissions  
- 🔁 [Versioning Strategy](Version.md) — Release process and version control  

---
<div align="center">

**AI Email Agent**
Built with Python · OpenRouter · Gmail SMTP · RSS Intelligence

*Stay informed without the noise.*

<br/>

If this project was useful, consider starring the repository.

</div>
