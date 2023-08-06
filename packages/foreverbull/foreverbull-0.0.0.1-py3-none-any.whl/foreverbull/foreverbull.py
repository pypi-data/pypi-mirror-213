import logging
import threading
from inspect import signature

from foreverbull.data import Database
from foreverbull.models import OHLC, Configuration, DefaultStrategy, Info, Parameter
from foreverbull.worker import WorkerPool
from foreverbull_core.socket.client import SocketClient, SocketConfig
from foreverbull_core.socket.exceptions import SocketClosed, SocketTimeout
from foreverbull_core.socket.router import MessageRouter


class Foreverbull(threading.Thread):
    _parameters = []
    _worker_routes = {}
    _default_strategy = None

    def __init__(
        self,
        socket_config: SocketConfig = None,
        worker_pool: WorkerPool = None,
        default_strategy: DefaultStrategy = None,
    ):
        self.socket_config = socket_config
        self.running = False
        self._worker_pool: WorkerPool = worker_pool
        self.logger = logging.getLogger(__name__)
        self._routes = MessageRouter()
        self._routes.add_route(self.info, "info")
        self._routes.add_route(self.stop, "stop")
        self._routes.add_route(self.configure, "configure", Configuration)
        self._routes.add_route(self.run_backtest, "run_backtest")
        threading.Thread.__init__(self)

    @staticmethod
    def _eval_param(type: str) -> str:
        if type == int:
            return "int"
        elif type == float:
            return "float"
        elif type == bool:
            return "bool"
        elif type == str:
            return "str"
        else:
            raise Exception("Unknown parameter type: {}".format(type))

    @staticmethod
    def add_route(func, msg_type):
        for key, value in signature(func).parameters.items():
            if value.annotation == Database or value.annotation == OHLC:
                continue
            default = None if value.default == value.empty else str(value.default)
            parameter = Parameter(key=key, default=default, type=Foreverbull._eval_param(value.annotation))
            Foreverbull._parameters.append(parameter)
        Foreverbull._worker_routes[msg_type] = func

    @staticmethod
    def on(msg_type, default_strategy: DefaultStrategy = None):
        def decorator(func):
            Foreverbull._default_strategy = default_strategy
            Foreverbull.add_route(func, msg_type)
            return func

        return decorator

    def info(self):
        return Info(
            type="worker", version="0.0.1", parameters=self._parameters, routes=list(self._worker_routes.keys())
        )

    def run(self):
        self.running = True
        self.logger.info("Starting instance")
        socket = SocketClient(self.socket_config)
        context_socket = None
        self.logger.info("Listening on {}:{}".format(self.socket_config.host, self.socket_config.port))
        while self.running:
            try:
                context_socket = socket.new_context()
                request = context_socket.recv()
                response = self._routes(request)
                context_socket.send(response)
                context_socket.close()
            except SocketTimeout:
                context_socket.close()
            except SocketClosed as exc:
                self.logger.exception(exc)
                self.logger.info("main socket closed, exiting")
        socket.close()
        self.logger.info("exiting")

    def configure(self, configuration: Configuration) -> None:
        self.logger.info("Configuring instance")
        self._worker_pool.configure(configuration)
        return None

    def run_backtest(self):
        self.logger.info("Running backtest")
        self._worker_pool.run_backtest()

    def stop(self):
        self.logger.info("Stopping instance")
        if self._worker_pool:
            self._worker_pool.stop()
        self.running = False
