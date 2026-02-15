# src\file_conversor\backend\audio_video\codec\video\__init__.py

from enum import Enum

from file_conversor.backend.audio_video.codec.video._av1_vpx import Av1VpxCodecs
from file_conversor.backend.audio_video.codec.video._h26x import H26xCodecs
from file_conversor.backend.audio_video.codec.video._mpeg import MpegCodecs
from file_conversor.backend.audio_video.codec.video.ffmpeg_video_codec import (
    FFmpegVideoCodec,
)


class FFmpegVideoCodecs(Enum):
    NULL = "null"
    COPY = "copy"

    # mpeg codecs
    MPEG4 = MpegCodecs.MPEG4.value

    # h264 codecs
    H264_LIB = H26xCodecs.H264_LIB.value
    H264_VAAPI = H26xCodecs.H264_VAAPI.value
    H264_QSV = H26xCodecs.H264_QSV.value
    H264_NVENC = H26xCodecs.H264_NVENC.value

    # h265 codecs
    H265_LIB = H26xCodecs.H265_LIB.value
    H265_VAAPI = H26xCodecs.H265_VAAPI.value
    H265_QSV = H26xCodecs.H265_QSV.value
    H265_NVENC = H26xCodecs.H265_NVENC.value

    # vp8 codecs
    VP8_LIB = Av1VpxCodecs.VP8_LIB.value
    VP8_VAAPI = Av1VpxCodecs.VP8_VAAPI.value
    VP8_QSV = Av1VpxCodecs.VP8_QSV.value

    # vp9 codecs
    VP9_LIB = Av1VpxCodecs.VP9_LIB.value
    VP9_VAAPI = Av1VpxCodecs.VP9_VAAPI.value
    VP9_QSV = Av1VpxCodecs.VP9_QSV.value

    # av1 codecs
    AV1_LIB = Av1VpxCodecs.AV1_LIB.value
    AV1_VAAPI = Av1VpxCodecs.AV1_VAAPI.value
    AV1_QSV = Av1VpxCodecs.AV1_QSV.value
    AV1_NVENC = Av1VpxCodecs.AV1_NVENC.value

    @property
    def codec(self) -> FFmpegVideoCodec:
        match self:
            case FFmpegVideoCodecs.NULL | FFmpegVideoCodecs.COPY:
                return FFmpegVideoCodec(self.value)
            case self.MPEG4:
                return MpegCodecs.MPEG4.codec

            # h264 codecs
            case self.H264_LIB:
                return H26xCodecs.H264_LIB.codec
            case self.H264_VAAPI:
                return H26xCodecs.H264_VAAPI.codec
            case self.H264_QSV:
                return H26xCodecs.H264_QSV.codec
            case self.H264_NVENC:
                return H26xCodecs.H264_NVENC.codec

            # h265 codecs
            case self.H265_LIB:
                return H26xCodecs.H265_LIB.codec
            case self.H265_VAAPI:
                return H26xCodecs.H265_VAAPI.codec
            case self.H265_QSV:
                return H26xCodecs.H265_QSV.codec
            case self.H265_NVENC:
                return H26xCodecs.H265_NVENC.codec

            # vp8 codecs
            case self.VP8_LIB:
                return Av1VpxCodecs.VP8_LIB.codec
            case self.VP8_VAAPI:
                return Av1VpxCodecs.VP8_VAAPI.codec
            case self.VP8_QSV:
                return Av1VpxCodecs.VP8_QSV.codec

            # vp9 codecs
            case self.VP9_LIB:
                return Av1VpxCodecs.VP9_LIB.codec
            case self.VP9_VAAPI:
                return Av1VpxCodecs.VP9_VAAPI.codec
            case self.VP9_QSV:
                return Av1VpxCodecs.VP9_QSV.codec

            # av1 codecs
            case self.AV1_LIB:
                return Av1VpxCodecs.AV1_LIB.codec
            case self.AV1_VAAPI:
                return Av1VpxCodecs.AV1_VAAPI.codec
            case self.AV1_QSV:
                return Av1VpxCodecs.AV1_QSV.codec
            case self.AV1_NVENC:
                return Av1VpxCodecs.AV1_NVENC.codec


__all__ = [
    "FFmpegVideoCodec",
    "FFmpegVideoCodecs",
]
