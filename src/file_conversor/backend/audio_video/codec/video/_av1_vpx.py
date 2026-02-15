# src\file_conversor\backend\audio_video\codec\_vpx.py

import math

from enum import Enum
from typing import Any

# user-provided imports
from file_conversor.backend.audio_video.codec.video.ffmpeg_video_codec import FFmpegVideoCodec
from file_conversor.backend.audio_video.codec.video.__quality_opts_helper import QualityOptsHelper

# determine number of threads for encoding
_threads = FFmpegVideoCodec.get_cpu_count()


def _get_tile_column_option() -> dict[str, str]:
    # max 2 tile columns for VP9/AV1 (avoid quality loss)
    tile_column = min(int(math.log2(_threads)), 2)
    if tile_column <= 0:
        return {}
    return {"-tile-columns": str(tile_column)}


class Av1VpxCodecs(Enum):
    # LIB codecs
    VP8_LIB = "libvpx"
    VP9_LIB = "libvpx-vp9"
    AV1_LIB = "libaom-av1"

    # QSV codecs
    VP8_QSV = "vp8_qsv"
    VP9_QSV = "vp9_qsv"
    AV1_QSV = "av1_qsv"

    # VAAPI
    VP8_VAAPI = "vp8_vaapi"
    VP9_VAAPI = "vp9_vaapi"
    AV1_VAAPI = "av1_vaapi"

    # NVENC - only AV1
    AV1_NVENC = "av1_nvenc"

    @property
    def codec(self) -> FFmpegVideoCodec:
        return FFmpegVideoCodec(self.value,
                                options=self.options,
                                quality_setting_opts=self.quality_options,
                                encoding_speed_opts=self.encoding_speed_options,
                                )

    @property
    def options(self) -> dict[str, Any]:
        match self:
            case self.VP8_LIB:
                return {
                    "-threads": _threads,
                }
            case self.VP9_LIB | self.AV1_LIB:
                return {
                    "-threads": _threads,  # set number of threads
                    **_get_tile_column_option(),  # set tile columns based on CPU threads
                    "-row-mt": "1",  # enable row-based multi-threading
                }
            case _:
                return {}

    @property
    def quality_options(self) -> dict[FFmpegVideoCodec.QualitySetting, dict[str, Any]]:
        match self:
            case self.VP8_LIB:
                return QualityOptsHelper.LIB.get(high="6", medium="15", low="28", options={"-b:v": "0"})
            case self.VP9_LIB:
                return QualityOptsHelper.LIB.get(high="17", medium="30", low="40", options={"-b:v": "0"})
            case self.AV1_LIB:
                return QualityOptsHelper.LIB.get(high="22", medium="30", low="39", options={"-b:v": "0"})

            case self.VP8_QSV:
                return QualityOptsHelper.QSV.get(high="10", medium="19", low="34")
            case self.VP9_QSV:
                return QualityOptsHelper.QSV.get(high="16", medium="26", low="36")
            case self.AV1_QSV:
                return QualityOptsHelper.QSV.get(high="20", medium="26", low="33")

            case self.VP8_VAAPI:
                return QualityOptsHelper.VAAPI.get(high="12", medium="23", low="37")
            case self.VP9_VAAPI:
                return QualityOptsHelper.VAAPI.get(high="18", medium="28", low="39")
            case self.AV1_VAAPI:
                return QualityOptsHelper.VAAPI.get(high="24", medium="32", low="40")

            case self.AV1_NVENC:
                return QualityOptsHelper.NVENC.get(high="20", medium="26", low="33")

    @property
    def encoding_speed_options(self) -> dict[FFmpegVideoCodec.EncodingSetting, dict[str, Any]]:
        match self:
            # LIB codecs
            case self.VP8_LIB | self.VP9_LIB:
                return {
                    FFmpegVideoCodec.EncodingSetting.FAST: {"-cpu-used": "6"},
                    FFmpegVideoCodec.EncodingSetting.MEDIUM: {"-cpu-used": "4"},
                    FFmpegVideoCodec.EncodingSetting.SLOW: {"-cpu-used": "2"},
                }
            case self.AV1_LIB:
                return {
                    FFmpegVideoCodec.EncodingSetting.FAST: {"-cpu-used": "7"},
                    FFmpegVideoCodec.EncodingSetting.MEDIUM: {"-cpu-used": "6"},
                    FFmpegVideoCodec.EncodingSetting.SLOW: {"-cpu-used": "5"},
                }

            # QSV codecs
            case self.VP8_QSV | self.VP9_QSV | self.AV1_QSV:
                return {
                    FFmpegVideoCodec.EncodingSetting.FAST: {"-preset": "faster"},
                    FFmpegVideoCodec.EncodingSetting.MEDIUM: {"-preset": "medium"},
                    FFmpegVideoCodec.EncodingSetting.SLOW: {"-preset": "slower"},
                }

            # VAAPI codecs - no encoding speed options available
            case self.VP8_VAAPI | self.VP9_VAAPI | self.AV1_VAAPI:
                return {}

            # NVENC - only AV1 - preset options available
            case self.AV1_NVENC:
                return {
                    FFmpegVideoCodec.EncodingSetting.FAST: {"-preset": "p3"},
                    FFmpegVideoCodec.EncodingSetting.MEDIUM: {"-preset": "p4"},
                    FFmpegVideoCodec.EncodingSetting.SLOW: {"-preset": "p5"},
                }


__all__ = [
    "Av1VpxCodecs",
]
