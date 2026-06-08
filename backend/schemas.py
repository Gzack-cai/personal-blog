# backend/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class ResponseModel(BaseModel):
    code: int = 200
    message: str = "success"


class ProfileResponse(ResponseModel):
    data: Optional[dict] = None


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    github: Optional[str] = None
    bilibili: Optional[str] = None
    csdn: Optional[str] = None
    wechat: Optional[str] = None
    qq: Optional[str] = None


class ProjectResponse(ResponseModel):
    data: Optional[List[dict]] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    tech_stack: Optional[str] = None
    demo_url: Optional[str] = None
    github_url: Optional[str] = None
    sort_order: Optional[int] = None


class ArticleResponse(ResponseModel):
    data: Optional[List[dict]] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    url: Optional[str] = None
    date: Optional[date] = None
    sort_order: Optional[int] = None


class LifeResponse(ResponseModel):
    data: Optional[List[dict]] = None


class LifeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    date: Optional[date] = None


class FriendResponse(ResponseModel):
    data: Optional[List[dict]] = None


class FriendUpdate(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    description: Optional[str] = None
    blog_url: Optional[str] = None
    sort_order: Optional[int] = None


class ContactCreate(BaseModel):
    name: str
    email: str
    message: str


class ContactResponse(ResponseModel):
    data: Optional[dict] = None
