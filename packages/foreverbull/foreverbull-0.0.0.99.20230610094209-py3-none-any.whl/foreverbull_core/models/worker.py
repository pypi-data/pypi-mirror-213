from typing import NamedTuple

from foreverbull_core.models.base import Base


class Database(Base):
    """_summary_

    Args:
        user (str): str
        password (str): str
        netloc (str): str
        port (int): int
        dbname (str): str

    Returns:
        Database: database
    """

    user: str
    password: str
    netloc: str
    port: int
    dbname: str


class Run(NamedTuple):
    """_summary_

    Args:
        broker_url (str): str = ""
        local_host (str): str = ""

    Returns:
        Run: run
    """

    broker_url: str = ""
    local_host: str = ""


class BacktestRun(Run):
    """_summary_

    Args:
        service_id (str): str = ""
        instance_id (str): str =

    Returns:
        BacktestRun:
    """

    service_id: str = ""
    instance_id: str = ""


class TestRun(NamedTuple):
    """_summary_

    Args:
        NamedTuple (_type_): _description_
    """

    broker_url: str = ""
    local_host: str = ""
    backtest_id: str = ""
