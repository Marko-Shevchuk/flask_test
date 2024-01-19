from enum import Enum

from sqlalchemy import Integer, String, Enum as Enumeration, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app import db

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class PostType(Enum):
    NEWS = "NEWS"
    PUBLICATION = "PUBLICATION"
    OTHER = "OTHER"


class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    text: Mapped[str] = mapped_column(String(256), nullable=False)
    image: Mapped[str] = mapped_column(String(256), server_default='pdefault.png')
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    type: Mapped[str] = mapped_column(Enumeration(PostType), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'), nullable=False)
    tags = relationship('Tag', secondary=post_tags, backref='posts')
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status.name
        }