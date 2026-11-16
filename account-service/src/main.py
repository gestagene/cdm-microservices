from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.core.db import get_db
import uvicorn
from src.core.config import settings

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=settings.port, reload=True)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#check database connection
@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    row = db.execute(text("SELECT current_user, current_database()")).one()
    return {"user": row[0], "database": row[1]}