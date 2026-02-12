from fastapi import FastAPI, Header, Query, Path 
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# ---------- Example of a path parameter
# @app.get("/greet/{name}")
# async def greet(name: str) -> dict:
#     return {"message": f"Hello {name}!"}

# ---------- Example of a query parameter
# @app.get("/greet")
# async def greet(name: str, age: int) -> dict:
#     return {"message": f"Hello {name}! You are {age} years old."}

@app.get("/greet")
async def greet(name: Optional[str] = 'User', age: int = 0) -> dict:
    return {"message": f"Hello {name}! You are {age} years old."}

class BookCreatModel(BaseModel):
    title: str
    author: str

# ---------- Example of a POST endpoint with a request body(Serialization)
@app.post("/books")
async def create_book(book_data: BookCreatModel) -> dict:
    return {"message": f"Book '{book_data.title}' by {book_data.author} created successfully."} 

# ---------- Example of using Header parameters
@app.get("/headers",status_code=201)
async def read_headers(
    accept : Optional[str] = Header(None),
    content_type: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
    host: Optional[str] = Header(None)
    ):
    request_headers = {
        "Accept": accept,
        "Content-Type": content_type,
        "User-Agent": user_agent,
        "Host": host
    }
    return request_headers