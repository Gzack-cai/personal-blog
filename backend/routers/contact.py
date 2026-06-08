# backend/routers/contact.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ContactMessage
from schemas import ContactCreate, ContactResponse

router = APIRouter()


@router.post("/contact", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    message = ContactMessage(**contact.model_dump())
    db.add(message)
    db.commit()
    return ContactResponse(message="Message sent successfully")


@router.get("/contact", response_model=ContactResponse)
def get_contacts(db: Session = Depends(get_db)):
    messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    data = []
    for m in messages:
        data.append({
            "id": m.id,
            "name": m.name,
            "email": m.email,
            "message": m.message,
            "created_at": str(m.created_at),
        })
    return ContactResponse(data=data)


@router.delete("/contact/{message_id}", response_model=ContactResponse)
def delete_contact(message_id: int, db: Session = Depends(get_db)):
    message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(message)
    db.commit()
    return ContactResponse(message="Message deleted")
