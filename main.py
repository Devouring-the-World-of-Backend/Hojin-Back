from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    published_year: int

@app.get("/")
async def returnRootMessage():
    return {"message": "Hello, Library!"}