from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str]
    published_year: int
    
    @validator("published_year")
    def checkFutureDate(cls, publishedDate):
        currentDate = datetime.now().year
        if publishedDate > currentDate :
            raise ValueError("Published Year is Later than Present Year!")
        return publishedDate

bookDB: List[Book] = []

@app.post("/books", response_model=Book)
async def createBook(book: Book):
    if book.id in [single.id for single in fakeDB]:
        raise HTTPException(status_code=400, detail="Book Already Exists!")
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

@app.exception_handler(HTTPException)
async def httpExceptionHandler(request, execution):
    return JSONResponse(status_code=execution.status_code, content={"message": execution.detail})



client = TestClient(app)

def printBookTest():
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == {"message": "Book Not Found"}

def noBookTest():
    response = client.get("/books/100")
    assert response.status_code == 404
    assert response.json() == {"message": "Book Not Found"}

def createBookTest():
    new_book = {
        "id": 142,
        "title": "Hello",
        "author": "Han Hojin",
        "description": "This is a Test.",
        "published_year": 2024
    }

def createWrongBookTest():
    existing_book = fakeDB[0]
    response = client.post("/books", json=existing_book)
    assert response.status_code == 400

def updateBookTest():
    take_book = {
        "id": fakeDB[0].id,
        "title": "Goodbye",
        "author": "Ham Hojin",
        "description": "This is a Modified Test.",
        "published_year": 2004
    }
    response = client.put(f"/books/{take_book['id']}", json=take_book)
    assert response.status_code == 200
    assert response.json() == take_book

def updateWrongBookTest():
    test_id = 1428
    response = client.put(f"/books/{test_id}", json={"id": test_id})
    assert response.status_code == 404

def removeBookTest():
    removed_book = fakeDB[0]
    response = client.delete(f"/books/{removed_book.id}")
    assert response.status_code == 200
    assert response.json == {"message": "Selected Book Deleted!"}

def removeWrongBookTest():
    remove_wrong_book = 1429
    response = client.delete(f"/books/{remove_wrong_book}")
    assert response.status_code == 404



@app.get("/")
async def returnRootMessage():
    return {"message": "Hello, Library!"}