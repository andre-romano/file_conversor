# src/file_conversor/backend/gui/_api/pdf/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.pdf.compress import api_pdf_compress
from file_conversor.backend.gui._api.pdf.convert import api_pdf_convert
from file_conversor.backend.gui._api.pdf.decrypt import api_pdf_decrypt
from file_conversor.backend.gui._api.pdf.encrypt import api_pdf_encrypt


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
        FlaskRoute(
            rule="/api/pdf/decrypt",
            handler=api_pdf_decrypt,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/pdf/encrypt",
            handler=api_pdf_encrypt,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
