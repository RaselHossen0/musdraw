from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True)
    scores = relationship("Score", back_populates="user")  # Ensure this is properly defined
    messages = relationship("Message", back_populates="user")

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(255), unique=True)
class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey('words.id'))
    active = Column(Boolean, default=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    word = relationship("Word")
    player_count = Column(Integer, default=1)  # Default to 1 for the game creator
    messages = relationship("Message", back_populates="game")
    scores = relationship("Score", back_populates="game")


class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    score = Column(Integer, default=0)
    user = relationship("User", back_populates="scores")
    game = relationship("Game", back_populates="scores")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    content = Column(String(1024), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="messages")
    game = relationship("Game", back_populates="messages")
