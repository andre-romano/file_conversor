# src\file_conversor\gui\flask_route.py

from typing import Any, Callable, Self


class FlaskRoute:
    _routes: set["FlaskRoute"] = set()

    @classmethod
    def register(cls, route: str, **options: Any):
        def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
            flask_route = FlaskRoute(route, f, **options)
            if flask_route in cls._routes:
                raise ValueError(f"Route '{route}' is already registered.")
            cls._routes.add(flask_route)
            return f
        return decorator

    @classmethod
    def get_routes(cls):
        return cls._routes

    def __init__(self, route: str, handler: Callable[..., Any], **options: Any) -> None:
        super().__init__()
        self.route = route
        self.handler = handler
        self.options = options

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, FlaskRoute):
            return NotImplemented
        return self.route == value.route

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

    def __hash__(self) -> int:
        return hash(self.route)

    def __repr__(self) -> str:
        return f"FlaskRoute(route={self.route}, handler={self.handler.__name__}, options={self.options})"

    def __str__(self) -> str:
        return f"{self.route} -> {self.handler.__name__} ({self.options})"
