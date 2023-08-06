from datetime import datetime

import requests

from foreverbull_core.models.socket import SocketConfig

from .exceptions import RequestError


class Service:
    def __init__(self, host: str, session: requests.session = None) -> None:
        """Initializes Service- endpoint client api

        Args:
            host (str): Host address to the Foreverbull backend server. IP:PORT Format
            session (requests.Session, optional): Use pre defined session instead of creating new. Defaults to None.
        """
        self.host = host
        if session is None:
            session = requests.Session()
        self.session: requests.Session = session

    def create(self, name: str, image: str) -> bool:
        rsp = self.session.put(
            f"http://{self.host}/api/v1/services",
            json={"name": name, "image": image},
        )
        if not rsp.ok:
            code = rsp.status_code
            raise RequestError(
                f"""post call /services gave bad return code: {code}
            Text: {rsp.text}"""
            )
        return True

    def get(self, service: str) -> dict:
        rsp = self.session.get(f"http://{self.host}/api/v1/services/{service}")
        if not rsp.ok:
            code = rsp.status_code
            raise RequestError(
                f"""get call /services/{service} gave bad return code: {code}
            Text: {rsp.text}"""
            )
        return rsp.json()

    def backtest_ingest(
        self, service: str, symbols: list, start: datetime, end: datetime, calendar: str, benchmark: str
    ) -> bool:
        rsp = self.session.put(
            f"http://{self.host}/api/v1/services/{service}/backtest/ingest",
            json={
                "symbols": symbols,
                "start_time": start.isoformat(),
                "end_time": end.isoformat(),
                "calendar": calendar,
                "benchmark": benchmark,
            },
        )
        if not rsp.ok:
            code = rsp.status_code
            raise RequestError(
                f"""put call /services/{service}/backtest gave bad return code: {code}
            Text: {rsp.text}"""
            )
        return True

    def update_instance(self, service: str, container_id: str, socket: SocketConfig, online: bool) -> bool:
        rsp = self.session.put(
            f"http://{self.host}/api/v1/services/{service}/instances/{container_id}",
            json={**socket.dict(), "online": online},
        )
        if not rsp.ok:
            code = rsp.status_code  # to mitigate next line too long
            raise RequestError(
                f"""get call /services/{service}/instances/{container_id} gave bad return code: {code}
            Text: {rsp.text}"""
            )
        return True
