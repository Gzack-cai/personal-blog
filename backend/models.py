# backend/models.py
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, func
from database import Base


class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    avatar = Column(String(500))
    bio = Column(Text)
    skills = Column(Text, comment="JSON array")
    email = Column(String(200))
    phone = Column(String(50))
    github = Column(String(500))
    bilibili = Column(String(500))
    csdn = Column(String(500))
    wechat = Column(String(200))
    qq = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    image = Column(String(500))
    tech_stack = Column(Text, comment="JSON array")
    demo_url = Column(String(500))
    github_url = Column(String(500))
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    summary = Column(Text)
    url = Column(String(500), nullable=False)
    date = Column(Date)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())


class LifeMoment(Base):
    __tablename__ = "life_moments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200))
    content = Column(Text)
    image = Column(String(500))
    date = Column(Date)
    created_at = Column(DateTime, default=func.now())


class Friend(Base):
    __tablename__ = "friends"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    avatar = Column(String(500))
    description = Column(Text)
    blog_url = Column(String(500), nullable=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())


class ContactMessage(Base):
    __tablename__ = "contact_messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
