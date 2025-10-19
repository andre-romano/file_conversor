# src/file_conversor/backend/gui/_api/doc/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.doc.convert import api_doc_convert


def routes():
    return [
        FlaskRoute(
            rule="/api/doc/convert",
            handler=api_doc_convert,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
