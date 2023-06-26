from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, func, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(20), nullable=False)
    content = Column(String(120), nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_on = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    owner_id = Column(ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    owner = relationship('User')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(30), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    created_on = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())


class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    post_id = Column(Integer, ForeignKey(
        'posts.id', ondelete='CASCADE'), nullable=False, primary_key=True)
