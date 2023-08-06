from datetime import datetime, timezone
from typing import List, Optional

from pydantic import validator

from foreverbull_core.models.base import Base
from foreverbull_core.models.socket import SocketConfig
from foreverbull_core.models.worker import Database


class Parameter(Base):
    key: str
    default: str = None
    value: str = None
    type: str


class Configuration(Base):
    execution: str
    start_time: datetime
    end_time: datetime
    database: Optional[Database]
    parameters: Optional[List[Parameter]]
    socket: SocketConfig


class OHLC(Base):
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    time: datetime


class Info(Base):
    type: str
    version: str
    parameters: List[Parameter]
    routes: List[str]


class DefaultStrategy(Base):
    name: str
    symbols: List[str]
    start: datetime
    end: datetime
    calendar: str = "XNYS"
    backtest_service: str
    backtest_service_image: str
    worker_service: str
    worker_service_image: str
    parameters: Optional[List[Parameter]]

    @validator("start")
    def start_add_utc_tz_info(cls, v):
        return v.replace(tzinfo=timezone.utc)

    @validator("end")
    def end_add_utc_tz_info(cls, v):
        return v.replace(tzinfo=timezone.utc)
