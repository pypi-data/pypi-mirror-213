from __future__ import annotations

import asyncio
import logging
import typing
import uuid

import grpc.aio

from sila import commands, core, identifiers, properties

if typing.TYPE_CHECKING:
    from .feature import Feature


class ServerConfig(typing.TypedDict, total=False):
    host: str
    """Bind the gRPC server to this host."""

    port: typing.Union[str, int]
    """Bind the gRPC server to this port. If set to `0` an available port is chosen at runtime."""

    uuid: str
    """
    Uniquely identifies the SiLA server. Needs to remain the same even after restarting the server.
    Follows the textual representation of UUIDs, e.g. "082bc5dc-18ae-4e17-b028-6115bbc6d21e".
    """

    name: str
    """
    Human readable name of the SiLA server. This value is configurable during runtime via the SiLA
    Service feature's `set_server_name` command. Must not exceed 255 characters.
    """

    type: str
    """
    Human readable identifier of the SiLA server used to describe the entity the server represents.
    Starts with a capital letter, continued by letters and digits up to a maximum of 255 characters.
    """

    description: str
    """Describes the use and purpose of the SiLA Server."""

    version: str
    """
    The version of the SiLA server following the Semantic Versioning specification with pre-release
    identifiers separated by underscores, e.g. "3.19.373_mighty_lab_devices".
    """

    vendor_url: str
    """
    URL to the website of the vendor or the website of the product of this SiLA Server. Follows the
    Uniform Resource Locator specification in RFC 1738.
    """


class Server(core.Server):
    """
    SiLA 2 compliant gRPC server.

    A SiLA Server can either be a physical laboratory instrument or a software system that offers
    functionalities to clients. These functions are specified and described in Features.
    """

    def __init__(self, config: ServerConfig | None = None):
        config = config or {}
        super().__init__(
            uuid=config.get("uuid", str(uuid.uuid4())),
            type=config.get("type", "ExampleServer"),
            name=config.get("name", "SiLA Server"),
            version=config.get("version", "0.1"),
            description=config.get("description", ""),
            vendor_url=config.get("vendor_url", "https://github.com/UniteLabs/driver"),
        )
        self.host = config.get("host", "[::]")
        self.port = config.get("port", 0)

        self.server = grpc.aio.server()
        self.running = False
        self.features: dict[str, Feature] = {}

        self.command_executions: dict[str, commands.CommandExecution] = {}

    @property
    def logger(self) -> logging.Logger:
        """A standard python :class:`~logging.Logger` for the app."""
        logger = logging.getLogger("sila")
        logger.setLevel(logging.INFO)
        return logger

    async def start(self):
        """Starts this Server."""
        if self.running:
            raise RuntimeError("Server is already running.")

        try:
            self.port = self.server.add_insecure_port(f"{self.host}:{self.port}")
            await self.server.start()
            self.logger.info("Starting SiLA server on address '%s:%s'...", self.host, self.port)
            self.running = True
            await self.server.wait_for_termination()
        except asyncio.CancelledError:
            await self.stop()

    async def stop(self, grace: float | None = None):
        """
        Stops this server.

        Parameters:
            grace: A grace period allowing the RPC handlers to gracefully shutdown.
        """
        self.logger.info("Stopping SiLA server...")
        await self.server.stop(grace=grace)
        self.running = False

    def add_feature(self, feature: Feature):
        """
        Registers a SiLA Feature as RPC handler with this server.

        Parameters:
            feature: The SiLA feature to add to this server.
        """
        if self.running:
            raise RuntimeError("Cannot add feature. Server is already running.")

        feature.add_to_server(self)

    def get_feature(self, identifier: str | identifiers.FullyQualifiedFeatureIdentifier) -> Feature:
        """
        Get a registered feature.

        Parameters:
            identifier: The fully qualified feature identifier.
        """
        identifier = str(identifier)
        if identifier not in self.features:
            raise ValueError(f"Unknown feature with identifier {identifier}")

        return self.features[identifier]

    def add_command_execution(self, command_execution: commands.CommandExecution) -> None:
        if command_execution.command_execution_uuid in self.command_executions:
            raise ValueError(
                f"Command execution with uuid '{command_execution.command_execution_uuid}' already exists."
            )

        self.command_executions[command_execution.command_execution_uuid] = command_execution

    def get_command_execution(self, command_execution_uuid: str) -> commands.CommandExecution:
        if command_execution_uuid not in self.command_executions:
            raise ValueError(f"Command execution not found for uuid '{command_execution_uuid}'.")

        return self.command_executions[command_execution_uuid]

    def get_command(self, identifier: str) -> commands.Command:
        fully_qualifier_command_identifier = identifiers.FullyQualifiedCommandIdentifier.parse(identifier)

        if str(fully_qualifier_command_identifier) not in self.features:
            raise ValueError(f"Unknown feature in identifier: {identifier}")

        feature = self.features[str(fully_qualifier_command_identifier)]

        command = next(
            (
                command
                for command in feature.commands
                if command.identifier == fully_qualifier_command_identifier.command
            ),
            None,
        )

        if command is None:
            raise ValueError(f"Unknown command in identifier: {identifier}")

        return command

    def get_unobservable_command(self, identifier: str) -> commands.UnobservableCommand:
        unobservable_command = self.get_command(identifier)

        if not isinstance(unobservable_command, commands.UnobservableCommand):
            raise ValueError(f"Identifier does not identify an unobservable command: {identifier}")

        return unobservable_command

    def get_observable_command(self, identifier: str) -> commands.ObservableCommand:
        observable_command = self.get_command(identifier)

        if not isinstance(observable_command, commands.ObservableCommand):
            raise ValueError(f"Identifier does not identify an observable command: {identifier}")

        return observable_command

    def get_property(self, identifier: str) -> properties.Property:
        fully_qualifier_property_identifier = identifiers.FullyQualifiedPropertyIdentifier.parse(identifier)

        if str(fully_qualifier_property_identifier) not in self.features:
            raise ValueError(f"Unknown feature in identifier: {identifier}")

        feature = self.features[str(fully_qualifier_property_identifier)]

        if fully_qualifier_property_identifier.property not in feature.properties:
            raise ValueError(f"Unknown property in identifier: {identifier}")

        return feature.properties[fully_qualifier_property_identifier.property]

    def get_unobservable_property(self, identifier: str) -> properties.UnobservableProperty:
        unobservable_property = self.get_property(identifier)

        if not isinstance(unobservable_property, properties.UnobservableProperty):
            raise ValueError(f"Identifier does not identify an unobservable property: {identifier}")

        return unobservable_property

    def get_observable_property(self, identifier: str) -> properties.ObservableProperty:
        observable_property = self.get_property(identifier)

        if not isinstance(observable_property, properties.ObservableProperty):
            raise ValueError(f"Identifier does not identify an observable property: {identifier}")

        return observable_property
