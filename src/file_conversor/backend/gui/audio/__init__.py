# src/file_conversor/backend/gui/audio/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.audio._index import audio_index

from file_conversor.backend.gui.audio.check import audio_check
from file_conversor.backend.gui.audio.convert import audio_convert
from file_conversor.backend.gui.audio.info import audio_info


def routes():
    return [
        FlaskRoute(
            rule="/audio",
            handler=audio_index
        ),
        FlaskRoute(
            rule="/audio/check",
            handler=audio_check,
        ),
        FlaskRoute(
            rule="/audio/convert",
            handler=audio_convert,
        ),
        FlaskRoute(
            rule="/audio/info",
            handler=audio_info,
        ),
    ]


__all__ = [
    'audio_index',
    'audio_check',
    'audio_convert',
    'audio_info',

    'routes',
]
