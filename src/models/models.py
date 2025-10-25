from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Float
from ..config.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    capital = Column(String(255), nullable=True)
    region = Column(String(255), nullable=True)
    population = Column(BigInteger, nullable=False)
    currency_code = Column(String(7), nullable=True)

    exchange_rate = Column(nullable=True)
    estimated_gdp = Column(Float, default=0) # Store 0 as default
    flag_url = Column(required=True)
    last_refreshed_at = Column(DateTime)
