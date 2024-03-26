from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def returnRootMessage():
    return {"message": "Hello, Library!"}