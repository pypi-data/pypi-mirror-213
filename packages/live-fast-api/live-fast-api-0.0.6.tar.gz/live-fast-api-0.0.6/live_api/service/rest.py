# rest.py

import os
import time
import logging
from functools import partial
import threading
import datetime as dt
import copy
import types
import functools
from typing import (
    Any, Union, Iterable, Optional, Dict, Callable
)

from uvicorn import Server, Config as ServiceConfig
from fastapi import FastAPI, APIRouter
import fastapi

from live_api.base import terminate_thread, icons
from live_api.endpoints import (
    EndpointFileResponse, BaseEndpoint,
    GET, EndpointRedirectResponse,
    DocsEndpoint, FAVICON, DOCS, valid_endpoints
)

from represent import BaseModel, Modifiers

__all__ = [
    "RESTService"
]

Port = Union[str, int]
Host = str

Endpoints = Dict[str, BaseEndpoint]
EndpointsContainer = Union[Iterable[BaseEndpoint], Endpoints]

def override_signature(
        command: Union[Callable, types.FunctionType], /, *,
        new: types.FunctionType
) -> types.FunctionType:
    """
    Overrides the signature of a function.

    :param command: The function to override.
    :param new: The function wit the new signature.

    :return: The old function with the new signature.
    """

    attributes = (
        '__module__', '__name__', '__qualname__',
        '__doc__', '__annotations__'
    )

    for attr in attributes:
        setattr(command, attr, getattr(new, attr))
    # end for

    command.__annotations__['return'] = (
        Dict[str, Union[int, new.__annotations__['return']]]
    )

    command = functools.update_wrapper(command, new, assigned=attributes)

    command.__kwdefaults__ = copy.copy(new.__kwdefaults__)

    return command
# end override_signature

