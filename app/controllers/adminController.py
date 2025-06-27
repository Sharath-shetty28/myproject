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

# adminController.py

@router.get("/products")
def admin_view_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    users = db.query(User).all()
    return templates.TemplateResponse("admin_products.html", {"request": request, "products": products})


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
    return RedirectResponse(url="/admin/dashboard", status_code=302)

@router.get("/products/edit/{product_id}")
def edit_product_form(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    return templates.TemplateResponse("admin_edit_product.html", {"request": request, "product": product})

@router.post("/products/edit/{product_id}")
async def update_product(product_id: int, request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    name = form.get("name")
    price = float(form.get("price"))

    product = db.query(Product).get(product_id)
    product.name = name
    product.price = price

    db.commit()
    return RedirectResponse(url="/admin/products", status_code=302)

@router.post("/products/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if product:
        db.delete(product)
        db.commit()
    return RedirectResponse(url="/admin/products", status_code=302)
