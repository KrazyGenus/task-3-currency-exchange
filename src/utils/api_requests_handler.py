import httpx
from dotenv import load_dotenv
import os
import random
from datetime import datetime, timezone
from fastapi import HTTPException, status

load_dotenv()


            
async def get_countries_meta(country_meta_url:str, exchange_rate_meta_url:str):
    dt_object = datetime.now(timezone.utc)
    formatted_str = dt_object.strftime("%Y-%m-%dT%H:%M:%SZ")
    complete_payload = []
    json_country_response = None
    try:
        async with httpx.AsyncClient() as country_meta:
            country_response = await country_meta.get(f'{country_meta_url}')
            json_country_response = country_response.json()
    except (httpx.ConnectError, httpx.TimeoutException):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail= { 
                "error": "External data source unavailable",
                "details": f"Could not fetch data from {country_meta_url}"
            })
       
    for country in json_country_response:
        parsed_dict = {}
        parsed_dict["name"] = country.get("name")
        parsed_dict["capital"] = country.get("capital")
        parsed_dict["region"] = country.get("region")
        parsed_dict["population"] = country.get("population")
        if country.get("currencies"):
            exchange_rate = await get_exchange_rate_by_country_code(exchange_rate_meta_url, country.get("currencies")[0].get("code"))
            if not exchange_rate.get("rates"):

                parsed_dict["currency_code"] = country.get("currencies")[0].get("code")
                parsed_dict["exchange_rate"] = 0
                parsed_dict["estimated_gdp"] = 0
                parsed_dict["flag_url"] = country.get("flag")
                parsed_dict["last_refreshed_at"] = dt_object
                complete_payload.append(parsed_dict)
            else:
                parsed_dict["currency_code"] = country.get("currencies")[0].get("code")
                parsed_dict["exchange_rate"] =  exchange_rate.get("rates").get(country.get("currencies")[0].get("code"))
                calculated_gdp = country.get("population") * random.uniform(1000, 2000) / exchange_rate.get("rates").get(country.get("currencies")[0].get("code"))
                parsed_dict["estimated_gdp"] = calculated_gdp
                parsed_dict["flag_url"] = country.get("flag")
                parsed_dict["last_refreshed_at"] = dt_object
                complete_payload.append(parsed_dict)
            # print(country)
            #print(exchange_rate.get("rates").get(country.get("currencies")[0].get("code")))
             
        elif not country.get("currencies"):
            parsed_dict["currency_code"] = "NULL"
            parsed_dict["exchange_rate"] = 0
            parsed_dict["estimated_gdp"] = 0
            parsed_dict["flag_url"] = country.get("flag")
            parsed_dict["last_refreshed_at"] = dt_object
            complete_payload.append(parsed_dict)
    return complete_payload

async def get_exchange_rate_by_country_code(exchange_rate_meta_url, currency_code):
    try:
        async with httpx.AsyncClient() as exchange_meta:
            response = await exchange_meta.get(f'{exchange_rate_meta_url}{currency_code}')
            return response.json()
    except (httpx.ConnectError, httpx.TimeoutException):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail= { 
                "error": "External data source unavailable",
                "details": f"Could not fetch data from {exchange_rate_meta_url}"
            })



