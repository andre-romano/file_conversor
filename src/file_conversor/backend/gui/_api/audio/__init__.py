# src/file_conversor/backend/gui/_api/audio/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.audio.check import api_audio_check
from file_conversor.backend.gui._api.audio.convert import api_audio_convert
from file_conversor.backend.gui._api.audio.info import api_audio_info


def routes():
    return [
        FlaskRoute(
            rule="/api/audio/check",
            handler=api_audio_check,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/audio/convert",
            handler=api_audio_convert,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/audio/info",
            handler=api_audio_info,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
