from ..utils.api_requests_handler import get_countries_meta
from ..utils.image_generation import generate_summary_image
from ..models.models import Country
from .database_service import upsert_country_data
from sqlalchemy import select, func

# store the country payload to the db
async def create_country_db(country_meta_url, exchange_rate_meta_url, db_session):
    top_5_gdp_countries_raw = None
    new_objects = []
    country_meta_response = await get_countries_meta(country_meta_url, exchange_rate_meta_url)
    print(country_meta_response)
    for country in country_meta_response:
        new_entry = Country(**country)
        print("New entry", new_entry)
        new_objects.append(new_entry)
    print(new_objects)
    country_count = await upsert_country_data(db_session, new_objects)
    if country_count > 0:
        top_5_gdp_countries_raw = (
            await db_session.execute(
                select(Country.name, Country.estimated_gdp)
                .order_by(Country.estimated_gdp.desc())
                .limit(5)
            )
        ).all()
    top_5_gdp_countries = [{"name": name, "estimated_gdp": estimated_gdp} for name, estimated_gdp in top_5_gdp_countries_raw]
    print(top_5_gdp_countries)
    last_refresh_time_stamp = await db_session.scalar(select(func.max(Country.last_refreshed_at)))
    print(last_refresh_time_stamp)
    await generate_summary_image(country_count, top_5_gdp_countries, last_refresh_time_stamp)
        




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