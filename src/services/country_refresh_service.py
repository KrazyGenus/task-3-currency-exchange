import httpx
from dotenv import load_dotenv
import os

load_dotenv()

async def get_countries_meta(country_meta_url:str):
    async with httpx.AsyncClient() as country_meta:
        country_response = await country_meta.get(f'{country_meta_url}')
        
        return country_response.json
    

async def get_exchange_rate_by_country_code():
    async with httpx.AsyncClient() as exchange_meta:
        exchange_meta_url = os.getenv("EXCHANGE_RATE_META_ENDPOINT")
        response = await exchange_meta.get(f'{exchange_meta_url}{'COUNTRY_CODE'}')


async def create_country_db():
    pass

async def fetch_country_db_filtering():
    pass

async def fetch_country_by_name():
    pass

async def delete_country_by_name():
    pass
    
    
async def db_country_table_status():
    pass

async def fetch_country_image_summary():
    pass