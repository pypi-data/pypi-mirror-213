import importlib
import logging
import os
import socket
import time
from multiprocessing import set_start_method

import click

import foreverbull_core.logger
from foreverbull import Foreverbull
from foreverbull.models import Configuration
from foreverbull.worker import WorkerPool
from foreverbull_core.broker import Broker
from foreverbull_core.models.socket import Request, SocketConfig, SocketType
from foreverbull_core.socket.client import SocketClient

foreverbull_core.logger.Logger()

log = logging.getLogger("Foreverbull")

broker = click.make_pass_decorator(Broker)


@click.group()
@click.argument("algo_file", type=str)
@click.pass_context
def base(ctx, algo_file: str):
    try:
        importlib.import_module(algo_file.replace("/", ".").split(".py")[0])
    except ModuleNotFoundError as e:
        logging.error(f"Could not import {algo_file} {e}")
        exit(1)

    broker_url = os.environ.get("BROKER_URL", "127.0.0.1:8080")
    local_host = os.environ.get("LOCAL_HOST", socket.gethostbyname(socket.gethostname()))
    ctx.obj = Broker(broker_url, local_host)


@base.command()
@broker
def start(broker: Broker):
    worker_pool = WorkerPool(**Foreverbull._worker_routes)
    worker_pool.setup()
    fb = Foreverbull(broker.socket_config, worker_pool)
    fb.start()

    while not broker.socket_config.port:
        time.sleep(0.1)

    try:
        broker.http.service.update_instance(
            os.environ.get("SERVICE_NAME"), socket.gethostname(), broker.socket_config, True
        )
        while fb.running:
            time.sleep(0.5)
    except KeyboardInterrupt:
        logging.info("Keyboard- Interrupt recieved exiting")
        broker.http.service.update_instance(
            os.environ.get("SERVICE_NAME"), socket.gethostname(), broker.socket_config, False
        )
    except Exception as e:
        logging.error(f"unable to call backend: {repr(e)}")

    fb.stop()
    exit(0)


@base.command()
@click.option("--strategy", type=str)
@broker
def run(broker: Broker, strategy: str):
    worker_pool = WorkerPool(**Foreverbull._worker_routes)
    worker_pool.setup()
    fb = Foreverbull(broker.socket_config, worker_pool)
    fb.start()

    while not broker.socket_config.port:
        time.sleep(0.1)

    if fb._default_strategy and strategy is None:
        try:
            stored_strategy = broker.http.strategy.get(fb._default_strategy.name)
            log.info(f"Using stored strategy: {stored_strategy}")
            if stored_strategy["backtest"] != fb._default_strategy.backtest_service:
                log.info("Stored backtest does not match default backtest. exiting...")
                fb.stop()
                exit(1)
            if stored_strategy["worker"] != fb._default_strategy.worker_service:
                log.info("Stored worker does not match default worker. exiting...")
                fb.stop()
                exit(1)
            strategy = stored_strategy["name"]
        except Exception:
            log.info("No stored strategy found. Creating one")
            pass

    # We never found a stored strategy, so we need to create one
    if fb._default_strategy and strategy is None:
        try:
            broker.http.finance.get_assets(fb._default_strategy.symbols)
            log.info("Assets already exist")
        except Exception:
            broker.http.finance.create_assets(fb._default_strategy.symbols)
            log.info("Assets created")

        try:
            broker.http.finance.check_ohlc(
                fb._default_strategy.symbols, fb._default_strategy.start, fb._default_strategy.end
            )
            log.info("OHLC already exists")
        except Exception:
            broker.http.finance.create_ohlc(
                fb._default_strategy.symbols, fb._default_strategy.start, fb._default_strategy.end
            )
            log.info("OHLC created")

        try:
            broker.http.service.create(fb._default_strategy.worker_service, fb._default_strategy.worker_service_image)
        except Exception as e:
            log.exception(e)
            log.info("exiting...")
            fb.stop()
            exit(1)

        log.info("Worker service created")

        try:
            broker.http.service.create(
                fb._default_strategy.backtest_service, fb._default_strategy.backtest_service_image
            )
        except Exception as e:
            log.exception(e)
            log.info("exiting...")
            fb.stop()
            exit(1)

        log.info("Backtest service created")
        for _ in range(20):
            rsp = broker.http.service.get(fb._default_strategy.backtest_service)

            if rsp["status"] == "ERROR":
                log.exception(rsp["error"])
                log.info("Exiting...")
                fb.stop()
                exit(1)

            if rsp["status"] == "READY":
                log.info("Backtest service ready")
                break
            time.sleep(1)

        broker.http.service.backtest_ingest(
            fb._default_strategy.backtest_service,
            fb._default_strategy.symbols,
            fb._default_strategy.start,
            fb._default_strategy.end,
            fb._default_strategy.calendar,
            fb._default_strategy.symbols[0],
        )
        log.info("Backtest service ingestion started")
        for _ in range(20):
            rsp = broker.http.service.get(fb._default_strategy.backtest_service)

            if rsp["status"] == "ERROR":
                log.exception(rsp["error"])
                log.info("Exiting...")
                fb.stop()
                exit(1)

            if rsp["status"] == "READY":
                log.info("Backtest service ready after ingestion")
                break
            time.sleep(1)
        broker.http.strategy.create(
            fb._default_strategy.name, fb._default_strategy.backtest_service, fb._default_strategy.worker_service
        )
        log.info("Strategy created")
        strategy = fb._default_strategy.name

    try:
        backtest = broker.http.backtest.run(strategy)
        while backtest["stage"] != "RUNNING":
            if backtest["error"]:
                log.error("backtest failed to start: ", backtest["error"])
                fb.stop()
                return
            time.sleep(1)
            backtest = broker.http.backtest.get(backtest["id"])
        socket_config = SocketConfig(
            host="127.0.0.1",
            port=27015,
            socket_type=SocketType.REQUESTER,
            listen=False,
            recv_timeout=10000,
            send_timeout=10000,
        )
        socket = SocketClient(socket_config)
        ctx = socket.new_context()
        ctx.send(Request(task="get_configuration"))
        rsp = ctx.recv()
        configuration = Configuration(**rsp.data)
        fb.configure(configuration)
        fb.run_backtest()
        ctx.send(Request(task="start"))
        rsp = ctx.recv()
        ctx.send(Request(task="stop"))
        rsp = ctx.recv()
    except KeyboardInterrupt:
        logging.info("Keyboard- Interrupt recieved exiting")
    except Exception as e:
        logging.error(f"unable to call backend: {repr(e)}")

    fb.stop()


if __name__ == "__main__":
    set_start_method("spawn")
    base()
