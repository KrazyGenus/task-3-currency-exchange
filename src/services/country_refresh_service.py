from ..utils.api_requests_handler import get_countries_meta, get_exchange_rate_by_country_code


async def create_country_db(country_meta_url, exchange_rate_meta_url):
    country_meta_response = await get_countries_meta(country_meta_url, exchange_rate_meta_url)
    return country_meta_response

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