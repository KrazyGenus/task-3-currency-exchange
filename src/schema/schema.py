from pydantic import BaseModel
from datetime import datetime

class CountryBase(BaseModel):
    id: int
    name: str
    capital: str
    region: str
    population: int
    currency_code: str

    exchange_rate: float
    estimated_gdp: float
    flag_url: str
    last_refreshed_at: datetime

class CountryCreate(CountryBase):
    pass
    
    
    class Config:
        orm_mode = True