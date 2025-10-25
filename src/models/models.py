from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean, Float
from ..models.models import Base
from datetime import datetime


class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    capital = Column(String(255), nullable=True)
    region = Column(String(255), nullable=True)
    population = Column(Integer, nullable=False)
    currency_code = Column(String(7), nullable=True)

    exchange_rate = Column(nullable=True)
    estimated_gdp = Column()
    flag_url = Column(required=True) # Null store 0
    last_refreshed_at = Column(DateTime)
