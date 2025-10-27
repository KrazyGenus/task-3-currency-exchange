from pydantic import BaseModel, field_serializer
from datetime import datetime
from typing import Optional


DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
class CountrySchema(BaseModel):
    id: int
    name: str
    capital: Optional[str]
    region: Optional[str]
    population: int
    currency_code: str
    exchange_rate: float
    estimated_gdp: float
    flag_url: Optional[str]
    last_refreshed_at: datetime
    
    
    @field_serializer("last_refreshed_at")
    def serialize_datetime(self, dt: datetime, _info):
        if dt is None:
            return None
        return dt.strftime(DATE_TIME_FORMAT)
    class Config:
        from_attribute = True