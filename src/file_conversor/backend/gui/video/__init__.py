# src/file_conversor/backend/gui/video/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.video.index import video_index

routes = [
    FlaskRoute(
        rule="/video",
        handler=video_index
    )
]

__all__ = ['routes']
