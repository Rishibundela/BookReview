from fastapi import FastAPI, APIRouter
from src.books.routes import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app:FastAPI):
  print(f"server is starting ... ")
  await init_db()
  yield
  print(f"server has been stopped ... ") 


# Internal release version (for your team)
API_RELEASE = "0.1.0" 

# Public URL version (for the users)
API_ROUTE_VERSION = "v1"

app = FastAPI(
  title="Bookly API",
  version=API_RELEASE, 
  description="A simple REST API for a book review web service built with FastAPI",
)

# 1. Create a "v1" Master Router
v1_router = APIRouter(prefix=f"/api/{API_ROUTE_VERSION}")

# 2. Add your specific resource routers to the Master Router
# (Inside book_router, the prefix should just be "/books")
v1_router.include_router(book_router, prefix="/books", tags=["Books"])
v1_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

# 3. Include only the Master Router in your main app
app.include_router(v1_router)
