# src/file_conversor/backend/gui/pipeline/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.pipeline.index import pipeline_index

routes = [
    FlaskRoute(
        rule="/pipeline",
        handler=pipeline_index
    )
]

__all__ = ['routes']
