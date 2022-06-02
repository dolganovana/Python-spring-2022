
from typing import List
from fastapi import FastAPI, Query
import recipes

app = FastAPI(
    title="Recipes API"
)

@app.get("/")
def root()->dict:
    return{"message": "Hello!"}

app.include_router(recipes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main.app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )
