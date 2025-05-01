import requests, os
from openai import OpenAI
from github import Github, GithubIntegration
from sqlalchemy.orm import sessionmaker
from models import Base, Review, Comment
from sqlalchemy import create_engine
from config import *

# Initialize GitHub Integration
git_integration = GithubIntegration(GITHUB_APP_ID, GITHUB_PRIVATE_KEY)
# Initialize OpenAI client
ai = OpenAI(api_key=OPENAI_API_KEY)

# Database setup
engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def analyze_pr(repo_full_name, pr_number):
    # Authenticate as App installation
    installation = git_integration.get_installation(repo_full_name.split("/")[0], repo_full_name.split("/")[1])
    token = git_integration.get_access_token(installation.id).token
    gh = Github(token)

    repo = gh.get_repo(repo_full_name)
    pr   = repo.get_pull(pr_number)
    files = pr.get_files()

    session = Session()
    review = Review(pr_number=pr_number, repo_full=repo_full_name)
    session.add(review); session.commit()

    for f in files:
        for hunk in f.patch.split("\n"):
            if hunk.startswith("+") and not hunk.startswith("+++"):
                prompt = f"Review this code snippet for potential issues:\n```python\n{hunk[1:]}\n```"
                response = ai.chat.completions.create(model=LLM_MODEL, messages=[{"role":"user","content":prompt}])
                message = response.choices[0].message.content.strip()
                if message:
                    pr.create_review_comment(body=message, commit_id=pr.head.sha,
                                              path=f.filename, position=1)
                    comment = Comment(review_id=review.id, file_path=f.filename,
                                      line=0, message=message)
                    session.add(comment)
    session.commit()
    session.close()
