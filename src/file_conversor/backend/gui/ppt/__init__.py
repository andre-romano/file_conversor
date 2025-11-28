# src/file_conversor/backend/gui/ppt/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.ppt._index import ppt_index

from file_conversor.backend.gui.ppt.convert import ppt_convert


def routes():
    return [
        FlaskRoute(
            rule="/ppt",
            handler=ppt_index,
        ),
        # TOOLS
        FlaskRoute(
            rule="/ppt/convert",
            handler=ppt_convert,
        ),
    ]


__all__ = [
    'ppt_index',
    'ppt_convert',

    'routes',
]
