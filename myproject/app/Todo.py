from enum import Enum

from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum as SQLEnum


class Status(Enum):
    TODO = 'Todo'
    IN_PROGRESS = 'In progress'
    DONE = 'Done'

    @staticmethod
    def get_dropdown_values():
        return [(status.name, status.value) for status in Status]


class Task(db.Model):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(SQLEnum(Status), nullable=False, default=Status.TODO)