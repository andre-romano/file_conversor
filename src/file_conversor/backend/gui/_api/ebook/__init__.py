# src/file_conversor/backend/gui/_api/ebook/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.ebook.convert import api_ebook_convert


def routes():
    return [
        FlaskRoute(
            rule="/api/ebook/convert",
            handler=api_ebook_convert,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
