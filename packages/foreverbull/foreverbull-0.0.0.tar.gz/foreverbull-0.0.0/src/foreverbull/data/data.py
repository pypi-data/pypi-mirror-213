from pandas import DataFrame, read_sql_query
from sqlalchemy import create_engine, desc
from sqlalchemy.orm.session import sessionmaker

from foreverbull.data.stock_data import Base, Period, Position
from foreverbull_core.models.worker import Database as DatabaseConfiguration


class DateManager:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.current = None


class Database:
    def __init__(self, execution_id: str, date_manager: DateManager, db_conf: DatabaseConfiguration = None):
        self.db_conf = db_conf
        if db_conf is None:
            self.uri = "sqlite:///:memory:"
        else:
            self.uri = (
                f"postgresql://{db_conf.user}:{db_conf.password}@{db_conf.netloc}:{db_conf.port}/{db_conf.dbname}"
            )
        self.execution_id = execution_id
        self.date_manager = date_manager
        self.engine = create_engine(self.uri)
        if self.db_conf is None:
            Base.metadata.create_all(self.engine)
        self.session_maker = sessionmaker(self.engine)

    def stock_data(self, symbol: str = None) -> DataFrame:
        if symbol:
            query = f"""Select symbol, time, high, low, open, close, volume
                        FROM ohlc WHERE time BETWEEN '{self.date_manager.start}'
                        AND '{self.date_manager.current}' AND symbol='{symbol}'"""
        else:
            query = f"""Select symbol, time, high, low, open, close, volume
                        FROM ohlc WHERE time BETWEEN '{self.date_manager.start}'
                        AND '{self.date_manager.current}'"""
        return read_sql_query(query, self.engine)

    def period(self) -> Period:
        with self.session_maker() as db_session:
            q = db_session.query(Period).filter_by(execution_id=self.execution_id)
            period = q.order_by(desc(Period.timestamp)).first()
        return period

    def get_position(self, symbol: str) -> Position:
        with self.session_maker() as db_session:
            query = db_session.query(Position)
            query = query.filter(Position.execution == self.execution_id)
            query = query.filter(symbol == Position.symbol)
            query = query.order_by(desc(Position.period))
            position = query.first()

        return position
