# src/file_conversor/backend/audio_video/codec/video/_get_quality_opts.py

from enum import Enum

# user-provided imports
from file_conversor.backend.audio_video.codec.video.ffmpeg_video_codec import FFmpegVideoCodec


class QualityOptsHelper(Enum):
    LIB = "lib"
    QSV = "qsv"
    VAAPI = "vaapi"
    NVENC = "nvenc"

    def get(
        self,
        high: str,
        medium: str,
        low: str,
        options: dict[str, str] | None = None,
    ) -> dict[FFmpegVideoCodec.QualitySetting, dict[str, str]]:
        options = options or {}

        option_flag: str
        match self:
            case QualityOptsHelper.LIB:
                option_flag = "-crf"
            case QualityOptsHelper.QSV:
                option_flag = "-global_quality"
            case QualityOptsHelper.NVENC:
                option_flag = "-cq"
            case QualityOptsHelper.VAAPI:
                option_flag = "-qp"

        return {
            FFmpegVideoCodec.QualitySetting.HIGH: {option_flag: high, **options},
            FFmpegVideoCodec.QualitySetting.MEDIUM: {option_flag: medium, **options},
            FFmpegVideoCodec.QualitySetting.LOW: {option_flag: low, **options},
        }


__all__ = [
    "QualityOptsHelper",
]
