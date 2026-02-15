# src\file_conversor\backend\audio_video\container\video_format_container.py

from enum import Enum
from typing import Any, Self

from file_conversor.backend.audio_video.codec import (
    FFmpegAudioCodecs,
    FFmpegVideoCodecs,
)
from file_conversor.backend.audio_video.container.format_container import (
    FormatContainer,
)

# user-provided imports
from file_conversor.config import Log, get_translation


_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class VideoFormatContainers(Enum):
    NULL = "null"
    MP4 = "mp4"
    AVI = "avi"
    MKV = "mkv"
    WEBM = "webm"

    @property
    def container(self) -> FormatContainer:
        match self:
            case self.NULL:
                return FormatContainer("null")
            case self.MP4:
                return FormatContainer("mp4",
                                       audio_codec=FFmpegAudioCodecs.AAC_LIB,
                                       video_codec=FFmpegVideoCodecs.H264_LIB,
                                       available_audio_codecs={
                                           FFmpegAudioCodecs.AAC_LIB, FFmpegAudioCodecs.AC3_LIB,
                                           FFmpegAudioCodecs.MP3_LIB,
                                       },
                                       available_video_codecs={
                                           FFmpegVideoCodecs.H264_LIB, FFmpegVideoCodecs.H265_LIB,
                                           FFmpegVideoCodecs.H264_NVENC, FFmpegVideoCodecs.H265_NVENC,
                                           FFmpegVideoCodecs.H264_VAAPI, FFmpegVideoCodecs.H265_VAAPI,
                                           FFmpegVideoCodecs.H264_QSV, FFmpegVideoCodecs.H265_QSV,
                                       })
            case self.AVI:
                return FormatContainer("avi",
                                       audio_codec=FFmpegAudioCodecs.MP3_LIB,
                                       video_codec=FFmpegVideoCodecs.MPEG4,
                                       available_audio_codecs={
                                           FFmpegAudioCodecs.MP3_LIB, FFmpegAudioCodecs.PCM_S16LE,
                                       })
            case self.MKV:
                return FormatContainer("matroska",
                                       audio_codec=FFmpegAudioCodecs.AAC_LIB,
                                       video_codec=FFmpegVideoCodecs.H264_LIB,
                                       available_audio_codecs={
                                           FFmpegAudioCodecs.AAC_LIB, FFmpegAudioCodecs.AC3_LIB,
                                           FFmpegAudioCodecs.MP3_LIB, FFmpegAudioCodecs.OPUS_LIB,
                                           FFmpegAudioCodecs.VORBIS_LIB, FFmpegAudioCodecs.FLAC_LIB,
                                       },
                                       available_video_codecs={
                                           FFmpegVideoCodecs.H264_LIB, FFmpegVideoCodecs.H265_LIB,
                                           FFmpegVideoCodecs.H264_NVENC, FFmpegVideoCodecs.H265_NVENC,
                                           FFmpegVideoCodecs.H264_VAAPI, FFmpegVideoCodecs.H265_VAAPI,
                                           FFmpegVideoCodecs.H264_QSV, FFmpegVideoCodecs.H265_QSV,
                                           FFmpegVideoCodecs.VP8_LIB, FFmpegVideoCodecs.VP9_LIB, FFmpegVideoCodecs.AV1_LIB,
                                           FFmpegVideoCodecs.VP8_VAAPI, FFmpegVideoCodecs.VP9_VAAPI, FFmpegVideoCodecs.AV1_VAAPI,
                                           FFmpegVideoCodecs.VP8_QSV, FFmpegVideoCodecs.VP9_QSV, FFmpegVideoCodecs.AV1_QSV,
                                           FFmpegVideoCodecs.AV1_NVENC,
                                       })
            case self.WEBM:
                return FormatContainer("webm",
                                       audio_codec=FFmpegAudioCodecs.VORBIS_LIB,
                                       video_codec=FFmpegVideoCodecs.VP8_LIB,
                                       available_audio_codecs={
                                           FFmpegAudioCodecs.VORBIS_LIB,
                                           FFmpegAudioCodecs.OPUS_LIB,
                                       },
                                       available_video_codecs={
                                           FFmpegVideoCodecs.VP8_LIB, FFmpegVideoCodecs.VP9_LIB, FFmpegVideoCodecs.AV1_LIB,
                                           FFmpegVideoCodecs.VP8_VAAPI, FFmpegVideoCodecs.VP9_VAAPI, FFmpegVideoCodecs.AV1_VAAPI,
                                           FFmpegVideoCodecs.VP8_QSV, FFmpegVideoCodecs.VP9_QSV, FFmpegVideoCodecs.AV1_QSV,
                                           FFmpegVideoCodecs.AV1_NVENC,
                                       })

    def __contains__(self, value: str | Self | Any) -> bool:
        if isinstance(value, str):
            return value.lower() == self.value
        if isinstance(value, VideoFormatContainers):
            return value == self
        raise ValueError(_("Value must be a string or an instance of VideoFormatContainers"))


__all__ = [
    "VideoFormatContainers",
]
