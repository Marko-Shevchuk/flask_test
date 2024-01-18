from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum as Enumeration, DateTime
from sqlalchemy.sql import func

from enum import Enum

class Satisfaction(Enum):
    AWESOME = 'AWESOME'
    GOOD = 'GOOD'
    NEUTRAL = 'NEUTRAL'
    BAD = 'BAD'
    HORRIBLE = 'HORRIBLE'

class Feedback(db.Model):
    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    feedback: Mapped[str] = mapped_column(String, nullable=True)
    satisfaction: Mapped[str] = mapped_column(Enumeration(Satisfaction), nullable=False)
    user: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), nullable=False)
