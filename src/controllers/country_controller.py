from ..services.country_refresh_service import create_country_db, get_filtered_countries, find_country_by_name, delete_country_by_name, db_country_status
async def create_country(country_meta_url, exchange_rate_meta_url, db_session):
    create_meta_response = await create_country_db(country_meta_url, exchange_rate_meta_url, db_session)
    return create_meta_response
    


async def get_country_by_filtering(query_params_payload, db_session):
    query_payload = await get_filtered_countries(query_params_payload, db_session)
    return query_payload


async def get_country_by_name(country_name:str, db_session):
    found_country_meta = await find_country_by_name(country_name, db_session)
    return found_country_meta


async def delete_country(country_name:str, db_session):
    try:
        await delete_country_by_name(country_name, db_session)
    except Exception as e:
        raise print(e)


async def get_table_status(db_session):
    try:
        status = await db_country_status(db_session)
        return status
    except Exception as e:
        raise print(e)


async def get_summary_image():
    pass