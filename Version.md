# Git Version Control Strategy
### AI Email Agent Project

> **Document Version:** 1.0.0
> **Last Updated:** April 2026
> **Maintained By:** AI Email Agent Core Team

---

## Table of Contents

1. [Branch Strategy](#1-branch-strategy)
2. [Commit Message Guidelines](#2-commit-message-guidelines)
3. [Versioning Strategy](#3-versioning-strategy)
4. [Release Process](#4-release-process)
5. [Folder Change Rules](#5-folder-change-rules)
6. [Documentation Updates](#6-documentation-updates)
7. [Rollback Strategy](#7-rollback-strategy)

---

## 1. Branch Strategy

The project follows a structured branching model designed to separate stable production code from active development and experimental features.

### Branch Overview

```
main
 └── dev
      ├── feature/ai-summarization
      ├── feature/smtp-oauth
      └── feature/dashboard-ui
```

### Branch Definitions

| Branch | Purpose | Protected | Merge Target |
|--------|---------|-----------|--------------|
| `main` | Stable, production-ready code | ✅ Yes | — |
| `dev` | Active development and integration | ✅ Yes | `main` |
| `feature/*` | Individual feature development | ❌ No | `dev` |

---

### `main` — Production Branch

- Contains only **stable, tested, and release-tagged** code.
- Direct commits are **strictly prohibited**.
- All changes must arrive via pull request from `dev`.
- Every merge to `main` must be accompanied by a version tag (e.g., `v1.0.0`).

```bash
# ✅ Correct — merge via pull request only
git checkout main
git merge --no-ff dev
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin main --tags
```

---

### `dev` — Development Branch

- The primary branch for integrating completed features.
- All `feature/*` branches are merged here first.
- Must pass all tests before merging into `main`.
- Reflects the **next upcoming release**.

```bash
# Create dev branch from main (initial setup)
git checkout -b dev main
git push -u origin dev
```

---

### `feature/*` — Feature Branches

- Created from `dev` for each new feature, fix, or task.
- Named using the format: `feature/<short-description>`
- Deleted after successful merge into `dev`.

```bash
# Create a new feature branch
git checkout -b feature/ai-summarization dev

# Push to remote
git push -u origin feature/ai-summarization

# After completion — merge back to dev
git checkout dev
git merge --no-ff feature/ai-summarization
git push origin dev

# Delete feature branch
git branch -d feature/ai-summarization
git push origin --delete feature/ai-summarization
```

**Naming Examples:**

```
feature/ai-summarization
feature/smtp-oauth-login
feature/email-tagging
feature/saas-dashboard
feature/bulk-reply-handler
```

---

## 2. Commit Message Guidelines

Every commit must follow a clear, consistent format to maintain a readable and auditable project history.

### Commit Format

```
<type>: <short description>

[optional body]

[optional footer — issue reference, breaking change note]
```

- **Type:** lowercase keyword indicating the nature of the change
- **Short description:** imperative, present-tense summary (max 72 characters)
- **Body:** optional explanation of *why*, not *what*
- **Footer:** optional — reference issues (`Closes #42`) or note breaking changes

---

### Commit Types

| Type | When to Use |
|------|-------------|
| `feat` | Introducing a new feature |
| `fix` | Patching a bug or error |
| `refactor` | Code restructuring without behavior change |
| `docs` | Documentation updates only |
| `style` | Formatting, whitespace — no logic change |
| `test` | Adding or updating tests |
| `chore` | Build process, dependencies, config changes |
| `perf` | Performance improvements |
| `revert` | Reverting a previous commit |

---

### Examples

```bash
# New feature
feat: add AI summarization for incoming emails

# Bug fix
fix: resolve SMTP login failure on expired token

# Refactoring
refactor: restructure project folders for modularity

# Documentation
docs: update README with environment setup steps

# Dependency update
chore: upgrade nodemailer to v6.9.4

# Reverting a change
revert: undo dashboard routing change from commit a3f92bc
```

---

### Rules

- ✅ Use the **imperative mood** — "add", "fix", "update" (not "added" or "fixing")
- ✅ Keep the subject line **under 72 characters**
- ✅ Separate subject and body with a **blank line**
- ❌ Do **not** end the subject line with a period
- ❌ Do **not** use vague messages like `update stuff` or `fix bug`

---

## 3. Versioning Strategy

The project uses **Semantic Versioning (SemVer)**: `vMAJOR.MINOR.PATCH`

```
v MAJOR . MINOR . PATCH
  │        │       └── Bug fixes, minor patches (no new features)
  │        └────────── Backward-compatible improvements and features
  └─────────────────── Breaking changes or major rewrites
```

---

### Version Milestones

| Version | Label | Scope |
|---------|-------|-------|
| `v1.0.0` | Initial Release | Core email fetching, basic AI reply, SMTP send |
| `v1.1.0` | Improvements | Better AI prompts, logging, error handling |
| `v1.2.0` | Extended Features | Tagging, filtering, scheduling |
| `v2.0.0` | Major Upgrade | SaaS dashboard, multi-user support, billing |

---

### Tagging Releases

```bash
# Tag a release on main
git checkout main
git tag -a v1.0.0 -m "Initial release — basic email agent system"
git push origin v1.0.0

# List all tags
git tag -l

# View tag details
git show v1.0.0
```

---

## 4. Release Process

Every release follows a defined, repeatable workflow to ensure stability and traceability.

### Step-by-Step Release Workflow

```
[feature/* branches]
        │
        ▼
    [ dev ] ──── Test & Integrate
        │
        ▼  (All tests pass)
    [ main ] ──── Tag & Release
        │
        ▼
   v1.x.x Release
```

---

### Release Checklist

```
[ ] All feature branches merged into dev
[ ] All unit and integration tests passing on dev
[ ] README and CHANGELOG updated
[ ] Code reviewed and approved via pull request
[ ] Merge dev → main (no-fast-forward)
[ ] Version tag applied on main
[ ] Tag pushed to remote
[ ] Release notes published (GitHub Releases or equivalent)
```

---

### Commands

```bash
# Step 1 — Confirm tests pass on dev
git checkout dev
# run test suite here

# Step 2 — Merge dev into main
git checkout main
git merge --no-ff dev -m "chore: release v1.1.0"

# Step 3 — Tag the release
git tag -a v1.1.0 -m "Release v1.1.0 — performance improvements and bug fixes"

# Step 4 — Push
git push origin main
git push origin v1.1.0
```

---

## 5. Folder Change Rules

The project's folder structure enforces a clear boundary between stable core logic and experimental development.

### Folder Responsibilities

| Folder | Status | Rules |
|--------|--------|-------|
| `core/` | 🔒 Stable | Changes require review + tests. No experimental code. |
| `upgrade/` | 🧪 Experimental | Active development allowed. Not production-deployed. |
| `docs/` | 📄 Documentation | Updated with every feature or change. |
| `tests/` | ✅ Test Suite | Must reflect all changes in `core/` and `upgrade/`. |

---

### `core/` — Stable Module

- Contains production email logic: fetching, AI processing, SMTP sending.
- **No direct experimental changes.** All modifications go through `dev` and require a pull request.
- Breaking changes to `core/` require a **MAJOR version bump**.

```
core/
├── email_fetcher.py
├── ai_handler.py
├── smtp_sender.py
└── config.py
```

---

### `upgrade/` — Experimental Module

- Used for new capabilities under active development.
- Code here **must not be imported** by `core/` until it is stable and reviewed.
- Promoted to `core/` only after review, testing, and team approval.

```
upgrade/
├── dashboard/
├── bulk_sender/
└── saas_billing/
```

---

## 6. Documentation Updates

Every feature, fix, or structural change must be reflected in the project documentation before it is merged.

### Documentation Policy

> **No feature is complete without a corresponding documentation update.**

---

### What Must Be Updated

| Change Type | Files to Update |
|-------------|-----------------|
| New feature added | `README.md`, `CHANGELOG.md` |
| Bug fix | `CHANGELOG.md` |
| New CLI flag or config option | `README.md` (Usage section) |
| Folder structure changed | `README.md` (Project Structure section) |
| New version released | `CHANGELOG.md`, `VERSION` file |

---

### CHANGELOG Format

```markdown
## [v1.1.0] — 2026-04-26

### Added
- AI summarization for inbox threads
- Email tagging and category filtering

### Fixed
- SMTP login failure on expired OAuth token

### Changed
- Refactored project folder structure for clarity

### Removed
- Legacy polling mechanism replaced by push listener
```

---

## 7. Rollback Strategy

When a release introduces a critical regression or failure, the rollback procedure must be initiated immediately using `git revert`.

### Rollback Policy

- `git revert` is the **only approved rollback method** in this project.
- `git reset --hard` is **strictly prohibited** on shared branches (`main`, `dev`).
- All reverts must be committed with a `revert:` prefix message.

---

### Revert a Single Commit

```bash
# Identify the faulty commit
git log --oneline

# Revert it (creates a new commit undoing the change)
git revert <commit-hash>

# Push the revert
git push origin main
```

---

### Revert a Merged Feature Branch

```bash
# Identify the merge commit hash
git log --oneline --merges

# Revert the merge commit
# -m 1 = keep the parent branch (main) as the base
git revert -m 1 <merge-commit-hash>

# Push
git push origin main
```

---

### Rollback to a Previous Release Tag

```bash
# Create a hotfix branch from a known stable tag
git checkout -b hotfix/rollback-v1.0.0 v1.0.0

# Apply any critical-only fixes, then merge to main
git checkout main
git merge --no-ff hotfix/rollback-v1.0.0
git tag -a v1.0.1 -m "Hotfix rollback to stable v1.0.0 base"
git push origin main --tags
```

---

### Decision Tree

```
Production issue detected
        │
        ▼
Is it a single bad commit?
   ├── YES → git revert <commit-hash>
   └── NO  → Is it a bad feature merge?
                ├── YES → git revert -m 1 <merge-commit>
                └── NO  → Roll back to last stable tag
                          → git checkout -b hotfix/rollback vX.X.X
```

---
---

## 🔗 Related Documents

- 📘 [Project README](Readme.md) — Project overview and setup guide  
- 📄 [License](Project_Policies.md) — Legal usage terms  

---
## Quick Reference Card

```bash
# === BRANCHING ===
git checkout -b feature/<name> dev          # New feature branch
git checkout dev && git merge --no-ff feature/<name>  # Merge feature → dev
git checkout main && git merge --no-ff dev  # Merge dev → main (release)

# === COMMIT FORMAT ===
git commit -m "feat: add AI summarization"
git commit -m "fix: resolve SMTP login issue"
git commit -m "refactor: restructure project folders"

# === TAGGING ===
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0

# === ROLLBACK ===
git revert <commit-hash>                    # Revert a commit
git revert -m 1 <merge-commit-hash>        # Revert a merge
```

---

*This document is the single source of truth for version control practices on the AI Email Agent project. All contributors are expected to follow these guidelines without exception.*
