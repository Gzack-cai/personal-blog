# backend/routers/projects.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Project
from schemas import ProjectResponse, ProjectUpdate
import json

router = APIRouter()


@router.get("/projects", response_model=ProjectResponse)
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.sort_order).all()
    data = []
    for p in projects:
        data.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "image": p.image,
            "tech_stack": json.loads(p.tech_stack) if p.tech_stack else [],
            "demo_url": p.demo_url,
            "github_url": p.github_url,
            "sort_order": p.sort_order,
        })
    return ProjectResponse(data=data)


@router.post("/projects", response_model=ProjectResponse)
def create_project(update: ProjectUpdate, db: Session = Depends(get_db)):
    project = Project(**update.model_dump(exclude_unset=True))
    db.add(project)
    db.commit()
    return ProjectResponse(message="Project created")


@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, update: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    return ProjectResponse(message="Project updated")


@router.delete("/projects/{project_id}", response_model=ProjectResponse)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return ProjectResponse(message="Project deleted")
