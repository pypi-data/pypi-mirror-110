# -*- coding: utf-8 -*-
import logging
import os
import socket

from outflow.core.logging import logger
from outflow.core.pipeline import config, context, settings
from outflow.core.pipeline.context_manager import PipelineContextManager


class AddIpFilter(logging.Filter):
    def filter(self, record):
        pid = os.getpid()
        ip = socket.gethostbyname(socket.gethostname())
        record.pid = pid
        record.ip = ip
        return True


class BaseActor:
    def set_pipeline_state(self, *, context_state, config_state, settings_state):
        context.setstate(context_state)
        config.setstate(config_state)
        settings.setstate(settings_state)

    def __init__(
        self,
        pipeline_states=None,
        actor_init_kwargs=None,
        python_path=None,
    ):
        logger.debug(f"Initialize actor '{self}'")
        if actor_init_kwargs is None:
            actor_init_kwargs = dict()
        self.__dict__.update(**actor_init_kwargs)
        self.context_manager = (
            PipelineContextManager().__enter__()
        )  # TODO do this but cleaner
        self.set_pipeline_state(**pipeline_states)

        import logging.handlers

        from outflow.core.logging import set_plugins_loggers_config

        set_plugins_loggers_config()

        logging.config.dictConfig(config["logging"])

        socket_handler = logging.handlers.SocketHandler(
            context.redis_address, logging.handlers.DEFAULT_TCP_LOGGING_PORT
        )
        socket_handler.setLevel(logging.DEBUG)
        socket_handler.addFilter(AddIpFilter())

        for logger_name in config["logging"].get("loggers", {}):
            if logger_name == "":
                continue
            _logger = logging.getLogger(logger_name)
            # logger.debug(f"adding socket handler {socket_handler} to logger {_logger}")
            _logger.handlers = [socket_handler]
