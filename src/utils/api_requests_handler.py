import httpx
from dotenv import load_dotenv
import os
load_dotenv()


async def process_payload(payload, exchange_rate_meta_url):
    print('Exchange rate url', exchange_rate_meta_url)
    for country in payload:
        if country.get("currencies"):    
            print(await get_exchange_rate_by_country_code(exchange_rate_meta_url, country.get("currencies")[0].get("code")))
        
async def get_countries_meta(country_meta_url:str, exchange_rate_meta_url:str):
    async with httpx.AsyncClient() as country_meta:
        country_response = await country_meta.get(f'{country_meta_url}')
        
        processed_response = await process_payload(country_response.json(), exchange_rate_meta_url)
        #return processed_response

async def get_exchange_rate_by_country_code(exchange_rate_meta_url, currency_code):
    async with httpx.AsyncClient() as exchange_meta:
        # exchange_meta_url = os.getenv("EXCHANGE_RATE_META_ENDPOINT")
        response = await exchange_meta.get(f'{exchange_rate_meta_url}{currency_code}')
        print(response.json())



