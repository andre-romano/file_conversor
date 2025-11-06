# src/file_conversor/backend/gui/_api/image/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.image.convert import api_image_convert


def routes():
    return [
        FlaskRoute(
            rule="/api/image/convert",
            handler=api_image_convert,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
