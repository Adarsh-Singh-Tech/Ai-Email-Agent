# Project Policies & Best Practices

**Project:** AI Email Agent
**Document Version:** v1.0.0
**Maintained by:** Adarsh Singh

**Last Revised:** 2026
**Applies to:** All contributors, collaborators, and forks of this repository


---

> This document defines the engineering standards, operational policies, and
> development practices that govern all work on the AI Email Agent project.
> Every contributor — including the original author — is expected to follow
> these guidelines. They exist not as bureaucratic overhead, but as the
> accumulated decision-making framework that keeps a growing codebase
> reliable, secure, and maintainable over time.

---

## Table of Contents

1. [Code Structure Policy](#1-code-structure-policy)
2. [API Usage Policy](#2-api-usage-policy)
3. [Security Policy](#3-security-policy)
4. [Email Delivery Policy](#4-email-delivery-policy)
5. [Development Workflow](#5-development-workflow)
6. [Error Handling Strategy](#6-error-handling-strategy)
7. [Scalability Guidelines](#7-scalability-guidelines)
8. [Contribution Guidelines](#8-contribution-guidelines)
9. [Policy Enforcement & Amendments](#9-policy-enforcement--amendments)

---

## 1. Code Structure Policy

### 1.1 The Core / Upgrade Boundary

The repository is divided into two structurally isolated zones. This boundary is not a convention — it is a hard architectural rule.

```
ai-email-agent/
├── core/        ← Production system. Stable. Tested. Never broken.
└── upgrade/     ← Experimental development. Isolated. Never imported by core.
```

**`core/` is the production system.** It must be deployable, functional, and complete at every point in time. Anyone cloning the repository should be able to run `python core/main.py` and receive a delivered newsletter within 15 minutes of setup. No exceptions.

**`upgrade/` is a staging zone.** It exists for features that are planned but not yet proven stable. Code in `upgrade/` may be incomplete, experimental, or actively broken. That is acceptable — because it is completely isolated from `core/`.

#### Enforced rules

| Rule | Enforcement |
|---|---|
| No file in `core/` may import from `upgrade/` | Import review required in all PRs |
| No file in `upgrade/` may modify `core/` behavior | Architectural review required before promotion |
| `core/` must pass a full pipeline test before any commit is merged | CI test gate (planned) |
| Experimental dependencies may only appear in `upgrade/requirements.txt` | Separate requirements files per zone |

#### The promotion process

When a feature in `upgrade/` is considered stable, it is promoted into `core/` through a deliberate, documented integration step:

1. The upgrade module must have documented behavior and known edge cases
2. Integration is performed as a single, focused pull request with a clear title: `promote: [module-name] to core`
3. The promotion PR must not include unrelated changes
4. Post-promotion, the original `upgrade/` files are retained for reference but marked with a deprecation header

### 1.2 Module Responsibility Principle

Each module in `core/` owns exactly one layer of the pipeline. This principle must be maintained as the codebase grows.

| Module | Owns | Does not own |
|---|---|---|
| `main.py` | Pipeline orchestration and sequencing | Business logic of any stage |
| `config.py` | All configurable parameters | Any runtime state |
| `news_fetcher.py` | Feed polling, filtering, deduplication | Summarization, email construction |
| `ai_utils.py` | LLM API calls, prompt construction, fallback | Feed logic, email formatting |
| `email_utils.py` | HTML rendering, MIME construction, SMTP delivery | Article processing, API calls |

If a proposed change requires a module to touch concerns outside its ownership column, that is a signal to refactor — not a reason to expand the module's scope.

### 1.3 Configuration Centralization

**All configurable values must live in `config.py`.** This includes:

- RSS feed URLs
- Model names and fallback sequences
- Relevance scoring thresholds
- Email layout parameters
- Scheduling intervals
- Retry counts and timeout values

Values that change between environments (API keys, email addresses, recipient lists) must be loaded from environment variables in `config.py` and accessed from there by all other modules.

```python
# Correct — configuration read once, accessed everywhere
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
PRIMARY_MODEL = os.getenv("PRIMARY_MODEL", "openai/gpt-4o-mini")

# ✅ Other modules import from config
# ai_utils.py
from config import OPENROUTER_API_KEY, PRIMARY_MODEL

# ❌ Never do this — direct environment access outside config
import os
api_key = os.getenv("OPENROUTER_API_KEY")  # prohibited outside config.py
```

### 1.4 File and Function Naming

- All Python files use `snake_case`
- All functions use `snake_case`
- All classes use `PascalCase`
- Constants use `UPPER_SNAKE_CASE`
- No abbreviations in names unless the abbreviation is universally understood (`api`, `url`, `html`, `smtp` are acceptable; `fn`, `mgr`, `cfg` are not)

---

## 2. API Usage Policy

### 2.1 Fallback is Mandatory, Not Optional

Every external API call in this project is subject to failure. Rate limits, model unavailability, network timeouts, and malformed responses are not edge cases — they are expected operating conditions. All LLM calls must implement a fallback mechanism.

**Minimum required fallback structure:**

```python
def call_with_fallback(payload: dict) -> str:
    models = [config.PRIMARY_MODEL, config.FALLBACK_MODEL]

    for model in models:
        try:
            response = call_openrouter(payload, model=model)
            if is_valid_response(response):
                return response
            logging.warning(f"Model {model} returned invalid response. Trying next.")
        except APIError as e:
            logging.warning(f"Model {model} failed with: {e}. Trying next.")
        except Exception as e:
            logging.error(f"Unexpected error with model {model}: {e}")

    # Final fallback — return raw content rather than crash
    logging.error("All models failed. Returning raw fallback content.")
    return payload.get("raw_summary", "Summary unavailable for this article.")
```

The pipeline must never halt entirely due to an LLM API failure. A newsletter with raw RSS descriptions is better than no newsletter.

### 2.2 No Hardcoded Model Names in Business Logic

Model names must never appear in `ai_utils.py`, `main.py`, or any other business logic file as string literals. They belong exclusively in `config.py` and `.env`.

```python
# ✅ Correct
model = config.PRIMARY_MODEL

# ❌ Prohibited — hardcoded model name in business logic
response = openrouter.complete(model="openai/gpt-4o", ...)
```

**Reason:** Model availability on OpenRouter changes without notice. Models are deprecated, renamed, or throttled. Centralizing model names means a model change requires editing a single configuration value — not hunting through multiple files.

### 2.3 Response Validation Before Use

Every LLM response must be validated before being passed to downstream pipeline stages. Validation must check:

- Response is not `None` or empty
- Response length exceeds a minimum threshold (prevents empty string acceptances)
- Required structural elements are present (for structured outputs, all labeled sections must exist)
- Response does not contain known refusal patterns

```python
def is_valid_response(response: str) -> bool:
    if not response or len(response.strip()) < 50:
        return False
    required_sections = ["WHAT HAPPENED:", "WHY IT MATTERS:", "KEY TAKEAWAY:"]
    return all(section in response for section in required_sections)
```

### 2.4 Rate Limiting and Courtesy Delays

When processing multiple articles in a single run:

- Add a minimum 1-second delay between consecutive API calls
- Do not attempt more than 10 LLM calls per pipeline run without explicit configuration change
- Log total API call counts per run for cost monitoring

```python
import time

for article in filtered_articles[:config.MAX_ARTICLES_PER_RUN]:
    summary = summarize_with_fallback(article)
    article["ai_summary"] = summary
    time.sleep(1)  # Courtesy delay between calls
```

### 2.5 API Key Rotation Readiness

The codebase must be structured so that an API key can be rotated by changing a single `.env` value with zero code changes. This is guaranteed by the configuration centralization policy in Section 1.3.

---

## 3. Security Policy

### 3.1 Absolute Prohibition on Credentials in Code

**No API key, password, email address, or secret value of any kind may ever appear in any Python file, configuration file, or any file tracked by version control.**

This includes:

- `OPENROUTER_API_KEY`
- `GMAIL_APP_PASSWORD`
- `GMAIL_ADDRESS`
- `RECIPIENT_EMAILS`
- Any future service credentials (database passwords, webhook secrets, OAuth tokens)

Violations are treated as critical security incidents regardless of whether the repository is public or private. Credentials committed to git history are considered compromised — rotation is required immediately even after removal.

### 3.2 Environment Variable Management

All secrets are managed through the `.env` file, which is permanently excluded from version control via `.gitignore`.

**Required `.gitignore` entries:**

```gitignore
# Environment and secrets
.env
.env.local
.env.production
*.env

# Do not track credentials of any kind
*.key
*.pem
*.p12
```

A `.env.example` file must exist in the repository root with all required variable names and placeholder values. This file is safe to commit. It must never contain real values.

```env
# .env.example — safe to commit, contains no real values
OPENROUTER_API_KEY=your_openrouter_api_key_here
PRIMARY_MODEL=openai/gpt-4o-mini
FALLBACK_MODEL=mistralai/mistral-7b-instruct
GMAIL_ADDRESS=your.address@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
RECIPIENT_EMAILS=recipient@example.com
```

### 3.3 Gmail App Password Policy

**The Gmail account password must never be used for SMTP authentication.** Only Gmail App Passwords are permitted.

Rationale:
- App Passwords are scoped to a single application and can be revoked independently of the account password
- Google explicitly blocks account password authentication for programmatic SMTP access
- App Passwords do not grant access to the full Google account — they are application-scoped credentials

App Passwords must be:
- Generated specifically for this project, named "AI Email Agent"
- Stored only in the `.env` file
- Rotated if they are ever exposed or if repository access changes

### 3.4 Dependency Security

- All dependencies must be pinned to specific versions in `requirements.txt`
- Dependencies must not be upgraded without reviewing the changelog for security advisories
- No dependency may be added to `core/requirements.txt` without a clear, documented justification
- Packages with known vulnerabilities must be replaced or patched before the next release

### 3.5 Log Sanitization

Application logs must never contain sensitive values. The logging configuration must explicitly mask or exclude credentials.

```python
# ✅ Correct — log the action, not the secret
logging.info(f"Authenticating with Gmail as {config.GMAIL_ADDRESS}")

# ❌ Prohibited — credential exposure in logs
logging.debug(f"Using App Password: {config.GMAIL_APP_PASSWORD}")
```

---

## 4. Email Delivery Policy

### 4.1 Frequency Limits

The AI Email Agent is a newsletter system, not a notification system. Delivery frequency must be controlled to maintain recipient trust and avoid spam classification.

| Delivery type | Maximum frequency | Configuration parameter |
|---|---|---|
| Standard newsletter | Once per day | `MAX_EMAILS_PER_DAY = 1` |
| Test delivery | Up to 5 per day during active development | Manual override only |
| Retry on failure | Maximum 2 retries, 10-minute intervals | `EMAIL_MAX_RETRIES = 2` |

**There must be no mechanism in `core/` that enables sending more than one newsletter email per day to the same recipient without explicit manual override.**

### 4.2 Recipient List Management

- Recipient email addresses must be stored in the `.env` file, never in code
- The system must not send to addresses that have not been explicitly configured
- Multiple recipients are supported via comma-separated values in `RECIPIENT_EMAILS`
- No recipient list storage in publicly accessible files or logs

### 4.3 Content Standards

Every email delivered by this system must meet the following content standards:

- **Subject line** must accurately describe the content — no clickbait or misleading phrasing
- **From address** must be the configured `GMAIL_ADDRESS` — no spoofing or alias deception
- **Unsubscribe guidance** must appear in every newsletter footer — even as a plain instruction to reply requesting removal
- **Plain-text fallback** must be included in every MIME message for accessibility and deliverability

### 4.4 Anti-Spam Compliance

The system must operate in a manner consistent with email best practices to avoid triggering spam filters:

- Emails are sent from a single, consistent `From` address
- HTML content uses standard, clean markup — no hidden text, no misleading links
- No use of purchased, scraped, or unverified recipient lists
- Delivery volume remains within personal-use thresholds (under 500 recipients per day)
- All links in the email must resolve to real, legitimate URLs — no redirects through tracking domains without explicit disclosure

---

## 5. Development Workflow

### 5.1 Phase-Based Development

Features are built in sequential phases. Each phase must produce a working, testable deliverable before the next phase begins. Skipping phases to accelerate delivery consistently produces unstable systems that are slower to debug than they would have been to build correctly.

```
Phase 1 — Core function works       (e.g., SMTP delivery verified)
    ↓
Phase 2 — Intelligence layer added  (e.g., LLM summarization working)
    ↓
Phase 3 — Automation layer added    (e.g., filtering pipeline complete)
    ↓
Phase 4 — Presentation layer added  (e.g., HTML newsletter rendering)
    ↓
Phase 5 — Architecture formalized   (e.g., core/upgrade separation)
    ↓
Phase 6 — Upgrade modules developed (e.g., dashboard, analytics, export)
```

**Never start Phase N+1 until Phase N produces verifiable, working output.**

### 5.2 Test Before Upgrading

Before any `upgrade/` module is promoted to `core/`:

1. The module must have been run successfully in isolation at least 10 times
2. All known failure modes must be documented in the module's docstring or README
3. Edge cases (empty input, API failure, malformed data) must be explicitly handled
4. The integration must be previewed in a development branch before merging to main

### 5.3 Branch Strategy

| Branch | Purpose | Merge policy |
|---|---|---|
| `main` | Production-ready code — `core/` is always deployable | Requires PR review |
| `dev` | Active development integration branch | Requires passing tests |
| `feat/[name]` | Individual feature development | Merge to `dev` only |
| `fix/[name]` | Bug fixes | May merge directly to `main` for critical fixes |
| `upgrade/[name]` | Upgrade module development | Merge to `dev` only |

### 5.4 Commit Message Standards

All commits must follow a structured format:

```
[type]: [concise description in present tense]

[optional body — explain why, not what]
```

**Permitted types:**

| Type | When to use |
|---|---|
| `feat` | New capability added |
| `fix` | Bug corrected |
| `refactor` | Code restructured without behavior change |
| `docs` | Documentation updated |
| `config` | Configuration values changed |
| `promote` | Upgrade module moved to core |
| `security` | Security-related change |

**Examples:**
```
feat: add model fallback chain to ai_utils
fix: correct inline CSS rendering in Outlook email clients
security: remove hardcoded API key from config.py
promote: dashboard_utils moved to core with FastAPI integration
```

---

## 6. Error Handling Strategy

### 6.1 Fail Gracefully, Never Silently

Every error must result in one of two outcomes:

1. **Graceful degradation** — the pipeline continues with reduced functionality and the degraded state is logged
2. **Explicit, informative failure** — the pipeline stops with a clear, actionable error message

Silent failures — where the system appears to succeed but produces no output, logs nothing, or swallows an exception — are the most dangerous class of bug. They are prohibited.

```python
# ✅ Graceful degradation
try:
    summary = summarize_article(article)
except Exception as e:
    logging.warning(f"Summarization failed for '{article['title']}': {e}. Using raw description.")
    summary = article.get("raw_summary", "Summary unavailable.")

# ✅ Explicit failure with actionable message
if not config.GMAIL_APP_PASSWORD:
    raise EnvironmentError(
        "GMAIL_APP_PASSWORD is not set. "
        "Generate an App Password at myaccount.google.com/apppasswords "
        "and add it to your .env file."
    )

# ❌ Silent failure — prohibited
try:
    summary = summarize_article(article)
except:
    pass
```

### 6.2 Logging Standards

The project uses Python's standard `logging` module. Print statements are not permitted in production code.

**Log level usage:**

| Level | When to use |
|---|---|
| `DEBUG` | Detailed diagnostic information useful during development only |
| `INFO` | Normal pipeline progress — stage completions, article counts, delivery confirmation |
| `WARNING` | Recoverable issues — model fallback triggered, article skipped, retry attempted |
| `ERROR` | Unrecoverable stage failure — API completely unavailable, SMTP delivery failed after retries |
| `CRITICAL` | System-level failure — missing required configuration, corrupted state |

**Log format standard:**

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]  %(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
```

**Example compliant log output:**
```
[INFO]   2026-03-15 07:00:01  Stage 1 — Fetching feeds · 6 sources polled
[INFO]   2026-03-15 07:00:04  Stage 2 — Filtering · 43 → 11 articles retained
[WARNING] 2026-03-15 07:00:09  Model gpt-4o-mini failed · retrying with fallback
[INFO]   2026-03-15 07:00:52  Stage 5 — Delivery confirmed · 1 recipient
```

### 6.3 Configuration Validation at Startup

`main.py` must validate all required configuration values before any pipeline stage executes. This prevents confusing mid-pipeline failures caused by missing configuration.

```python
def validate_configuration():
    required = {
        "OPENROUTER_API_KEY": config.OPENROUTER_API_KEY,
        "GMAIL_ADDRESS": config.GMAIL_ADDRESS,
        "GMAIL_APP_PASSWORD": config.GMAIL_APP_PASSWORD,
        "RECIPIENT_EMAILS": config.RECIPIENT_EMAILS,
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise EnvironmentError(
            f"Missing required configuration: {', '.join(missing)}. "
            f"Check your .env file against .env.example."
        )
```

### 6.4 Exception Specificity

Catch specific exceptions, not broad `Exception` classes, wherever the specific exception type is known. Broad catches are acceptable only at the top-level fallback layer where all other specific handling has been exhausted.

```python
# ✅ Specific exception handling
try:
    response = requests.get(feed_url, timeout=10)
    response.raise_for_status()
except requests.exceptions.Timeout:
    logging.warning(f"Feed {feed_url} timed out after 10s. Skipping.")
except requests.exceptions.HTTPError as e:
    logging.warning(f"Feed {feed_url} returned HTTP {e.response.status_code}. Skipping.")

# ❌ Overly broad catch without justification
try:
    response = requests.get(feed_url)
except Exception:
    pass
```

---

## 7. Scalability Guidelines

### 7.1 Design for Extension, Not Modification

New capabilities must be added by extending the system, not by modifying existing working components. When a new feature requires changes to a core module, evaluate whether the change can be implemented through configuration, a new module, or an upgrade module promotion instead.

The Open/Closed principle applies here: core modules should be open for extension and closed for direct modification wherever possible.

### 7.2 Upgrade Module Isolation

Upgrade modules must be fully self-contained. They must not:

- Import from `core/` modules
- Modify any files in `core/`
- Require changes to `core/config.py` for their own operation
- Share state with the running core pipeline

Each upgrade module maintains its own dependencies, its own configuration, and its own data storage. When promoted, the integration is a deliberate, scoped act — not a gradual entanglement.

### 7.3 Stateless Pipeline Design

The core pipeline must be stateless between runs. Each execution of `main.py` is a complete, independent pipeline run. No run may depend on the state or output of a previous run.

This design ensures:
- Runs can be executed manually, on a schedule, or triggered by an API without order dependency
- Failed runs can be retried without side effects
- The system can be reset to a clean state by simply removing any generated output files

State that must persist between runs (run history, analytics) belongs in the `upgrade/analytics` module, not in `core/`.

### 7.4 Configuration-Driven Behavior

Every significant behavioral parameter must be configurable without code changes. As the system grows, the gap between what is hardcoded and what is configurable is where technical debt accumulates. When adding new behavior, ask: "Should this be a configuration value?"

Candidates for configuration that must never be hardcoded:
- Number of articles per run
- Relevance score thresholds
- Model names and fallback sequences
- Retry counts and timeout durations
- Email sending frequency limits
- RSS feed lists

---

## 8. Contribution Guidelines

### 8.1 Code Quality Standards

All code submitted to this repository must meet the following standards before review is requested:

- **PEP 8 compliance** — enforced via `flake8` or equivalent linter. Maximum line length: 100 characters
- **Type annotations** — all function signatures must include parameter and return type annotations
- **Docstrings** — all public functions and classes must include a docstring describing purpose, parameters, and return value
- **No dead code** — commented-out code blocks must not be committed. Use branches for work in progress.
- **No print statements** — use `logging` throughout

```python
# ✅ Compliant function signature
def score_article_relevance(article: dict, keywords: list[str]) -> int:
    """
    Score an article's relevance against a keyword list.

    Args:
        article: Normalized article dict containing 'title' and 'description' keys.
        keywords: List of keyword strings to match against article content.

    Returns:
        Integer relevance score from 0 to 100.
    """
    ...
```

### 8.2 Naming Conventions

| Construct | Convention | Example |
|---|---|---|
| Files | `snake_case` | `news_fetcher.py` |
| Functions | `snake_case` | `fetch_rss_feeds()` |
| Classes | `PascalCase` | `NewsArticle` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_ARTICLES_PER_RUN` |
| Variables | `snake_case` | `filtered_articles` |
| Boolean variables | Prefix with `is_` or `has_` | `is_valid`, `has_summary` |

### 8.3 Pull Request Requirements

All pull requests must include:

1. **A clear title** following the commit message format defined in Section 5.4
2. **A description** explaining what changed, why it changed, and how it was tested
3. **No unrelated changes** — PRs that mix feature work with unrelated cleanup will be asked to split
4. **Updated documentation** — if behavior changed, the README or this document must be updated in the same PR
5. **Confirmation that `core/` still runs end-to-end** — include a note confirming you have run `python core/main.py` successfully after your changes

### 8.4 Documentation Requirements

Every new module, function, or configuration parameter must be documented at the point of addition — not as a follow-up task. Documentation debt compounds. A function without a docstring at the time of creation will likely never have one.

Minimum documentation for:
- **New module:** Module-level docstring explaining purpose, dependencies, and usage
- **New function:** Docstring with purpose, args, return value, and known exceptions
- **New config parameter:** Inline comment explaining the parameter, its valid range or options, and its default value
- **New upgrade module:** README section in the `upgrade/[module]/` directory

### 8.5 Backward Compatibility

Changes to `core/` must not break existing functionality. If a change requires modifying the behavior of a stable module:

1. The old behavior must be preserved as a default
2. New behavior must be opt-in via configuration
3. The change must be documented in `CHANGELOG.md` with migration notes

---

## 9. Policy Enforcement & Amendments

### 9.1 Enforcement Approach

These policies are enforced through code review on all pull requests. Automated enforcement (linting, import boundary checking, test gates) will be introduced progressively as the project scales.

No change that violates a policy in this document will be merged to `main`. If a policy creates an impractical constraint for a specific situation, the correct path is to propose an amendment to the policy — not to work around it silently.

### 9.2 Policy Amendments

This document is versioned. Amendments are proposed through a pull request that modifies this file with:

- The specific section being amended
- The rationale for the change
- The revised policy text

Amendments to security policies require explicit review and sign-off before merging.

### 9.3 Version History

| Version | Date | Author | Summary |
|---|---|---|---|
| v1.0.0 | 2026 | Adarsh Singh | Initial policy document — covers all eight policy areas |

---
---

## 🔗 Related Documents

- 📘 [Project README](Readme.md) — Overview, setup, and usage  
- 🔁 [Versioning Strategy](Version.md) — Version control and release workflow  

---
<div align="center">

**AI Email Agent — Project Policies & Best Practices**
Maintained by Adarsh Singh · Version 1.0.0 · 2026

*Good engineering is not just working code — it is code that others can trust, extend, and maintain.*

</div>
