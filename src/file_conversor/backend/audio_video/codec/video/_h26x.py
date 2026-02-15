# src\file_conversor\backend\audio_video\codec\_h26x.py

from enum import Enum

from file_conversor.backend.audio_video.codec.video.__quality_opts_helper import (
    QualityOptsHelper,
)
from file_conversor.backend.audio_video.codec.video.ffmpeg_video_codec import (
    FFmpegVideoCodec,
)


class H26xCodecs(Enum):
    # LIB codecs
    H264_LIB = "libx264"
    H265_LIB = "libx265"

    # QSV codecs
    H264_QSV = "h264_qsv"
    H265_QSV = "hevc_qsv"

    # VAAPI
    H264_VAAPI = "h264_vaapi"
    H265_VAAPI = "hevc_vaapi"

    # NVENC codecs
    H264_NVENC = "h264_nvenc"
    H265_NVENC = "hevc_nvenc"

    @property
    def codec(self) -> FFmpegVideoCodec:
        return FFmpegVideoCodec(self.value,
                                options=self.options,
                                encoding_speed_opts=self.encoding_speed_options,
                                quality_setting_opts=self.quality_options,
                                profile_opts=self.profile_options,
                                )

    @property
    def options(self) -> dict[str, str]:
        return {}

    @property
    def encoding_speed_options(self) -> dict[FFmpegVideoCodec.EncodingSetting, dict[str, str]]:
        match self:
            # LIB and QSV codecs
            case self.H264_LIB | self.H265_LIB | self.H264_QSV | self.H265_QSV:
                return {
                    FFmpegVideoCodec.EncodingSetting.FAST: {"-preset": "faster"},
                    FFmpegVideoCodec.EncodingSetting.MEDIUM: {"-preset": "medium"},
                    FFmpegVideoCodec.EncodingSetting.SLOW: {"-preset": "slower"},
                }

            # VAAPI codecs do not have encoding speed options
            case self.H264_VAAPI | self.H265_VAAPI:
                return {}

            # NVENC codecs
            case self.H264_NVENC | self.H265_NVENC:
                return {
                    FFmpegVideoCodec.EncodingSetting.FAST: {"-preset": "p3"},
                    FFmpegVideoCodec.EncodingSetting.MEDIUM: {"-preset": "p4"},
                    FFmpegVideoCodec.EncodingSetting.SLOW: {"-preset": "p5"},
                }

    @property
    def quality_options(self) -> dict[FFmpegVideoCodec.QualitySetting, dict[str, str]]:
        match self:
            # LIB codecs
            case self.H264_LIB:
                return QualityOptsHelper.LIB.get(high="19", medium="23", low="28")
            case self.H265_LIB:
                return QualityOptsHelper.LIB.get(high="17", medium="21", low="25")

            # QSV codecs
            case self.H264_QSV:
                return QualityOptsHelper.QSV.get(high="19", medium="23", low="28")
            case self.H265_QSV:
                return QualityOptsHelper.QSV.get(high="17", medium="21", low="25")

            # VAAPI codecs
            case self.H264_VAAPI:
                return QualityOptsHelper.VAAPI.get(high="20", medium="26", low="32")
            case self.H265_VAAPI:
                return QualityOptsHelper.VAAPI.get(high="18", medium="24", low="29")

            # NVENC codecs
            case self.H264_NVENC:
                return QualityOptsHelper.NVENC.get(high="19", medium="23", low="28")
            case self.H265_NVENC:
                return QualityOptsHelper.NVENC.get(high="17", medium="21", low="25")

    @property
    def profile_options(self) -> dict[FFmpegVideoCodec.ProfileSetting, dict[str, str]]:
        match self:
            case self.H264_LIB | self.H264_QSV | self.H264_VAAPI | self.H264_NVENC:
                # H264 profiles
                return {
                    FFmpegVideoCodec.ProfileSetting.HIGH: {"-profile:v": "high"},
                    FFmpegVideoCodec.ProfileSetting.MEDIUM: {"-profile:v": "main"},
                    FFmpegVideoCodec.ProfileSetting.LOW: {"-profile:v": "baseline"},
                }

            # H265 profiles
            case self.H265_LIB | self.H265_QSV | self.H265_VAAPI | self.H265_NVENC:
                return {
                    FFmpegVideoCodec.ProfileSetting.HIGH: {"-profile:v": "main"},  # H265 High profile maps to Main
                    FFmpegVideoCodec.ProfileSetting.MEDIUM: {"-profile:v": "main"},
                    FFmpegVideoCodec.ProfileSetting.LOW: {"-profile:v": "main"},  # H265 does not have Baseline profile
                }


__all__ = [
    "H26xCodecs",
]
