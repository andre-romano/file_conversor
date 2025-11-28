# src/file_conversor/backend/gui/xls/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.xls._index import xls_index

from file_conversor.backend.gui.xls.convert import xls_convert


def routes():
    return [
        FlaskRoute(
            rule="/xls",
            handler=xls_index
        ),
        # TOOLS
        FlaskRoute(
            rule="/xls/convert",
            handler=xls_convert
        ),
    ]


__all__ = [
    'xls_index',
    'xls_convert',

    'routes',
]
