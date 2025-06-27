from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.models import schema
from app.database import SessionLocal
from fastapi.templating import Jinja2Templates
from app.models.schema import Product

from app.models.schema import User, Product, Cart

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.get("/", response_class=HTMLResponse)
def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/")
def signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_exists = db.query(schema.User).filter(schema.User.email == email).first()
    if user_exists:
        return HTMLResponse("<h3>Email already registered.</h3>")
    new_user = schema.User(name=name, email=email, password=password)
    db.add(new_user)
    db.commit()
    return RedirectResponse("/signin", status_code=303)



@router.get("/signin", response_class=HTMLResponse)
def signin_form(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})


@router.post("/signin")
def signin(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(schema.User).filter(schema.User.email == email).first()
    if not user or user.password != password:
        return HTMLResponse("<h3>Invalid credentials</h3>", status_code=401)

    # Redirect to profile using user ID (no session/JWT used)
    if user.is_admin:
        return RedirectResponse(url="/admin/dashboard", status_code=302)
    else:
        return RedirectResponse(url=f"/profile/{user.id}", status_code=302)



@router.get("/profile/{user_id}", response_class=HTMLResponse)
def profile(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    products = db.query(Product).all()

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
        "cart_items": cart_items,
        "products": products
    })


@router.post("/profile/{user_id}/bio")
def update_bio(user_id: int, bio: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(schema.User).filter(schema.User.id == user_id).first()
    if user:
        user.bio = bio
        db.commit()
    return RedirectResponse(url=f"/profile/{user_id}", status_code=303)

@router.get("/logout", response_class=HTMLResponse)
def logout():
    # No session to clear — simply redirect to login page
    return RedirectResponse(url="/signin", status_code=303)




def seed_products():
    db = SessionLocal()
    if db.query(Product).count() == 0:
        shoes = [
            Product(name="Nike Air Max", price=9999, description="Lightweight running shoes."),
            Product(name="Adidas Ultraboost", price=11999, description="Comfort and performance."),
            Product(name="Puma RS-X", price=8499, description="Stylish and durable."),
        ]
        db.add_all(shoes)
        db.commit()
    db.close()
