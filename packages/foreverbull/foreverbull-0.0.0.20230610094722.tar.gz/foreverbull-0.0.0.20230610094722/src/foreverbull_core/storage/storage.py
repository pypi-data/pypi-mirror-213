import minio

from .backtest import Backtest


class Storage:
    def __init__(self, address, access_key, secret_key, secure=False):
        self.client = minio.Minio(address, access_key=access_key, secret_key=secret_key, secure=secure)
        self.backtest = Backtest(self.client)

    def create_bucket(self, bucket_name):
        self.client.make_bucket(bucket_name)
