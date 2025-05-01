from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"
    id         = Column(Integer, primary_key=True)
    pr_number  = Column(Integer, nullable=False)
    repo_full  = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Comment(Base):
    __tablename__ = "comments"
    id         = Column(Integer, primary_key=True)
    review_id  = Column(Integer, nullable=False)
    file_path  = Column(String, nullable=False)
    line       = Column(Integer, nullable=False)
    message    = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
