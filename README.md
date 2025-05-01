# AI-Powered Code Review Bot

## Overview
AI-driven code review tools have surged in popularity, with services like CodeRabbit offering open-source tiers for free GitHub/GitLab integration and Sourcery providing instant feedback across 30+ languages. Community-built apps (e.g., GitPack-AI) showcase Django-based GitHub Apps that post line-by-line reviews, while emerging open-source projects like Qodo’s PR-Agent demonstrate AI feedback directly on PRs. Cutting-edge research (e.g., Bugdar) illustrates the power of Retrieval-Augmented Generation for context-aware feedback in under a minute per request. Our project brings these concepts together in a self-hosted, extensible Python tool.

## Features & Motivation
- Automated PR Analysis
 On each new pull request, fetch changed files and use an LLM to identify bugs, style issues, or optimization opportunities.

- Inline Comments
 Post contextual suggestions directly on diff hunks via the GitHub Checks API, emulating human reviewers.

- Configurable Rules
 Allow teams to enable/disable specific review types (e.g., security, performance, docstring checks).

- Self-Hosted & Extensible
 Can run as a GitHub App or via GitHub Actions; supports local LLMs (e.g., Code Llama) or cloud APIs.

- Web Dashboard
 Flask app to view review history, aggregate metrics (e.g., average comment count), and adjust settings.

## High-Level Architecture
```bash
flowchart LR
  PR[New Pull Request]
  GH_API[GitHub API] --> Bot{Review Bot}
  Bot --> LLM[LLM / OpenAI API]
  LLM --> Bot
  Bot --> GH_API
  Bot --> DB[(SQLite)]
  Bot --> Dashboard[Flask UI]
```

- Webhook Listener (Flask) receives pull_request events.
- Review Engine fetches diffs via GitHub API, chunks them, and calls the LLM for critique.
- Comments are posted back to GitHub as review comments.
- Storage logs verdicts and metrics in SQLite (via SQLAlchemy).
- Dashboard shows past reviews and allows rule toggling.

## Usage & Deployment
```bash
# Install dependencies
pip install fastapi flask PyGithub openai sqlalchemy

# Configure environment
Set GITHUB_APP_ID, GITHUB_PRIVATE_KEY_PEM, and OPENAI_API_KEY in your environment.

# Run Flask server
flask run --port 5000

# Register GitHub App
- Create a GitHub App with webhook pointing to /webhook.
- Grant repo and pull-request permissions.
- Install the app on desired repositories.
```

## Why & Next Steps
- **Speed & Consistency:** Accelerate reviews and reduce human bias.
- **Security:** Automate vulnerability hints using RAG approaches like Bugdar.
- **Extensibility:** Swap out LLM_MODEL to use local models (e.g., Code Llama) or adapt prompts for domain-specific rules.

Future enhancements might include Slack notifications, audit dashboards, or integration with CI pipelines as a GitHub Action.

Pull requests, feature requests, and community contributions are welcome. Let’s build the next generation of AI-augmented code reviews!

