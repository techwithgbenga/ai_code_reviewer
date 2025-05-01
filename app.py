from flask import Flask, request, jsonify, render_template
from review_engine import analyze_pr
from config import *
from models import Base, Review, Comment
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.json
    if payload.get("action") == "opened" and payload.get("pull_request"):
        repo = payload["repository"]["full_name"]
        pr_number = payload["pull_request"]["number"]
        analyze_pr(repo, pr_number)
    return "", 204

@app.route("/")
def index():
    session = Session()
    reviews = session.query(Review).order_by(Review.created_at.desc()).all()
    return render_template("dashboard.html", reviews=reviews)

@app.route("/review/<int:review_id>")
def review_details(review_id):
    session = Session()
    comments = session.query(Comment).filter_by(review_id=review_id).all()
    return render_template("review.html", comments=comments)
