# backend/routers/articles.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Article
from schemas import ArticleResponse, ArticleUpdate

router = APIRouter()


@router.get("/articles", response_model=ArticleResponse)
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(Article.sort_order).all()
    data = []
    for a in articles:
        data.append({
            "id": a.id,
            "title": a.title,
            "summary": a.summary,
            "url": a.url,
            "date": str(a.date) if a.date else None,
        })
    return ArticleResponse(data=data)


@router.post("/articles", response_model=ArticleResponse)
def create_article(update: ArticleUpdate, db: Session = Depends(get_db)):
    article = Article(**update.model_dump(exclude_unset=True))
    db.add(article)
    db.commit()
    return ArticleResponse(message="Article created")


@router.put("/articles/{article_id}", response_model=ArticleResponse)
def update_article(article_id: int, update: ArticleUpdate, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(article, key, value)
    db.commit()
    return ArticleResponse(message="Article updated")


@router.delete("/articles/{article_id}", response_model=ArticleResponse)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(article)
    db.commit()
    return ArticleResponse(message="Article deleted")
