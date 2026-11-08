from fastapi import FastAPI
import uvicorn
from src.core.config import settings

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=settings.port, reload=True)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}