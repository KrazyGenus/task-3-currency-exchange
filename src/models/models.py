from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Float
from ..config.database import Base
from sqlalchemy.sql import func
from datetime import datetime, timezone

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(512), nullable=False, unique=True, index=True)
    capital = Column(String(512), nullable=True)
    region = Column(String(512), nullable=True, index=True)
    population = Column(BigInteger, nullable=False)
    currency_code = Column(String(5), nullable=False, index=True)
    exchange_rate = Column(Float(precision=10), nullable=False, default=0)
    estimated_gdp = Column(Float(precision=20), nullable=False, default=0) # Store 0 as default
    flag_url = Column(String(512), nullable=True)
    last_refreshed_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, onupdate=func.now())
    
    def __repr__(self):
        return (
            f"Country(id={self.id}, name='{self.name}', capital='{self.capital}', region='{self.region}', "
            f"population={self.population}, currency_code='{self.currency_code}', exchange_rate={self.exchange_rate}, "
            f"estimated_gdp={self.estimated_gdp}, flag_url='{self.flag_url}', last_refreshed_at={self.last_refreshed_at})"
        )