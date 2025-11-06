# src/file_conversor/backend/gui/_api/image/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.image.antialias import api_image_antialias
from file_conversor.backend.gui._api.image.blur import api_image_blur
from file_conversor.backend.gui._api.image.compress import api_image_compress
from file_conversor.backend.gui._api.image.convert import api_image_convert


def routes():
    return [
        FlaskRoute(
            rule="/api/image/antialias",
            handler=api_image_antialias,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/blur",
            handler=api_image_blur,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/compress",
            handler=api_image_compress,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/convert",
            handler=api_image_convert,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
