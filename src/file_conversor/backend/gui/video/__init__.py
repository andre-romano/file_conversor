# src/file_conversor/backend/gui/video/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.video._index import video_index

from file_conversor.backend.gui.video.check import video_check
from file_conversor.backend.gui.video.compress import video_compress
from file_conversor.backend.gui.video.convert import video_convert
from file_conversor.backend.gui.video.enhance import video_enhance
from file_conversor.backend.gui.video.info import video_info
from file_conversor.backend.gui.video.mirror import video_mirror
from file_conversor.backend.gui.video.resize import video_resize
from file_conversor.backend.gui.video.rotate import video_rotate


def routes():
    return [
        FlaskRoute(
            rule="/video",
            handler=video_index,
        ),
        # TOOLS
        FlaskRoute(
            rule="/video/check",
            handler=video_check,
        ),
        FlaskRoute(
            rule="/video/compress",
            handler=video_compress,
        ),
        FlaskRoute(
            rule="/video/convert",
            handler=video_convert,
        ),
        FlaskRoute(
            rule="/video/enhance",
            handler=video_enhance,
        ),
        FlaskRoute(
            rule="/video/info",
            handler=video_info,
        ),
        FlaskRoute(
            rule="/video/mirror",
            handler=video_mirror,
        ),
        FlaskRoute(
            rule="/video/resize",
            handler=video_resize,
        ),
        FlaskRoute(
            rule="/video/rotate",
            handler=video_rotate,
        ),
    ]


__all__ = [
    'video_index',
    'video_check',
    'video_compress',
    'video_convert',
    'video_enhance',
    'video_info',
    'video_mirror',
    'video_resize',
    'video_rotate',

    'routes',
]