class RESTService(BaseModel):
    """
    A class to represent a service object.

    The BaseService is the parent class of service class.
    The service class creates a service object to deploy
    functionality of endpoint objects as a REST API.

    data attributes:

    - name:
        The name of the service.

    - endpoints:
        A set of endpoint objects to serve with the api.

    - root:
        A common root path to add to all endpoints.

    - icon:
        A path to an icon file to display in a web interface (*.ico).

    - home:
        The path to the home page of the web interface.

    - debug:
        The value to set the home page as the test page.

    >>> from live_api.endpoints import BaseEndpoint, GET
    >>> from live_api.service.rest import RESTService
    >>>
    >>> class MyEndpoint(BaseEndpoint):
    >>>     ...
    >>>
    >>>     def endpoint(self, *args: Any, **kwargs: Any) -> Any:
    >>>         ...
    >>>
    >>> endpoint = MyEndpoint(path="/my_endpoint", methods=[GET])
    >>>
    >>> service = RESTService(
    >>>     name="service", path="<PATH TO THE SERVICE>",
    >>>     endpoints=[endpoint]
    >>> )
    >>>
    >>> service.run()
    """

    SILENT = False

    ICON = icons() + "\\icon.ico"
    VERSION = "0.0.0"
    DESCRIPTION = ""
    NAME = "Live Auto-API Service"

    modifiers = Modifiers(
        excluded=[
            "app", "_root", "timeout_process",
            "service_process", "modifiers"
        ]
    )

    def __init__(
            self,
            name: Optional[str] = None,
            version: Optional[str] = None,
            endpoints: Optional[EndpointsContainer] = None,
            root: Optional[str] = None,
            description: Optional[str] = None,
            icon: Optional[str] = None,
            home: Optional[Union[str, bool]] = None,
            debug: Optional[bool] = None
    ) -> None:
        """
        Defines the class attributes.

        :param name: The name of the service.
        :param version: The version of the service.
        :param endpoints: The service endpoints.
        :param description: The description of the object.
        :param icon: The icon path.
        :param root: The root to the path.
        :param home: The home endpoint.
        :param debug: The value to create the docs' endpoint for the home endpoint.
        """

        self._root = None

        self.endpoints = {}

        if (
            (isinstance(home, bool) and home) or
            (debug and (home is None))
        ):
            home = True
        # end if

        self.app = None

        self.service_process = None
        self.timeout_process = None

        self.block = False

        self.description = description or self.DESCRIPTION
        self.root = root or ""
        self.icon = icon or self.ICON
        self.home = home
        self.name = name or self.NAME
        self.version = version or self.VERSION

        self.endpoints.update(
            self.valid_endpoints(endpoints)
        )

        for endpoint in self.endpoints.values():
            endpoint.service = self
        # end for
    # end __init__

    def __getstate__(self) -> Dict[str, Any]:
        """
        Gets the state of the object.

        :return: The state of the object.
        """

        data = self.__dict__.copy()

        data["app"] = None
        data["service_process"] = None
        data["service_process"] = None

        return data
    # end __getstate__

    @staticmethod
    def valid_endpoints(endpoints: Optional[Any] = None) -> Endpoints:
        """
        Process the endpoints' commands to validate and modify it.

        :param endpoints: The endpoints object to check.

        :return: The valid endpoints object.
        """

        return valid_endpoints(endpoints=endpoints)
    # end valid_endpoints

    @property
    def root(self) -> str:
        """
        Gets the root path of the service.

        :returns: The root path.
        """

        return self._root
    # end get_root

    @root.setter
    def root(self, value: str) -> None:
        """
        Sets the root path of the endpoints and the service.

        :param value: The root path.
        """

        if value == self._root:
            return
        # end if

        self._root = value

        for endpoint in self.endpoints.copy().values():
            endpoint.set_root(self.root)

            if endpoint.root:
                self.endpoints.pop(endpoint.path)

                self.endpoints[
                    "/" + endpoint.root + endpoint.path
                ] = endpoint
            # end if
        # end for

        if self.built():
            self.build()
        # end if
    # end set_root

    def set_root(self, root: str, /) -> None:
        """
        Sets the root path of the endpoints and the service.

        :param root: The root path.
        """

        self.root = root
    # end set_root

    def get_root(self) -> str:
        """
        Gets the root path of the service.

        :returns: The root path.
        """

        return self.root
    # end get_root

    def blocked(self) -> bool:
        """
        Returns the value of te execution being blocked by the service loop.

        :return: The blocking value.
        """

        return self.block
    # end blocked

    def add_endpoint(self, endpoint: BaseEndpoint, path: Optional[str] = None) -> None:
        """
        Adds the endpoint to the service.

        :param path: The path for the endpoint.
        :param endpoint: The command to run.
        """

        self.endpoints[path or endpoint.path] = endpoint
    # end add_endpoint

    def add_endpoints(self, endpoints: EndpointsContainer) -> None:
        """
        Adds the endpoint to the service.

        :param endpoints: The commands to run.
        """

        self.endpoints.update(self.valid_endpoints(endpoints))
    # end add_endpoints

    def set_endpoint(
            self, endpoint: BaseEndpoint, path: Optional[str] = None
    ) -> None:
        """
        Adds the endpoint to the service.

        :param path: The path for the endpoint.
        :param endpoint: The command to run.
        """

        path = path or endpoint.path

        if path not in self.endpoints:
            raise ValueError(
                f"The path was not initialized for a different "
                f"endpoint beforehand. Consider using "
                f"'{self.add_endpoint.__name__}' method instead, "
                f"to add endpoints with new path. Given path: {path}. "
                f"Valid paths: {', '.join(self.endpoints.keys())}"
            )
        # end if

        self.endpoints[path] = endpoint
    # end set_endpoint

    def remove_endpoint(
            self, *,
            path: Optional[str] = None,
            endpoint: Optional[BaseEndpoint] = None
    ) -> None:
        """
        Removes the endpoint from the service.

        :param path: The index for the endpoint.
        :param endpoint: The command to run.
        """

        if path is not None:
            try:
                self.endpoints.pop(path)

            except KeyError:
                raise ValueError(
                    f"The path was not initialized for a different "
                    f"endpoint beforehand, therefore an endpoint "
                    f"labeled with that path couldn't be removed. Given path: {path}. "
                    f"Valid paths: {', '.join(self.endpoints.keys())}"
                )
            # end try

        elif endpoint is not None:
            for key, value in self.endpoints.items():
                if (value is endpoint) or (value == endpoint):
                    self.endpoints.pop(key)
                # end if

            else:
                raise ValueError(
                    f"Endpoint object '{repr(endpoint)}' doesn't "
                    f"exist in the endpoints of service object {repr(self)}, "
                    f"therefore could not be removed. Given path: {path}. "
                    f"Valid paths: {', '.join(self.endpoints.keys())}"
                )
            # end for
        # end if
    # end remove_endpoint

    def remove_endpoints(
            self, *,
            paths: Optional[Iterable[str]] = None,
            endpoints: Optional[EndpointsContainer] = None
    ) -> None:
        """
        Removes the endpoint from the service.

        :param paths: The paths for the endpoint.
        :param endpoints: The commands to run.
        """

        if paths is not None:
            for path in paths:
                self.remove_endpoint(path=path)
            # end if

        else:
            for endpoint in endpoints:
                self.remove_endpoint(endpoint=endpoint)
            # end for
        # end if
    # end remove_endpoint

    def remove_all_endpoints(self) -> None:
        """Removes all the endpoints from the service."""

        self.endpoints.clear()
    # end remove_all_endpoints

    def set_endpoints(self, endpoints: EndpointsContainer) -> None:
        """
        Adds the endpoint to the service.

        :param endpoints: The commands to run.
        """

        self.endpoints: Endpoints = self.valid_endpoints(endpoints)
    # end set_endpoints

    def build(self) -> None:
        """
        Builds the service endpoints.

        :returns: The app object.
        """

        self.app = FastAPI(
            title=self.name,
            description=self.description,
            version=self.version,
            docs_url=None
        )

        router = APIRouter()

        for endpoint in self.endpoints.values():
            endpoint.set_root(self.root)

            path = ("/" + endpoint.root if endpoint.root else '') + endpoint.path

            command = override_signature(
                partial(endpoint.__call__, endpoint),
                new=endpoint.endpoint
            )

            try:
                router.add_api_route(
                    path, command,
                    methods=endpoint.methods, description=endpoint.description,
                    **endpoint.options
                )

            except fastapi.exceptions.FastAPIError:
                endpoint.options.setdefault('response_model', None)

                router.add_api_route(
                    path, command,
                    methods=endpoint.methods, description=endpoint.description,
                    **endpoint.options
                )
            # end try
        # end for

        if (self.icon is not None) and os.path.exists(self.icon):
            router.add_api_route(
                ("/" + self.root if self.root else '') + FAVICON,
                lambda: EndpointFileResponse(self.icon),
                methods=[GET], include_in_schema=False
            )
        # end if

        if isinstance(self.home, bool) and self.home:
            router.add_api_route(
                ("/" + self.root if self.root else '') + '/',
                lambda: EndpointRedirectResponse(DOCS),
                methods=[GET], include_in_schema=False
            )
        # end if

        if DOCS not in self.endpoints:
            router.add_api_route(
                ("/" + self.root if self.root else '') + DOCS,
                DocsEndpoint(
                    icon=("/" + self.root if self.root else '') + FAVICON,
                    methods=[GET], title=self.name
                ).endpoint, methods=[GET], include_in_schema=False
            )
        # end if

        self.app.include_router(router)
    # end build

    def create(
            self,
            host: Optional[Host] = None,
            port: Optional[Port] = None,
            silent: Optional[bool] = None,
            daemon: Optional[bool] = True
    ) -> None:
        """
        Creates the process to run the api service.

        :param host: The host of the server.
        :param port: The port of the server.
        :param silent: The value to silent the output.
        :param daemon: The value to set the process as daemon.
        """

        if silent is None:
            silent = self.SILENT
        # end if

        if not self.built():
            self.build()
        # end if

        server = Server(
            config=ServiceConfig(
                app=self.app, host=host, port=port
            )
        )

        self.service_process = threading.Thread(
            target=lambda: (
                (
                    logging.disable(logging.INFO) if silent else ()
                ), server.run()
            ), daemon=daemon
        )
    # end create

    def run(
            self,
            host: Optional[Host] = None,
            port: Optional[Port] = None,
            silent: Optional[bool] = None,
            daemon: Optional[bool] = True,
            block: Optional[bool] = False,
            timeout: Optional[Union[int, float, dt.timedelta, dt.datetime]] = None
    ) -> Optional[threading.Thread]:
        """
        Runs the api service.

        :param host: The host of the server.
        :param port: The port of the server.
        :param silent: The value to silent the output.
        :param daemon: The value to set the process as daemon.
        :param block: The value to block the execution and wain for the service.
        :param timeout: The timeout for the process.
        """

        process = None

        if self.running():
            return
        # end if

        if self.service_process is None:
            self.create(
                host=host, port=port, silent=silent,
                daemon=daemon
            )
        # end if

        self.service_process.start()

        if block:
            self.block = True
        # end if

        if timeout:
            process = self.timeout(timeout)
        # end if

        while self.blocked():
            pass
        # end while

        return process
    # end run

    def rerun(
            self,
            host: Optional[Host] = None,
            port: Optional[Port] = None,
            silent: Optional[bool] = None,
            daemon: Optional[bool] = True,
            block: Optional[bool] = False,
            timeout: Optional[Union[int, dt.timedelta, dt.datetime]] = None
    ) -> Optional[threading.Thread]:
        """
        Runs the api service.

        :param host: The host of the server.
        :param port: The port of the server.
        :param silent: The value to silent the output.
        :param daemon: The value to set the process as daemon.
        :param block: The value to block the execution and wain for the service.
        :param timeout: The timeout for the process.
        """

        if self.running():
            self.terminate()
        # end if

        return self.run(
            host=host, port=port, silent=silent,
            daemon=daemon, block=block, timeout=timeout
        )
    # end run

    def timeout(
            self,
            timeout: Union[int, float, dt.timedelta, dt.datetime],
            block: Optional[bool] = False
    ) -> Optional[threading.Thread]:
        """
        Waits to terminate the process.

        :param timeout: The amount of seconds to wait before termination.
        :param block: The value to block the process.
        """

        if isinstance(timeout, dt.datetime):
            timeout = timeout - dt.datetime.now()
        # end if

        if isinstance(timeout, dt.timedelta):
            timeout = timeout.total_seconds()
        # end if

        if block:
            time.sleep(timeout)

            self.terminate()

        else:
            self.timeout_process = threading.Thread(
                target=lambda: (time.sleep(timeout), self.terminate())
            )

            self.timeout_process.start()

            return self.timeout_process
        # end if
    # end timeout

    def terminate(self) -> None:
        """Pauses the process of service."""

        if not self.running():
            return
        # end if

        if isinstance(self.service_process, threading.Thread):
            terminate_thread(self.service_process)

            self.service_process = None
        # end if
    # end terminate

    def running(self) -> bool:
        """
        Checks if the service is currently running.

        :return: The boolean value.
        """

        if self.created:
            return False
        # end if

        return self.service_process.is_alive()
    # end running

    def built(self) -> bool:
        """
        Checks if the service was built.

        :return: The value for the service being built.
        """

        return isinstance(self.app, FastAPI)
    # end built

    def created(self) -> bool:
        """
        Checks if the service was created.

        :return: The value for the service being created.
        """

        return isinstance(self.service_process, threading.Thread)
    # end created
# end BaseService