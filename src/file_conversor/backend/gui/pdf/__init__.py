# src/file_conversor/backend/gui/pdf/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.pdf._index import pdf_index

from file_conversor.backend.gui.pdf.compress import pdf_compress
from file_conversor.backend.gui.pdf.convert import pdf_convert
from file_conversor.backend.gui.pdf.decrypt import pdf_decrypt
from file_conversor.backend.gui.pdf.encrypt import pdf_encrypt
from file_conversor.backend.gui.pdf.extract_img import pdf_extract_img
from file_conversor.backend.gui.pdf.extract import pdf_extract
from file_conversor.backend.gui.pdf.merge import pdf_merge
from file_conversor.backend.gui.pdf.ocr import pdf_ocr
from file_conversor.backend.gui.pdf.repair import pdf_repair
from file_conversor.backend.gui.pdf.rotate import pdf_rotate
from file_conversor.backend.gui.pdf.split import pdf_split


def routes():
    return [
        FlaskRoute(
            rule="/pdf",
            handler=pdf_index,
        ),

        # TOOLS
        FlaskRoute(
            rule="/pdf/compress",
            handler=pdf_compress,
        ),
        FlaskRoute(
            rule="/pdf/convert",
            handler=pdf_convert,
        ),
        FlaskRoute(
            rule="/pdf/decrypt",
            handler=pdf_decrypt,
        ),
        FlaskRoute(
            rule="/pdf/encrypt",
            handler=pdf_encrypt,
        ),
        FlaskRoute(
            rule="/pdf/extract_img",
            handler=pdf_extract_img,
        ),
        FlaskRoute(
            rule="/pdf/extract",
            handler=pdf_extract,
        ),
        FlaskRoute(
            rule="/pdf/merge",
            handler=pdf_merge,
        ),
        FlaskRoute(
            rule="/pdf/ocr",
            handler=pdf_ocr,
        ),
        FlaskRoute(
            rule="/pdf/repair",
            handler=pdf_repair,
        ),
        FlaskRoute(
            rule="/pdf/rotate",
            handler=pdf_rotate,
        ),
        FlaskRoute(
            rule="/pdf/split",
            handler=pdf_split,
        ),
    ]


__all__ = [
    'pdf_index',
    'pdf_compress',
    'pdf_convert',
    'pdf_decrypt',
    'pdf_encrypt',
    'pdf_extract_img',
    'pdf_extract',
    'pdf_merge',
    'pdf_ocr',
    'pdf_repair',
    'pdf_rotate',
    'pdf_split',

    'routes',
]
