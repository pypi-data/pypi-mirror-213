import asyncio
import logging
import typing

from sila import cloud_connector, discovery, server

from unitelabs.features.core.sila_service import SiLAService

from .config import Config
from .logging import create_logger


class Connector:
    """Main app"""

    def __init__(self, config: typing.Optional[dict] = None):
        self.__config = Config.parse_obj(config or {})

        self._sila_server = server.Server(config=self.config.sila_server)
        self._broadcaster = discovery.Broadcaster(self._sila_server)
        self._cloud_server_endpoint = cloud_connector.CloudServerEndpoint(
            self._sila_server, self.config.cloud_server_endpoint
        )

        self.register(SiLAService())

    def register(self, feature: server.Feature):
        """Register a new feature to this driver"""
        self._sila_server.add_feature(feature)

    async def start(self):
        """Start running this driver"""
        self.logger.info("Starting driver...")

        await asyncio.gather(
            asyncio.create_task(self._sila_server.start()),
            asyncio.create_task(self._broadcaster.start()),
            asyncio.create_task(self._cloud_server_endpoint.start()),
        )

    @property
    def config(self) -> Config:
        return self.__config

    @property
    def sila_server(self) -> server.Server:
        return self._sila_server

    @property
    def logger(self) -> logging.Logger:
        """A standard Python :class:`~logging.Logger` for the app."""
        return create_logger(self.debug)

    @property
    def debug(self) -> bool:
        """Whether debug mode is enabled."""
        return True
