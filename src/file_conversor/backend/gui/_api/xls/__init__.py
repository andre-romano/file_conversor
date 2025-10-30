# src/file_conversor/backend/gui/_api/xls/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.xls.convert import api_xls_convert


def routes():
    return [
        FlaskRoute(
            rule="/api/xls/convert",
            handler=api_xls_convert,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
