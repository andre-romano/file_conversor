# src/file_conversor/backend/gui/_api/pdf/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.pdf.compress import api_pdf_compress
from file_conversor.backend.gui._api.pdf.convert import api_pdf_convert


def routes():
    return [
        FlaskRoute(
            rule="/api/pdf/compress",
            handler=api_pdf_compress,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/pdf/convert",
            handler=api_pdf_convert,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
