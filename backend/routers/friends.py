# backend/routers/friends.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Friend
from schemas import FriendResponse, FriendUpdate

router = APIRouter()


@router.get("/friends", response_model=FriendResponse)
def get_friends(db: Session = Depends(get_db)):
    friends = db.query(Friend).order_by(Friend.sort_order).all()
    data = []
    for f in friends:
        data.append({
            "id": f.id,
            "name": f.name,
            "avatar": f.avatar,
            "description": f.description,
            "blog_url": f.blog_url,
        })
    return FriendResponse(data=data)


@router.post("/friends", response_model=FriendResponse)
def create_friend(update: FriendUpdate, db: Session = Depends(get_db)):
    friend = Friend(**update.model_dump(exclude_unset=True))
    db.add(friend)
    db.commit()
    return FriendResponse(message="Friend created")


@router.put("/friends/{friend_id}", response_model=FriendResponse)
def update_friend(friend_id: int, update: FriendUpdate, db: Session = Depends(get_db)):
    friend = db.query(Friend).filter(Friend.id == friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(friend, key, value)
    db.commit()
    return FriendResponse(message="Friend updated")


@router.delete("/friends/{friend_id}", response_model=FriendResponse)
def delete_friend(friend_id: int, db: Session = Depends(get_db)):
    friend = db.query(Friend).filter(Friend.id == friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")
    db.delete(friend)
    db.commit()
    return FriendResponse(message="Friend deleted")
