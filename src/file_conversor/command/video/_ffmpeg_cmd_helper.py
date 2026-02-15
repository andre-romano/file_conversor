
# src\file_conversor\command\video\_ffmpeg_cmd_helper.py

import shlex

from enum import Enum
from pathlib import Path
from typing import Any, Callable, Self

# user-provided modules
from file_conversor.backend.audio_video import FFmpegBackend, FFprobeBackend
from file_conversor.backend.audio_video.codec import (
    FFmpegAudioCodecs,
    FFmpegVideoCodecs,
)
from file_conversor.backend.audio_video.filter import (
    FFmpegFilter,
    FFmpegFilterDeshake,
    FFmpegFilterEq,
    FFmpegFilterHflip,
    FFmpegFilterMInterpolate,
    FFmpegFilterScale,
    FFmpegFilterTranspose,
    FFmpegFilterUnsharp,
    FFmpegFilterVflip,
)
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import Log, State, get_translation
from file_conversor.utils.formatters import format_bytes, parse_bytes
from file_conversor.utils.validators import is_close


# get app config
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class FFmpegCmdHelper:
    BACKEND = FFmpegBackend

    AudioCodecs = FFmpegAudioCodecs
    VideoCodecs = FFmpegVideoCodecs

    VideoProfile = FFmpegBackend.VideoProfile
    VideoEncoding = FFmpegBackend.VideoEncoding
    VideoQuality = FFmpegBackend.VideoQuality

    class Rotation(Enum):
        DEG_NEG_90 = -90
        DEG_90 = 90
        DEG_180 = 180
        DEG_270 = 270

        def get(self) -> list[FFmpegFilter]:
            match self:
                case  self.DEG_90:
                    return [FFmpegFilterTranspose(direction=1)]
                case self.DEG_180:
                    return [
                        FFmpegFilterTranspose(direction=1),
                        FFmpegFilterTranspose(direction=1),
                    ]
                case self.DEG_NEG_90 | self.DEG_270:
                    return [FFmpegFilterTranspose(direction=2)]

    class MirrorAxis(Enum):
        X = "x"
        Y = "y"
        XY = "xy"

        def get(self) -> list[FFmpegFilter]:
            match self:
                case self.X:
                    return [FFmpegFilterHflip()]
                case self.Y:
                    return [FFmpegFilterVflip()]
                case self.XY:
                    return [FFmpegFilterHflip(), FFmpegFilterVflip()]

    def __init__(
            self,
            install_deps: bool | None,
            verbose: bool,
            datamodel: BatchFilesDataModel,
            progress_callback: Callable[[float], Any] = lambda p: p,
    ) -> None:
        super().__init__()

        # init ffmpeg and ffprobe backends
        self._ffmpeg_backend = FFmpegBackend(
            install_deps=install_deps,
            verbose=verbose,
            overwrite_output=datamodel.overwrite_output,
        )
        self._ffprobe_backend = FFprobeBackend(
            install_deps=install_deps,
            verbose=verbose,
        )
        self._install_deps = install_deps
        self._verbose = verbose

        self._datamodel = datamodel
        self._progress_callback = progress_callback

        self._audio_codec: FFmpegCmdHelper.AudioCodecs | None = None
        self._video_codec: FFmpegCmdHelper.VideoCodecs | None = None

        self._video_profile: FFmpegCmdHelper.VideoProfile | None = None
        self._video_encoding_speed: FFmpegCmdHelper.VideoEncoding | None = None
        self._video_quality: FFmpegCmdHelper.VideoQuality | None = None

        self._target_size_bytes: int = 0

        self._audio_bitrate: int = -1
        self._video_bitrate: int = -1
        self._two_pass: bool = False

        self._audio_filters: list[FFmpegFilter] = []
        self._video_filters: list[FFmpegFilter] = []
        self._ffmpeg_args: list[str] = []

    def _set_video_bitrate_for_target_size(self, input_file: Path):
        if self._target_size_bytes <= 0:
            return

        duration = self._ffprobe_backend.get_duration(input_file)
        if duration < 0:
            raise RuntimeError(_('Could not determine input file duration'))

        # total size in kbit
        target_size_kbit = int(self._target_size_bytes * 8.0 / 1024.0)
        target_size_kbps = int(target_size_kbit / duration)

        # audio size
        self._audio_bitrate = 128 if self._audio_bitrate <= 0 else self._audio_bitrate
        self._video_bitrate = target_size_kbps - self._audio_bitrate

        audio_bytes_per_sec = self._audio_bitrate / 8.0
        audio_megabytes = audio_bytes_per_sec * duration / 1024.0

        if self._video_bitrate < 1:
            target_size = format_bytes(self._target_size_bytes)
            raise RuntimeError(f"{_('Target size too small')}: {target_size}. {_(f'Increase target size to at least')} '{audio_megabytes + 0.100:.2f}M' {_('(might not be enougth to achieve good video quality)')}.")

    def set_codecs(
            self,
            audio_codec: AudioCodecs | None = None,
            video_codec: VideoCodecs | None = None,
    ) -> Self:
        """
        Set audio and video codecs.

        :param audio_codec: Audio codec name.
        :param video_codec: Video codec name.
        """
        self._audio_codec = audio_codec
        self._video_codec = video_codec
        return self

    def set_video_settings(
        self,
        profile: VideoProfile | None = None,
        encoding_speed: VideoEncoding | None = None,
        quality: VideoQuality | None = None,
    ) -> Self:
        """
        Set video encoding settings.

        :param encoding_speed: Video encoding speed preset.
        :param quality: Video quality setting.
        """
        self._video_profile = profile
        self._video_encoding_speed = encoding_speed
        self._video_quality = quality
        return self

    def set_bitrate(
        self,
        audio_bitrate: int | None = None,
        video_bitrate: int | None = None,
    ) -> Self:
        """
        Set audio and video bitrate.

        :param audio_bitrate: Audio bitrate value.
        :param video_bitrate: Video bitrate value.
        """
        if audio_bitrate is not None:
            if audio_bitrate < -1:
                raise ValueError(_('Bitrates must be greater than or equal to -1'))
            self._audio_bitrate = audio_bitrate

        if video_bitrate is not None:
            if video_bitrate < -1:
                raise ValueError(_('Bitrates must be greater than or equal to -1'))
            self._video_bitrate = video_bitrate

        self._two_pass = (self._video_bitrate > 0) or (self._audio_bitrate > 0)
        return self

    def set_target_size(self, size_str: str = "0") -> Self:
        """
        Convert target size string to bytes.

        :param size_str: Target size string (e.g., "100M", "1G"). 0 means no target size.
        :return: Target size in bytes.
        """
        self._target_size_bytes = parse_bytes(size_str)
        self._two_pass = (self._target_size_bytes > 0)
        return self

    def set_audio_filters(
        self,
        custom_filters: list[str] | None = None,
    ) -> Self:
        """
        Set custom audio filters.

        :param filters: Custom audio filters as strings.
        :return: Self instance.
        """
        self._audio_filters.extend(FFmpegBackend.build_filter(f) for f in custom_filters or [])
        return self

    def set_video_filters(
        self,
        rotation: Rotation | None = None,
        mirror_axis: MirrorAxis | None = None,
        deshake: bool = False,
        unsharp: bool = False,
        resolution: tuple[int, int] | None = None,
        fps: int | None = None,
        brightness: float = 1.0,
        contrast: float = 1.0,
        color: float = 1.0,
        gamma: float = 1.0,
        custom_filters: list[str] | None = None,
    ) -> Self:
        """
        Set FFmpeg filters.

        :param rotation: Video rotation.
        :param mirror_axis: Video mirroring axis.
        :param deshake: Apply deshake filter.
        :param unsharp: Apply unsharp filter.
        :param resolution: Target resolution (width, height). if (0, 0), no scaling is applied.
        :param fps: Target frames per second. If 0, no fps change is applied.
        :param brightness: Brightness adjustment. If 1.0, no adjustment is applied.
        :param contrast: Contrast adjustment. If 1.0, no adjustment is applied.
        :param color: Color saturation adjustment. If 1.0, no adjustment is applied.
        :param gamma: Gamma correction. If 1.0, no adjustment is applied.
        :param custom_filters: Custom video filters as strings.

        :return: Self instance.
        """
        if rotation:
            self._video_filters.extend(rotation.get())

        if mirror_axis:
            self._video_filters.extend(mirror_axis.get())

        if deshake:
            self._video_filters.append(FFmpegFilterDeshake())

        if unsharp:
            self._video_filters.append(FFmpegFilterUnsharp())

        if resolution is not None and resolution[0] > 0 and resolution[1] > 0:
            self._video_filters.append(FFmpegFilterScale(*resolution))

        if fps is not None and fps > 0:
            self._video_filters.append(FFmpegFilterMInterpolate(fps=fps))

        if not all(is_close(val, 1.0) for val in (brightness, contrast, color, gamma)):
            self._video_filters.append(FFmpegFilterEq(brightness=brightness, contrast=contrast, saturation=color, gamma=gamma))

        self._video_filters.extend(FFmpegBackend.build_filter(f) for f in custom_filters or [])
        return self

    def set_ffmpeg_args(self, arg: str):
        """
        Set custom FFmpeg arguments.

        :param args: Custom FFmpeg arguments.
        :return: Self instance.
        """
        self._ffmpeg_args = shlex.split(arg)
        return self

    def _step_one(self, data: FileDataModel, get_progress: Callable[[float], float]):  # noqa: ARG002
        logger.debug(f"Input file: {data.input_file}")

        self._set_video_bitrate_for_target_size(data.input_file)
        logger.debug(f"{_('Two-pass encoding:')} [bold]{'[blue]ENABLED' if self._two_pass else '[red]DISABLED'}[/]")
        logger.debug(f"{_('Audio bitrate')}: [bold green]{self._audio_bitrate} kbps[/]")
        logger.debug(f"{_('Video bitrate')}: [bold green]{self._video_bitrate} kbps[/]")

        self._ffmpeg_backend.set_files(input_file=data.input_file, output_file=data.output_file)
        self._ffmpeg_backend.set_audio_codec(
            *self._audio_filters,
            codec=self._audio_codec,
            bitrate=self._audio_bitrate,
        )
        self._ffmpeg_backend.set_video_codec(
            *self._video_filters,
            codec=self._video_codec,
            bitrate=self._video_bitrate,
            profile_setting=self._video_profile,
            encoding_speed=self._video_encoding_speed,
            quality_setting=self._video_quality,
        )

        # display current progress
        steps_completed: int = 0
        step_progress: float = 0.50 if self._two_pass else 1.0

        def progress_callback(p: float):
            return self._progress_callback(step_progress * (steps_completed * 100.0 + p))

        self._ffmpeg_backend.execute(
            progress_callback=progress_callback,
            pass_num=1 if self._two_pass else 0,
            out_opts=self._ffmpeg_args,
        )

        if self._two_pass:
            steps_completed += 1
            self._ffmpeg_backend.execute(
                progress_callback=progress_callback,
                pass_num=2,
                out_opts=self._ffmpeg_args,
            )
        # ensure progress is set to 100% after execution
        progress_callback(100.0)

    def execute(self) -> Self:
        self._datamodel.execute(self._step_one)
        logger.info(f"{_('FFMpeg result')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
        return self


__all__ = [
    "FFmpegCmdHelper",
]
