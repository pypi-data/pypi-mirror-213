import requests

from foreverbull_core.http import RequestError


class Backtest:
    def __init__(self, host: str, session: requests.Session = None) -> None:
        """Initializes Backtest service client api

        Args:
            host (str): Host address to the Foreverbull backend server. IP:PORT Format
            session (requests.Session, optional): Use pre defined session instead of creating new. Defaults to None.
        """
        self.host = host
        if session is None:
            session = requests.Session()
        self.session = session

    def run(self, strategy: str) -> dict:
        rsp = self.session.put(
            f"http://{self.host}/api/v1/strategies/{strategy}/backtests",
            params={"execution_type": "manual"},
        )
        if not rsp.ok:
            code = rsp.status_code
            raise RequestError(
                f"""put call /strategies/{strategy}/backtests gave bad return code: {code}
            Text: {rsp.text}"""
            )
        return rsp.json()

    def get(self, backtest: str) -> dict:
        rsp = self.session.get(f"http://{self.host}/api/v1/strategies/backtests/{backtest}")
        if not rsp.ok:
            code = rsp.status_code
            raise RequestError(
                f"""get call /backtests/{backtest} gave bad return code: {code}
            Text: {rsp.text}"""
            )
        return rsp.json()
