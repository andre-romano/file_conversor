# src/file_conversor/backend/gui/image/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.image._index import image_index

from file_conversor.backend.gui.image.antialias import image_antialias
from file_conversor.backend.gui.image.blur import image_blur
from file_conversor.backend.gui.image.compress import image_compress
from file_conversor.backend.gui.image.convert import image_convert
from file_conversor.backend.gui.image.enhance import image_enhance
from file_conversor.backend.gui.image.filter import image_filter
from file_conversor.backend.gui.image.info import image_info
from file_conversor.backend.gui.image.mirror import image_mirror
from file_conversor.backend.gui.image.render import image_render
from file_conversor.backend.gui.image.resize import image_resize
from file_conversor.backend.gui.image.rotate import image_rotate
from file_conversor.backend.gui.image.to_pdf import image_to_pdf
from file_conversor.backend.gui.image.unsharp import image_unsharp


def routes():
    return [
        FlaskRoute(
            rule="/image",
            handler=image_index,
        ),
        FlaskRoute(
            rule="/image/convert",
            handler=image_convert,
        ),
        FlaskRoute(
            rule="/image/render",
            handler=image_render,
        ),
        FlaskRoute(
            rule="/image/to_pdf",
            handler=image_to_pdf,
        ),
        FlaskRoute(
            rule="/image/compress",
            handler=image_compress,
        ),
        FlaskRoute(
            rule="/image/mirror",
            handler=image_mirror,
        ),
        FlaskRoute(
            rule="/image/rotate",
            handler=image_rotate,
        ),
        FlaskRoute(
            rule="/image/resize",
            handler=image_resize,
        ),
        FlaskRoute(
            rule="/image/antialias",
            handler=image_antialias,
        ),
        FlaskRoute(
            rule="/image/blur",
            handler=image_blur,
        ),
        FlaskRoute(
            rule="/image/enhance",
            handler=image_enhance,
        ),
        FlaskRoute(
            rule="/image/filter",
            handler=image_filter,
        ),
        FlaskRoute(
            rule="/image/unsharp",
            handler=image_unsharp,
        ),
        FlaskRoute(
            rule="/image/info",
            handler=image_info,
        ),
    ]


__all__ = [
    'image_index',
    'image_antialias',
    'image_blur',
    'image_compress',
    'image_convert',
    'image_enhance',
    'image_filter',
    'image_info',
    'image_mirror',
    'image_render',
    'image_resize',
    'image_rotate',
    'image_to_pdf',
    'image_unsharp',

    'routes',
]
