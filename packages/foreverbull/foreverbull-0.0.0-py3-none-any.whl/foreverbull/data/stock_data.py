from sqlalchemy import Column, DateTime, Float, Integer, Numeric, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OHLC(Base):
    __tablename__ = "ohlc"
    id = Column("id", Integer, primary_key=True)
    symbol = Column("symbol", String)
    open = Column("open", Numeric)
    high = Column("high", Numeric)
    low = Column("low", Numeric)
    close = Column("close", Numeric)
    volume = Column("volume", Integer)
    time = Column("time", DateTime)


class Position(Base):
    __tablename__ = "position"
    id = Column("id", Integer, primary_key=True)
    execution = Column("execution", String)
    symbol = Column("symbol", String)
    amount = Column("amount", Integer)
    cost_basis = Column("cost_basis", Float)
    period = Column("period", DateTime)


class Period(Base):
    __tablename__ = "backtest_period"
    id = Column("id", Integer, primary_key=True)
    execution_id = Column("execution", String)
    cash_flow = Column("cash_flow", Float)
    starting_cash = Column("starting_cash", Integer)
    portfolio_value = Column("portfolio_value", Float)
    pnl = Column("pnl", Float)
    returns = Column("_returns", Float)
    timestamp = Column("start_date", DateTime)
    positions_value = Column("positions_value", Float)
    positions_exposure = Column("positions_exposure", Float)
