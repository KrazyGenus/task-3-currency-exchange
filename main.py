from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import os
from src.config.database import get_async_db
from src.controllers.country_controller import create_country
from src.config.database import Base, async_engine
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Attempting a synchronous database table creation")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    print("Database schema created") 


app = FastAPI(lifespan=lifespan)
load_dotenv()

@app.post('/countries/refresh')
async def fetch_and_cache(db_session: AsyncSession = Depends(get_async_db)):
    country_meta_url = os.getenv("COUNTRY_META_END_POINT")
    exchange_rate_meta_url = os.getenv("EXCHANGE_RATE_META_ENDPOINT")
    print("DB", db_session)
    country_meta_response = await create_country(country_meta_url, exchange_rate_meta_url, db_session)
    return country_meta_response


@app.get('/countries')

@app.get('/countries/{name}')
async def get_by_name():
    pass

@app.delete('/countries/{name}')
async def delete_by_name():
    pass

@app.get('status')
async def get_status():
    pass

@app.get('/countries/image')
async def summary_image():
    pass