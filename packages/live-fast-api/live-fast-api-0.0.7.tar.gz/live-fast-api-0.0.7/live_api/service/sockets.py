# sockets.py

import socket
from typing import (
    Optional, Union, Tuple, Dict, Any, Iterable
)
from urllib.parse import urlparse

from sockets_communication.sockets import SocketServer

from live_api.endpoints import (
    BaseEndpoint, encode, valid_endpoints
)

__all__ = [
    "SocketService"
]

Socket = socket.socket
Host = str
Port = Union[str, int]
Address = Tuple[Host, Port]
Endpoints = Dict[str, BaseEndpoint]
EndpointsContainer = Union[
    Iterable[BaseEndpoint],
    Endpoints
]

class SocketService(SocketServer):
    """
    A class to represent a service object.

    The BaseService is the parent class of service class.
    The service class creates a service object to deploy
    functionality of endpoint objects as a REST API, with sockets backend.

    data attributes:

    - endpoints:
        A set of endpoint objects to serve with the api.

    >>> from live_api.endpoints import BaseEndpoint, GET
    >>> from live_api.service.sockets import SocketService
    >>>
    >>> class MyEndpoint(BaseEndpoint):
    >>>     ...
    >>>
    >>>     def endpoint(self, *args: Any, **kwargs: Any) -> Any:
    >>>         ...
    >>>
    >>> endpoint = MyEndpoint(path="/my_endpoint", methods=[GET])
    >>>
    >>> service = SocketService(
    >>>     endpoints=[endpoint]
    >>> )
    >>>
    >>> service.run()
    """

    def __init__(self, endpoints: Optional[EndpointsContainer] = None) -> None:
        """
        Defines the server datasets for clients and client commands.

        :param endpoints: The commands to run for specific requests of the clients.
        """

        self.endpoints = self.valid_endpoints(endpoints or {})

        SocketServer.__init__(self)
    # end __init__

    @staticmethod
    def valid_endpoints(endpoints: Optional[Any] = None) -> Endpoints:
        """
        Process the endpoints' commands to validate and modify it.

        :param endpoints: The endpoints object to check.

        :return: The valid endpoints object.
        """

        return valid_endpoints(endpoints=endpoints)
    # end valid_endpoints

    def respond(self, address: Address, connection: Socket) -> None:
        """
        Sets or updates clients data in the clients' container .

        :param address: The ip address and port used for the sockets' connection.
        :param connection: The sockets object used for the connection.
        """

        url = self.receive(connection=connection).decode()

        payload = urlparse(url)

        kwargs = {
            segment[:segment.find("=")]: segment[segment.find("=") + 1:]
            for segment in payload.query.split("&")
        }

        self.send(
            message=encode(self.endpoints[payload.path[1:]](**kwargs)).encode(),
            connection=connection
        )

        self.disconnect_client(connection=connection)
    # end respond
# end SocketService