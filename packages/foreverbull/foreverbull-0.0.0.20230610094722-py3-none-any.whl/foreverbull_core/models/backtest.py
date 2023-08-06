from datetime import datetime, timezone
from typing import List, Optional

import numpy as np
from numpy import isnan

from foreverbull_core.models.base import Base
from foreverbull_core.models.socket import SocketConfig

# KEEP TILL HTTP IS FIXED


class Execution(Base):
    running: bool
    stage: str
    error: Optional[str]


class Session(Base):
    id: Optional[str]
    backtest_id: str
    worker_id: Optional[str]
    worker_count: Optional[int]
    run_automaticlly: bool = False
    execution: Optional[Execution]


# END KEEP


class Database(Base):
    user: str
    password: str
    netloc: str
    port: int
    dbname: str


class Sockets(Base):
    main: SocketConfig
    feed: SocketConfig
    broker: SocketConfig
    running: bool


class IngestConfig(Base):
    calendar: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    symbols: List[str]


class EngineConfig(Base):
    calendar: str
    start_time: datetime
    end_time: datetime
    benchmark: Optional[str] = None
    symbols: List[str]


class Period(Base):
    period: datetime
    shorts_count: Optional[int]
    pnl: Optional[int]
    long_value: Optional[int]
    short_value: Optional[int]
    long_exposure: Optional[int]
    starting_exposure: Optional[int]
    short_exposure: Optional[int]
    capital_used: Optional[int]
    gross_leverage: Optional[int]
    net_leverage: Optional[int]
    ending_exposure: Optional[int]
    starting_value: Optional[int]
    ending_value: Optional[int]
    starting_cash: Optional[int]
    ending_cash: Optional[int]
    returns: Optional[int]
    portfolio_value: Optional[int]
    longs_count: Optional[int]
    algo_volatility: Optional[int]
    sharpe: Optional[int]
    alpha: Optional[int]
    beta: Optional[int]
    sortino: Optional[int]
    max_drawdown: Optional[int]
    max_leverage: Optional[int]
    excess_return: Optional[int]
    treasury_period_return: Optional[int]
    benchmark_period_return: Optional[int]
    benchmark_volatility: Optional[int]
    algorithm_period_return: Optional[int]

    @classmethod
    def from_backtest(cls, period):
        return Period(
            period=period["period_open"].to_pydatetime().replace(tzinfo=timezone.utc),
            shorts_count=int(period["shorts_count"] * 100),
            pnl=int(period["pnl"] * 100),
            long_value=int(period["long_value"] * 100),
            short_value=int(period["short_value"] * 100),
            long_exposure=int(period["long_exposure"] * 100),
            starting_exposure=int(period["starting_exposure"] * 100),
            short_exposure=int(period["short_exposure"] * 100),
            capital_used=int(period["capital_used"] * 100),
            gross_leverage=int(period["gross_leverage"] * 100),
            net_leverage=int(period["net_leverage"] * 100),
            ending_exposure=int(period["ending_exposure"] * 100),
            starting_value=int(period["starting_value"] * 100),
            ending_value=int(period["ending_value"] * 100),
            starting_cash=int(period["starting_cash"] * 100),
            ending_cash=int(period["ending_cash"] * 100),
            returns=int(period["returns"] * 100),
            portfolio_value=int(period["portfolio_value"] * 100),
            longs_count=int(period["longs_count"] * 100),
            algo_volatility=None if isnan(period["algo_volatility"]) else int(period["algo_volatility"] * 100),
            sharpe=None if isnan(period["sharpe"]) else int(period["sharpe"] * 100),
            alpha=None if period["alpha"] is None or np.isnan(period["alpha"]) else int(period["alpha"] * 100),
            beta=None if period["beta"] is None or np.isnan(period["beta"]) else int(period["beta"] * 100),
            sortino=None if isnan(period["sortino"]) else int(period["sortino"] * 100),
            max_drawdown=None if isnan(period["max_drawdown"]) else int(period["max_drawdown"] * 100),
            max_leverage=None if isnan(period["max_leverage"]) else int(period["max_leverage"] * 100),
            excess_return=None if isnan(period["excess_return"]) else int(period["excess_return"] * 100),
            treasury_period_return=None
            if isnan(period["treasury_period_return"])
            else int(period["treasury_period_return"] * 100),
            benchmark_period_return=None
            if isnan(period["benchmark_period_return"])
            else int(period["benchmark_period_return"] * 100),
            benchmark_volatility=None
            if isnan(period["benchmark_volatility"])
            else int(period["benchmark_volatility"] * 100),
            algorithm_period_return=None
            if isnan(period["algorithm_period_return"])
            else int(period["algorithm_period_return"] * 100),
        )


class Result(Base):
    periods: List[Period]
