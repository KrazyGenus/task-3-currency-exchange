from ..utils.api_requests_handler import get_countries_meta
from ..utils.image_generation import generate_summary_image
from ..models.models import Country
from .database_service import upsert_country_data
from sqlalchemy import select, func, and_, delete
from fastapi import HTTPException, status
from datetime import datetime




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
        




async def get_filtered_countries(query_payload, db_session):
    base_selection = select(Country)
    sort_map = {
        "gdp_desc": Country.estimated_gdp.desc(),
        "gdp_asc": Country.estimated_gdp.asc(),
        "name_asc": Country.name.asc(),
        "name_desc": Country.name.desc()
    }
    
    
    if "region" in query_payload:
        region_value = query_payload.get("region").strip()
        base_selection = base_selection.where(Country.region.ilike(f"{region_value}"))
    
    if "currency" in query_payload:
        currency_value = query_payload.get("currency").strip()
        base_selection = base_selection.where(Country.currency_code.ilike(f"{currency_value}"))
    
    if "sort" in query_payload:
        sort_value = query_payload.get("sort").strip()
        if sort_value in sort_map:
            base_selection = base_selection.order_by(sort_map[sort_value])
    result = await db_session.execute(base_selection)
    filtered_countries = result.scalars().all()

    return filtered_countries
        
        
async def find_country_by_name(country_name:str, db_session):
    base_selection = select(Country)
    country_name = country_name.strip()
    base_selection = base_selection.where(Country.name.ilike(f"{country_name}"))
    country_payload = await db_session.execute(base_selection)
    result = country_payload.scalars().all()
    return result



async def delete_country_by_name(country_name:str, db_session):
    country_name = country_name.strip()
    try:
        delete_selection = (delete(Country).where(Country.name.ilike(f"{country_name}")))
        result = await db_session.execute(delete_selection)
        await db_session.commit()
    except Exception as e:
        print(e)
    
async def db_country_status(db_session):
    try:
        count = await db_session.scalar(select(func.count(Country.id)))
        if count > 0:
            count += 1
        last_refresh_time_stamp = await db_session.scalar(select(func.max(Country.last_refreshed_at)))
        return {
            "total_countries": int(count),
            "last_refreshed_at": last_refresh_time_stamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    except Exception as e:
        print(e)