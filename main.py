from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str]
    published_year: int

bookDB: List[Book] = []

@app.post("/books", response_model=Book)
async def createBook(book: Book):
    bookDB.append(book)
    return book

@app.get("/books", response_model=List[Book])
async def printBookList():
    return bookDB

@app.get("/books/{book_id}", response_model=Book)
async def printSingleBook(book_id: int):
    for book in bookDB:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book Not Found")

@app.put("/books/{book_id}", response_model=Book)
async def updateBook(book_id: int, book: Book):
    for i, book in enumerate(bookDB):
        if book.id == book_id:
            bookDB[i] = book
            return book
    raise HTTPException(status_code=404, detail="Book Not Found")

@app.delete("/books/{book_id}")
async def removeBook(book_id: int):
    for i, book in enumerate(bookDB):
        del bookDB[i]
        return {"message": "Selected Book Deleted!"}
    raise HTTPException(status_code=404, detail="Book Not Found")

@app.get("/")
async def returnRootMessage():
    return {"message": "Hello, Library!"}