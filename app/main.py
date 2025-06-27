#uvicorn app.main:app --reload

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.controllers import authController #✅ This tells Python to look relative to the current package (. = current folder = app/)
from app.database import engine
from .models import schema
from app.controllers.authController import seed_products
import os
from app.controllers import cart_controller
from app.controllers import adminController


# Create tables
schema.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Static and routing
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(authController.router)
seed_products()
app.include_router(cart_controller.router)

app.include_router(adminController.router, prefix="/admin")

