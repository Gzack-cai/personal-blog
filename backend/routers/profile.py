# backend/routers/profile.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Profile
from schemas import ProfileResponse, ProfileUpdate
import json

router = APIRouter()


@router.get("/profile", response_model=ProfileResponse)
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    data = {
        "id": profile.id,
        "name": profile.name,
        "title": profile.title,
        "avatar": profile.avatar,
        "bio": profile.bio,
        "skills": json.loads(profile.skills) if profile.skills else [],
        "email": profile.email,
        "phone": profile.phone,
        "github": profile.github,
        "bilibili": profile.bilibili,
        "csdn": profile.csdn,
        "wechat": profile.wechat,
        "qq": profile.qq,
    }
    return ProfileResponse(data=data)


@router.put("/profile", response_model=ProfileResponse)
def update_profile(update: ProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)
    db.commit()
    return ProfileResponse(message="Profile updated")
