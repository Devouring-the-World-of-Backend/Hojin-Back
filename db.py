from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import hashlib

async_engine = create_async_engine('sqlite+aiosqlite:///./testdb.db', echo=True)
Base = declarative_base()

async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

class booklib(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)

class userdb(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    userid = Column(String)
    passwd = Column(String)

Base.metadata.create_all(engine)



app = FastAPI()

@app.get("/books/", response_model=List[booklib])
async def read_books():
    async with async_session():
        async with async_session().begin():
            result = await session.execute(select(booklib))
            books = result().scalars().all()
            return books


# CREATE
hasher = hashlib.sha256()
hasher.update("qwer1234".encode("utf-8"))
temp_pass = hasher.hexdigest()

create_book = booklib(title="testdata Book", author="Han Hojin")
create_user = userdb(name="Han Hojin", email="winterval.kor@gmail.com", userid="seupjak", passwd=temp_pass)
session.add(create_book)
session.add(create_user)
session.commit()

# READ
read_book_data = session.query(booklib).all()
for data in read_book_data:
    print(book.title, book.author)

# UPDATE
update_book_data = session.query(booklib).filter_by(title="testdata Book").first()
update_book_data.title = "pwned"
update_book_data.author = "0xdeadbeef"
session.commit()

# DELETE
delete_book_from_table = session.query(booklib).filter_by(title="pwned").first()
session.delete(delete_book_from_table)
session.commit()