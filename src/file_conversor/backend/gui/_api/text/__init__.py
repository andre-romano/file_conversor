# src/file_conversor/backend/gui/_api/text/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.text.check import api_text_check
from file_conversor.backend.gui._api.text.compress import api_text_compress
from file_conversor.backend.gui._api.text.convert import api_text_convert


def routes():
    return [
        FlaskRoute(
            rule="/api/text/check",
            handler=api_text_check,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/text/compress",
            handler=api_text_compress,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/text/convert",
            handler=api_text_convert,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
