from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import SessionLocal
from . import crud, schemas

async def get_db():
    async with SessionLocal() as session:
        yield session

app = FastAPI()

@app.post("/swipe/")
async def swipe(swipe: schemas.SwipeCreate, db: AsyncSession = Depends(get_db)):
    return await crud.handle_swipe(swipe, db)
