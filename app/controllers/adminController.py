# app/controllers/adminController.py

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.schema import User ,Product
from fastapi.responses import  RedirectResponse
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

@router.get("/products/add")
def show_add_product_form(request: Request):
    return templates.TemplateResponse("admin_add_product.html", {"request": request})


@router.post("/products/add")
async def add_product(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    name = form.get("name")
    price = float(form.get("price"))

    new_product = Product(name=name, price=price)
    db.add(new_product)
    db.commit()
    return RedirectResponse(url="/", status_code=302)
