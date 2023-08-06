import io

import minio
import pandas as pd


class Backtest:
    def __init__(self, client: minio.Minio) -> None:
        self.client = client

    def upload_backtest_result(self, backtest: str, result: pd.DataFrame) -> None:
        result.to_pickle("/tmp/result.pkl")
        self.client.fput_object("backtest-results", f"{backtest}", "/tmp/result.pkl")

    def download_backtest_results(self, backtest: str) -> pd.DataFrame:
        pickled_result = self.client.get_object("backtest-results", f"{backtest}").read()
        return pd.read_pickle(io.BytesIO(pickled_result))
