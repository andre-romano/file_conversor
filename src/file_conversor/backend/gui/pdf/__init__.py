# src/file_conversor/backend/gui/pdf/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.pdf.index import pdf_index

routes = [
    FlaskRoute(
        rule="/pdf",
        handler=pdf_index
    )
]

__all__ = ['routes']
