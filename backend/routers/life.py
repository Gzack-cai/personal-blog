# backend/routers/life.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import LifeMoment
from schemas import LifeResponse, LifeUpdate

router = APIRouter()


@router.get("/life", response_model=LifeResponse)
def get_life_moments(db: Session = Depends(get_db)):
    moments = db.query(LifeMoment).order_by(LifeMoment.date.desc()).all()
    data = []
    for m in moments:
        data.append({
            "id": m.id,
            "title": m.title,
            "content": m.content,
            "image": m.image,
            "date": str(m.date) if m.date else None,
        })
    return LifeResponse(data=data)


@router.post("/life", response_model=LifeResponse)
def create_life_moment(update: LifeUpdate, db: Session = Depends(get_db)):
    moment = LifeMoment(**update.model_dump(exclude_unset=True))
    db.add(moment)
    db.commit()
    return LifeResponse(message="Life moment created")


@router.put("/life/{moment_id}", response_model=LifeResponse)
def update_life_moment(moment_id: int, update: LifeUpdate, db: Session = Depends(get_db)):
    moment = db.query(LifeMoment).filter(LifeMoment.id == moment_id).first()
    if not moment:
        raise HTTPException(status_code=404, detail="Life moment not found")
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(moment, key, value)
    db.commit()
    return LifeResponse(message="Life moment updated")


@router.delete("/life/{moment_id}", response_model=LifeResponse)
def delete_life_moment(moment_id: int, db: Session = Depends(get_db)):
    moment = db.query(LifeMoment).filter(LifeMoment.id == moment_id).first()
    if not moment:
        raise HTTPException(status_code=404, detail="Life moment not found")
    db.delete(moment)
    db.commit()
    return LifeResponse(message="Life moment deleted")
