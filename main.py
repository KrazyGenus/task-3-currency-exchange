from fastapi import FastAPI
from dotenv import load_dotenv
import os
from src.controllers.country_controller import get_countries_meta



app = FastAPI()
load_dotenv()

@app.get('/')
async def root():
    return {'IAM': 'IAM'}


@app.post('/countries/refresh')
async def fetch_and_cache():
    country_meta_url = os.getenv("COUNTRY_META_END_POINT")
    country_meta_response = await get_countries_meta(f'{country_meta_url}')
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