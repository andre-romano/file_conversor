# src/file_conversor/backend/gui/_api/video/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.video.check import api_video_check
from file_conversor.backend.gui._api.video.compress import api_video_compress
from file_conversor.backend.gui._api.video.convert import api_video_convert
from file_conversor.backend.gui._api.video.enhance import api_video_enhance
from file_conversor.backend.gui._api.video.info import api_video_info
from file_conversor.backend.gui._api.video.mirror import api_video_mirror
from file_conversor.backend.gui._api.video.resize import api_video_resize
from file_conversor.backend.gui._api.video.rotate import api_video_rotate


def routes():
    return [
        FlaskRoute(
            rule="/api/video/check",
            handler=api_video_check,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/video/compress",
            handler=api_video_compress,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/video/convert",
            handler=api_video_convert,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/video/enhance",
            handler=api_video_enhance,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/video/info",
            handler=api_video_info,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/video/mirror",
            handler=api_video_mirror,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/video/resize",
            handler=api_video_resize,
            methods=["POST"],
        ),
        FlaskRoute(
            rule="/api/video/rotate",
            handler=api_video_rotate,
            methods=["POST"],
        ),
    ]


__all__ = ['routes']
