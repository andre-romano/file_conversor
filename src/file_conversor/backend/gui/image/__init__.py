# src/file_conversor/backend/gui/image/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.image.index import image_index

routes = [
    FlaskRoute(
        rule="/image",
        handler=image_index
    )
]

__all__ = ['routes']
