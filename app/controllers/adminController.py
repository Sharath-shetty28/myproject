# app/controllers/adminController.py

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.schema import User
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard")
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "users": users
    })
