# src/file_conversor/backend/gui/_api/image/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.image.antialias import api_image_antialias
from file_conversor.backend.gui._api.image.blur import api_image_blur
from file_conversor.backend.gui._api.image.compress import api_image_compress
from file_conversor.backend.gui._api.image.convert import api_image_convert
from file_conversor.backend.gui._api.image.enhance import api_image_enhance
from file_conversor.backend.gui._api.image.filter import api_image_filter
from file_conversor.backend.gui._api.image.info import api_image_info
from file_conversor.backend.gui._api.image.mirror import api_image_mirror
from file_conversor.backend.gui._api.image.render import api_image_render
from file_conversor.backend.gui._api.image.resize import api_image_resize
from file_conversor.backend.gui._api.image.rotate import api_image_rotate
from file_conversor.backend.gui._api.image.to_pdf import api_image_to_pdf
from file_conversor.backend.gui._api.image.unsharp import api_image_unsharp


def routes():
    return [
        FlaskRoute(
            rule="/api/image/antialias",
            handler=api_image_antialias,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/blur",
            handler=api_image_blur,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/compress",
            handler=api_image_compress,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/convert",
            handler=api_image_convert,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/enhance",
            handler=api_image_enhance,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/filter",
            handler=api_image_filter,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/info",
            handler=api_image_info,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/mirror",
            handler=api_image_mirror,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/render",
            handler=api_image_render,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/resize",
            handler=api_image_resize,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/rotate",
            handler=api_image_rotate,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/to_pdf",
            handler=api_image_to_pdf,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/image/unsharp",
            handler=api_image_unsharp,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
