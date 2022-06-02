
from typing import List
from fastapi import FastAPI, Query
from app.routers import recipes

app = FastAPI(
    title="Recipes API"
)

@app.get("/")
def root()->dict:
    return{"message": "Hello!"}


@app.get("/items/")
def read_items(q: List[int] = Query(None)):
    return {"q": q}

app.include_router(recipes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main.app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )
