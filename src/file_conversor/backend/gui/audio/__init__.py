# src/file_conversor/backend/gui/audio/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.audio.index import audio_index

routes = [
    FlaskRoute(
        rule="/audio",
        handler=audio_index
    )
]

__all__ = ['routes']
