# src/file_conversor/backend/gui/_api/hash/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.hash.check import api_hash_check
from file_conversor.backend.gui._api.hash.create import api_hash_create


def routes():
    return [
        FlaskRoute(
            rule="/api/hash/check",
            handler=api_hash_check,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/hash/create",
            handler=api_hash_create,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
