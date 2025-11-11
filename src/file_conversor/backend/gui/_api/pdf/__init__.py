# src/file_conversor/backend/gui/_api/pdf/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.pdf.compress import api_pdf_compress
from file_conversor.backend.gui._api.pdf.convert import api_pdf_convert
from file_conversor.backend.gui._api.pdf.decrypt import api_pdf_decrypt
from file_conversor.backend.gui._api.pdf.encrypt import api_pdf_encrypt
from file_conversor.backend.gui._api.pdf.extract_img import api_pdf_extract_img
from file_conversor.backend.gui._api.pdf.extract import api_pdf_extract
from file_conversor.backend.gui._api.pdf.merge import api_pdf_merge
from file_conversor.backend.gui._api.pdf.ocr import api_pdf_ocr
from file_conversor.backend.gui._api.pdf.repair import api_pdf_repair
from file_conversor.backend.gui._api.pdf.rotate import api_pdf_rotate
from file_conversor.backend.gui._api.pdf.split import api_pdf_split


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
        FlaskRoute(
            rule="/api/pdf/extract_img",
            handler=api_pdf_extract_img,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/pdf/extract",
            handler=api_pdf_extract,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/pdf/merge",
            handler=api_pdf_merge,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/pdf/ocr",
            handler=api_pdf_ocr,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/pdf/repair",
            handler=api_pdf_repair,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/pdf/rotate",
            handler=api_pdf_rotate,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/pdf/split",
            handler=api_pdf_split,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
