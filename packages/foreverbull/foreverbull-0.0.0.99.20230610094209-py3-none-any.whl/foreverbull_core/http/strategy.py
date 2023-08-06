import requests

from .exceptions import RequestError


class Strategy:
    def __init__(self, host: str, session: requests.session = None) -> None:
        self.host = host
        if session is None:
            session = requests.Session()
        self.session: requests.Session = session

    def create(self, name: str, backtest: str, worker: str):
        rsp = self.session.put(
            f"http://{self.host}/api/v1/strategies",
            json={"name": name, "backtest": backtest, "worker": worker},
        )
        if not rsp.ok:
            code = rsp.status_code
            raise RequestError(
                f"""put call /strategies gave bad return code: {code}
            Text: {rsp.text}"""
            )
        return rsp.json()

    def get(self, name: str):
        rsp = self.session.get(f"http://{self.host}/api/v1/strategies/{name}")
        if not rsp.ok:
            code = rsp.status_code
            raise RequestError(
                f"""get call /strategies/{name} gave bad return code: {code}
            Text: {rsp.text}"""
            )
        return rsp.json()
