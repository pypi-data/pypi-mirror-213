# backend.py

import datetime as dt
from functools import wraps
from typing import (
    List, Any, Union, Dict, Optional,
    Tuple, Callable, Iterable
)

from fastapi.openapi.docs import get_swagger_ui_html

from represent import Modifiers, BaseModel

from live_api.endpoints.process import copy
from live_api.endpoints.data import DOCS

__all__ = [
    "BaseEndpoint",
    "DocsEndpoint",
    "Record",
    "DataContainer",
    "valid_endpoints"
]

class Record(BaseModel):
    """A class to represent a result object for commands and conditions calls."""

    def __init__(
            self, *,
            args: Optional[Tuple] = None,
            kwargs: Optional[Dict[str, Any]] = None,
            returns: Optional[Any] = None
    ) -> None:
        """
        Defines the class attributes.

        :param args: The positional arguments.
        :param kwargs: The keyword arguments.
        :param returns: The returned values.
        """

        self.args = args or ()
        self.kwargs = kwargs or {}
        self.returns = returns
    # end __init__

    def collect(
            self, *,
            args: Optional[Tuple] = None,
            kwargs: Optional[Dict[str, Any]] = None,
            returns: Optional[Any] = None
    ) -> None:
        """
        Defines the class attributes.

        :param args: The positional arguments.
        :param kwargs: The keyword arguments.
        :param returns: The returned values.
        """

        self.args = args
        self.kwargs.update(kwargs)
        self.returns = returns
    # end collect
# end Record

Requests = List[Record]

