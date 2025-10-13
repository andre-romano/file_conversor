# src/file_conversor/backend/gui/pipeline/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.pipeline._index import pipeline_index

from file_conversor.backend.gui.pipeline.create import pipeline_create
from file_conversor.backend.gui.pipeline.execute import pipeline_execute


def routes():
    return [
        FlaskRoute(
            rule="/pipeline",
            handler=pipeline_index,
        ),
        # TOOLS
        FlaskRoute(
            rule="/pipeline/create",
            handler=pipeline_create,
        ),
        FlaskRoute(
            rule="/pipeline/execute",
            handler=pipeline_execute,
        ),
    ]


__all__ = ['routes']
