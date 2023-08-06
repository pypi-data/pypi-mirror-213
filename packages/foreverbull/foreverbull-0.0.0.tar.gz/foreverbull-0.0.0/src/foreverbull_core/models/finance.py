from datetime import datetime
from enum import IntEnum
from typing import Optional

from foreverbull_core.models.base import Base


class Asset(Base):
    symbol: str
    exchange: str
    name: str


class OHLC(Base):
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    time: datetime


class OrderStatus(IntEnum):
    OPEN = 0
    FILLED = 1
    CANCELLED = 2
    REJECTED = 3
    HELD = 4


class Order(Base):
    id: Optional[str]
    symbol: Optional[str]
    amount: Optional[int]
    filled: Optional[int]
    commission: Optional[int]
    limit_price: Optional[int]
    stop_price: Optional[int]
    created_at: Optional[datetime]
    status: Optional[OrderStatus]

    @classmethod
    def from_zipline(cls, order):
        return cls(
            id=order.id,
            symbol=order.sid.symbol,
            amount=order.amount,
            filled=order.filled,
            commission=order.commission,
            limit_price=order.limit,
            stop_price=order.stop,
            created_at=order.created,
            status=order.status,
        )


class Position(Base):
    symbol: str
    amount: int
    cost_basis: float
    period: datetime
