from pydantic import BaseModel

class MarketData(BaseModel):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float
