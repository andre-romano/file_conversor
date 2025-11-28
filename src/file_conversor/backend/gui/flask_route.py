# src\file_conversor\backend\gui\flask_route.py

from flask import Flask
from typing import Any, Callable


class FlaskRoute:
    __routes: dict[str, "FlaskRoute"] = {}

    @classmethod
    def get_url(cls, func_or_name: Callable | str) -> str:
        """
        Gets the URL for a Flask endpoint function.

        :param func_or_endpoint: The Flask endpoint function or endpoint name.
        :return: The URL for the given endpoint.
        """
        func_name = func_or_name if isinstance(func_or_name, str) else func_or_name.__name__
        return cls.__routes[func_name].rule

    def __init__(self, rule: str, handler: Callable[..., Any], **options: Any) -> None:
        super().__init__()
        self.rule = rule
        self.handler = handler
        self.options = options

        # register route
        FlaskRoute.__routes[handler.__name__] = self

    def __hash__(self) -> int:
        return hash(self.rule)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, FlaskRoute):
            return NotImplemented
        return self.rule == value.rule

    def __repr__(self) -> str:
        return f"FlaskRoute(rule={self.rule}, options={self.options})"

    def __str__(self) -> str:
        return f"{self.rule}" + f"({self.options})" if self.options else ""

    def register(self, app: Flask) -> None:
        app.route(self.rule, **self.options)(self.handler)


__all__ = [
    "FlaskRoute",
]
