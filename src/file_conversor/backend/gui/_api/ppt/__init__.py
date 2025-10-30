# src/file_conversor/backend/gui/_api/ppt/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.ppt.convert import api_ppt_convert


def routes():
    return [
        FlaskRoute(
            rule="/api/ppt/convert",
            handler=api_ppt_convert,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
