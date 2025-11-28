# src/file_conversor/backend/gui/hash/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.hash._index import hash_index

from file_conversor.backend.gui.hash.check import hash_check
from file_conversor.backend.gui.hash.create import hash_create


def routes():
    return [
        FlaskRoute(
            rule="/hash",
            handler=hash_index
        ),
        FlaskRoute(
            rule="/hash/check",
            handler=hash_check
        ),
        FlaskRoute(
            rule="/hash/create",
            handler=hash_create
        ),
    ]


__all__ = [
    'hash_index',
    'hash_check',
    'hash_create',

    'routes',
]
