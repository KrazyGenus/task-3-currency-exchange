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
        