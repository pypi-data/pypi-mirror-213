from datetime import datetime
from typing import List

import requests

from .exceptions import RequestError


class Finance:
    def __init__(self, host: str, session: requests.session = None) -> None:
        self.host = host
        if session is None:
            session = requests.Session()
        self.session: requests.Session = session

    def get_assets(self, symbols: List[str]) -> List[dict]:
        rsp = self.session.get(f"http://{self.host}/api/v1/finance/assets", params={"symbols": symbols})
        if not rsp.ok:
            code = rsp.status_code
            raise RequestError(
                f"""get call /finance/assets gave bad return code: {code}
            Text: {rsp.text}"""
            )
        return rsp.json()

    def create_assets(self, symbols: List[str]) -> List[dict]:
        rsp = self.session.put(f"http://{self.host}/api/v1/finance/assets", json={"symbols": symbols})
        if not rsp.ok:
            code = rsp.status_code
            raise RequestError(
                f"""put call /finance/assets gave bad return code: {code}
            Text: {rsp.text}"""
            )
        return rsp.json()

    def check_ohlc(self, symbols: List[str], start: datetime, end: datetime) -> bool:
        rsp = self.session.get(
            f"http://{self.host}/api/v1/finance/ohlc/check",
            params={"symbols": symbols, "startTime": start.isoformat(), "endTime": end.isoformat()},
        )
        if not rsp.ok:
            code = rsp.status_code
            raise RequestError(
                f"""head call /finance/ohlc/check gave bad return code: {code}
            Text: {rsp.text}"""
            )
        return rsp.ok

    def create_ohlc(self, symbols: List[str], start: datetime, end: datetime) -> List[dict]:
        rsp = self.session.put(
            f"http://{self.host}/api/v1/finance/ohlc",
            json={"symbols": symbols, "start_time": start.isoformat(), "end_time": end.isoformat()},
        )
        if not rsp.ok:
            code = rsp.status_code
            raise RequestError(
                f"""put call /finance/ohlc gave bad return code: {code}
            Text: {rsp.text}"""
            )
        return rsp.json()
