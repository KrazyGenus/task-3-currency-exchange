from fastapi import FastAPI, Depends, Request, HTTPException, status
from starlette.responses import FileResponse
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import os
from src.config.database import get_async_db
from src.controllers.country_controller import create_country, get_country_by_filtering, get_country_by_name, delete_country, get_table_status, get_summary_image
from src.config.database import Base, async_engine
from contextlib import asynccontextmanager
from src.schema.schema import CountrySchema
from typing import List



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Attempting a synchronous database table creation")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    print("Database schema created") 


app = FastAPI(lifespan=lifespan)
load_dotenv()



@app.post('/countries/refresh', status_code=200)
async def fetch_and_cache(db_session: AsyncSession = Depends(get_async_db)):
    country_meta_url = os.getenv("COUNTRY_META_END_POINT")
    exchange_rate_meta_url = os.getenv("EXCHANGE_RATE_META_ENDPOINT")
    print("DB", db_session)
    await create_country(country_meta_url, exchange_rate_meta_url, db_session)


@app.get('/countries', response_model=List[CountrySchema], status_code=200)
async def filter_by_query(request: Request, db_session: AsyncSession = Depends(get_async_db)):
    valid_query_fields = ["region", "currency", "sort"]
    """
    The query parameter supported are as follows:
        - region=Africa |
        - currency=NGN |
        - sort=gdp_desc
    """
    query_params = request.query_params
    for key, values in query_params.items():
        if key not in valid_query_fields:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid query parameter: {key}")
    filtered_payload = await get_country_by_filtering(query_params, db_session)
    return filtered_payload


@app.get('/countries/image')
async def summary_image():
    image_url = await get_summary_image()
    return FileResponse(
        path = image_url,
        media_type='image/png',
    )




@app.get('/countries/{name}', response_model=List[CountrySchema], status_code=200)
async def get_by_name(name: str, db_session: AsyncSession = Depends(get_async_db)):
    if name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name cannot be empty")
    else:
        country_payload = await get_country_by_name(name, db_session)
        return country_payload

@app.delete('/countries/{name}', status_code=200)
async def delete_by_name(name:str, db_session: AsyncSession = Depends(get_async_db)):
    print("Delete: ", name)
    if name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name cannot be empty")
    else:
        try:
            country_payload = await delete_country(name, db_session)
            if country_payload is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= { "error": "Country not found"})
            print(country_payload)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= { "error": "Country not found"})



@app.get('/status', status_code=200)
async def get_status(db_session: AsyncSession = Depends(get_async_db)):
    current_status = await get_table_status(db_session)
    return current_status


    