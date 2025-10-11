# src/file_conversor/backend/gui/win/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.win.index import win_index

routes = [
    FlaskRoute(
        rule="/win",
        handler=win_index
    )
]

__all__ = ['routes']
