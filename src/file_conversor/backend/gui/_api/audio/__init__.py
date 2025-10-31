# src/file_conversor/backend/gui/_api/audio/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.audio.check import api_audio_check


def routes():
    return [
        FlaskRoute(
            rule="/api/audio/check",
            handler=api_audio_check,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
