import os

GITHUB_APP_ID       = os.getenv("GITHUB_APP_ID")
GITHUB_PRIVATE_KEY  = os.getenv("GITHUB_PRIVATE_KEY_PEM")
OPENAI_API_KEY      = os.getenv("OPENAI_API_KEY")
LLM_MODEL           = os.getenv("LLM_MODEL", "gpt-4")  # or self-hosted like "codellama-34b"
DATABASE_URL        = os.getenv("DATABASE_URL", "sqlite:///reviews.db")