class DataContainer(BaseModel, dict):
    """A class to represent a data container."""

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Sets the attribute.

        :param key: The key to the attribute.
        :param value: The value of the attribute.
        """

        self[key] = value

        super().__setattr__(key, value)
    # end __setattr__

    def copy(self):
        """
        Copies the data of the model.

        :return: The copy of the model.
        """

        data: DataContainer = copy(self)

        return data
    # end copy

    def update(self, config: Dict[str, Any], **kwargs: Any) -> None:
        """
        Updates the object's data with the config.

        :param config: The config object.
        :param kwargs: Any keyword arguments.
        """

        if isinstance(config, type(self)):
            config = config.__dict__
        # end if

        if isinstance(config, dict):
            for key in self.__dict__.keys():
                if key in config:
                    setattr(self, key, config[key])
                # end if
            # end for
        # end if

        super().update(config, **kwargs)
    # end update
# end DataContainer

class BaseEndpoint(BaseModel):
    """
    A class to represent an endpoint.

    The BaseEndpoint is a command class that is the base of custom
    endpoint classes. Custom endpoint classes inherit from BaseEndpoint
    to add the command to execute when the endpoint is requested
    by a client, through the API of a service object.

    The endpoint method is implemented in child classes.

    All the returned values and parameters end endpoint collects through
    its lifetime are stored as AssistantResponse and Request objects at the internal
    record of the object.

    data attributes:

    - io:
        The configuration for saving and loading data and attributes
        that are none-mandatory to load and save. When given to False,
        The io object will have no keys inside it.

    - methods:
        A list of API endpoint methods that the endpoint should be
        able to operate with.

    - path:
        The path to the endpoint through the api.

    - root:
        The root of the path to the endpoint, when not ''.

    >>> from live_api.endpoints import BaseEndpoint, GET
    >>>
    >>> class MyEndpoint(BaseEndpoint):
    >>>     ...
    >>>
    >>>     def endpoint(self, *args: Any, **kwargs: Any) -> Any:
    >>>         ...
    >>>
    >>> endpoint = MyEndpoint(path="/<ENDPOINT PATH IN URL>", methods=[GET])
    # end AnswerEndpoint
    """

    modifiers = Modifiers(
        excluded=["service", "options", "record", "modifiers"]
    )

    PATH: str
    METHODS: List[str]

    def __init__(
            self,
            path: Optional[str] = None,
            methods: Optional[Iterable[str]] = None,
            service: Optional[object] = None,
            description: Optional[str] = None,
            root: Optional[str] = None,
            options: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param path: The path to the endpoint.
        :param methods: The endpoint methods.
        :param description: The description of the object.
        :param root: The root to the path.
        :param options: Any keyword arguments.
        :param service: The service object.
        """

        self.record: Requests = []

        self.options = options or {}

        self.path = str(path or self.PATH)
        self.root = root or ""
        self.description = description

        self.methods = list(methods or self.METHODS)

        self.service = service
    # end __init__

    def __call__(self, *args: Any, **kwargs: Any) -> Dict[str, Union[int, Any]]:
        """
        Returns the function to command the command.

        :param name: The intent that activated the command.
        :param message: The message for the intent.

        :return: The function to command the command.
        """

        start = dt.datetime.now()

        result = self.process(self.wrap(self.endpoint)(*args, **kwargs))

        end = dt.datetime.now()

        return dict(response=result, time=(end - start).total_seconds())
    # end __call__

    @staticmethod
    def call(instance) -> Callable:
        """
        Returns the function to command the command.

        :param instance: An instance of the class.

        :return: The function to command the command.
        """

        return instance.__call__
    # end __call__

    def process(self, response: Any) -> Any:
        """
        Processes the response of the endpoint.

        :param response: The endpoint response to process.

        :return: The processed response.
        """

        dir(self)

        return response
    # end process

    def wrap(self, endpoint: Callable[..., Any]) -> Any:
        """
        Processes the response of the endpoint.

        :param endpoint: The endpoint to process.

        :return: The processed response.
        """

        dir(self)

        @wraps(endpoint)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Returns the response for the API endpoint.

            :param args: The positional arguments.
            :param kwargs: Any keyword argument.

            :return: The response from the function call.
            """

            return endpoint(*args[1:], **kwargs)
        # end wrapper

        return wrapper
    # end process

    def set_root(self, root: str, /) -> None:
        """
        Sets the root path of the endpoint.

        :param root: The root path.
        """

        self.root = root
    # end set_root

    def get_root(self) -> str:
        """
        Gets the root path of the endpoint.

        :returns: The root path.
        """

        return self.root
    # end get_root

    def endpoint(self, *args: Any, **kwargs: Any) -> Any:
        """
        Returns the response for the API endpoint.

        :param args: The positional arguments.
        :param kwargs: Any keyword argument.

        :return: The response from the function call.
        """
    # end endpoint
# end BaseEndpoint

class DocsEndpoint(BaseEndpoint):
    """A class to represent an endpoint."""

    def __init__(
            self,
            methods: Optional[Iterable[str]] = None,
            service: Optional[object] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            icon: Optional[str] = None,
            options: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param methods: The endpoint methods.
        :param description: The description of the object.
        :param icon: The icon file path.
        :param title: The endpoint title.
        :param options: Any keyword arguments.
        :param service: The service object.
        """

        self.title = title
        self.icon = icon

        BaseEndpoint.__init__(
            self, path=DOCS, methods=methods, service=service,
            description=description, options=options
        )
    # end __init__

    def endpoint(self) -> Any:
        """
        Returns the response for the API endpoint.

        :return: The response from the function call.
        """

        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=(
                self.title + " - Service Docs"
                if self.title is not None else "Service Docs"
            ),
            swagger_favicon_url=(
                self.icon if self.icon is not None else
                "https://fastapi.tiangolo.com/img/favicon.png"
            )
        )
    # end answer
# end DocsEndpoint

def valid_endpoints(endpoints: Optional[Any] = None) -> Dict[str, BaseEndpoint]:
    """
    Process the endpoints' commands to validate and modify it.

    :param endpoints: The endpoints object to check.

    :return: The valid endpoints object.
    """

    if endpoints is None:
        endpoints = {}

    elif isinstance(endpoints, dict):
        endpoints = {**endpoints}

    else:
        try:
            endpoints = {
                endpoint.path: endpoint for endpoint in endpoints
            }

        except ValueError:
            raise ValueError(
                f"Endpoints parameter must be either a dictionary "
                f"with paths as keys and endpoint objects with matching "
                f"paths as values, or an iterable object with endpoint objects, "
                f"not: {endpoints}"
            )
        # end try
    # end if

    return endpoints
# end valid_endpoints