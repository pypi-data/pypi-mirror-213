import asyncio
import logging
import socket

import zeroconf

from sila.server import Server


class Broadcaster:
    def __init__(self, server: Server):
        self.mdns = zeroconf.Zeroconf()
        self.service = zeroconf.ServiceInfo(
            type_="_sila._tcp.local.",
            name=f"{server.uuid}._sila._tcp.local.",
            addresses=get_addresses(),
            port=int(server.port),
            properties={
                "version": server.version.encode("utf-8")[:247],
                "server_name": server.name.encode("utf-8")[:243],
                "description": server.description.encode("utf-8")[:243],
            },
        )

    async def start(self):
        """Starts this client."""
        self.logger.info("Starting broadcaster...")

        try:
            await self.mdns.async_register_service(self.service)
            while True:
                await asyncio.sleep(10)
        except asyncio.CancelledError:
            await self.stop()

    async def stop(self):
        """Stops this client."""
        self.logger.info("Stopping broadcaster...")
        await self.mdns.async_unregister_all_services()
        self.mdns.close()

    @property
    def logger(self) -> logging.Logger:
        """A standard Python :class:`~logging.Logger` for the app."""
        return logging.getLogger(__name__)


def get_addresses() -> list[bytes]:
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connection.settimeout(0)
    try:
        connection.connect(("8.8.8.8", 80))
        ip = connection.getsockname()[0]
    except Exception:  # pylint: disable=broad-exception-caught
        ip = socket.gethostbyname(socket.gethostname())
    finally:
        connection.close()

    return [socket.inet_pton(socket.AF_INET, ip)]
