
# src\file_conversor\cli\video\_ffmpeg_cmd_helper.py

from rich import print

from typing import Annotated, Any, Callable, List, Self
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend, FFprobeBackend
from file_conversor.backend.audio_video.ffmpeg_filter import FFmpegFilter, FFmpegFilterDeshake, FFmpegFilterEq, FFmpegFilterHflip, FFmpegFilterMInterpolate, FFmpegFilterScale, FFmpegFilterTranspose, FFmpegFilterUnsharp, FFmpegFilterVflip

from file_conversor.config import Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.formatters import format_bytes, normalize_degree, parse_bytes
from file_conversor.utils.validators import check_valid_options, is_close

# get app config
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES


class FFmpegCmdHelper:
    def __init__(
            self,
            install_deps: bool | None,
            verbose: bool,
            overwrite_output: bool,
    ) -> None:
        super().__init__()

        # init ffmpeg and ffprobe backends
        self._ffmpeg_backend = FFmpegBackend(
            install_deps=install_deps,
            verbose=verbose,
            overwrite_output=overwrite_output,
        )
        self._ffprobe_backend = FFprobeBackend(
            install_deps=install_deps,
            verbose=verbose,
        )
        self._install_deps = install_deps
        self._verbose = verbose
        self._overwrite_output = overwrite_output

        self._input_files: list[Path] = []

        self._file_format: str = ""
        self._out_stem: str = ""
        self._output_dir: Path = Path()

        self._audio_codec: str | None = None
        self._video_codec: str | None = None

        self._video_encoding_speed: str | None = None
        self._video_quality: str | None = None

        self._target_size_bytes: int = 0

        self._audio_bitrate: int = 0
        self._video_bitrate: int = 0
        self._two_pass: bool = False

        self._audio_filters: list[FFmpegFilter] = []
        self._video_filters: list[FFmpegFilter] = []

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
        audio_kbps = self._audio_bitrate / 8.0
        audio_mb = audio_kbps * duration / 1024.0

        self._video_bitrate = target_size_kbps - self._audio_bitrate
        if self._video_bitrate < 1:
            target_size = format_bytes(self._target_size_bytes)
            raise RuntimeError(f"{_('Target size too small')}: {target_size}. {_(f'Increase target size to at least')} '{audio_mb + 0.100:.2f}M' {_('(might not be enougth to achieve good video quality)')}.")

    def set_input(self, input_files: list[Path]) -> Self:
        """
        Set input files.

        :param input_files: List of input file paths.
        """
        self._input_files = input_files
        return self

    def set_output(
        self,
        file_format: str,
        out_stem: str = "",
        output_dir: Path = Path(),
    ) -> Self:
        """
        Set output parameters.

        :param file_format: Output file format.
        :param out_stem: Output file name stem.
        :param output_dir: Output directory path.
        """
        self._file_format = file_format
        self._out_stem = out_stem
        self._output_dir = output_dir
        return self

    def set_codecs(self, audio_codec: str | None, video_codec: str | None) -> Self:
        """
        Set audio and video codecs.

        :param audio_codec: Audio codec name.
        :param video_codec: Video codec name.
        """
        self._audio_codec = audio_codec
        self._video_codec = video_codec
        return self

    def set_video_settings(self, encoding_speed: str | None = None, quality: str | None = None) -> Self:
        """
        Set video encoding settings.

        :param encoding_speed: Video encoding speed preset.
        :param quality: Video quality setting.
        """
        self._video_encoding_speed = encoding_speed
        self._video_quality = quality
        return self

    def set_bitrate(self, audio_bitrate: int = 0, video_bitrate: int = 0) -> Self:
        """
        Set audio and video bitrate.

        :param audio_bitrate: Audio bitrate value.
        :param video_bitrate: Video bitrate value.
        """
        self._audio_bitrate = audio_bitrate
        self._video_bitrate = video_bitrate
        self._two_pass = (self._video_bitrate > 0) or (self._audio_bitrate > 0)
        return self

    def set_target_size(self, size_str: str | None) -> Self:
        """
        Convert target size string to bytes.

        :param size_str: Target size string (e.g., "100M", "1G").
        :return: Target size in bytes.
        """
        self._target_size_bytes = parse_bytes(size_str) if size_str else 0
        return self

    def set_resolution_filter(self, resolution: str | None) -> Self:
        """
        Set FFmpeg resolution from resolution string.

        :param resolution: Resolution string (e.g., "1920:1080").
        """
        if resolution is None:
            return self
        width_height = resolution.split(":")
        if len(width_height) != 2:
            raise ValueError(f"{_('Invalid resolution format')}: {resolution} {_('(expected format WIDTH:HEIGHT)')}")
        width, height = width_height
        self._video_filters.append(FFmpegFilterScale(width, height))
        return self

    def set_fps_filter(self, fps: int | None) -> Self:
        """
        Set FFmpeg target fps from fps integer value.

        :param fps: Frames per second value.
        """
        if fps is None:
            return self
        if fps < 1:
            raise ValueError(f"{_('Invalid FPS value')}: {fps}")
        self._video_filters.append(FFmpegFilterMInterpolate(fps=fps))
        return self

    def set_enhancement_filters(
        self,
        brightness: float = 1.0,
        contrast: float = 1.0,
        color: float = 1.0,
        gamma: float = 1.0,
    ) -> Self:
        """
        Set FFmpeg enhancement filters.

        :param brightness: Brightness adjustment value.
        :param contrast: Contrast adjustment value.
        :param color: Color adjustment value.
        :param gamma: Gamma adjustment value.
        """
        if not (is_close(brightness, 1.0) and is_close(contrast, 1.0) and is_close(color, 1.0) and is_close(gamma, 1.0)):
            self._video_filters.append(FFmpegFilterEq(brightness=brightness, contrast=contrast, saturation=color, gamma=gamma))
        return self

    def set_rotation_filter(self, rotation: int | None) -> Self:
        """
        Set FFmpeg rotation filter from rotation integer value.

        :param rotation: Rotation degree value.
        """
        if rotation is None:
            return self
        rotation = normalize_degree(rotation)
        if rotation == 0:
            # no need to rotate
            return self
        elif rotation in (90, 270):
            direction = {
                90: 1,
                270: 2,
            }[rotation]
            self._video_filters.append(FFmpegFilterTranspose(direction=direction))
        elif rotation in (180,):
            self._video_filters.append(FFmpegFilterTranspose(direction=1))
            self._video_filters.append(FFmpegFilterTranspose(direction=1))
        else:
            raise ValueError(f"{_('Invalid rotation value')}: {rotation}")
        return self

    def set_mirror_filter(self, mirror_axis: str | None) -> Self:
        """
        Set FFmpeg mirror filter from mirror axis string.

        :param mirror_axis: Mirror axis string ("x", "y", "xy").
        """
        if mirror_axis is None or mirror_axis == "":
            # no need to mirror
            return self
        elif mirror_axis == "x":
            self._video_filters.append(FFmpegFilterHflip())
        elif mirror_axis == "y":
            self._video_filters.append(FFmpegFilterVflip())
        elif mirror_axis == "xy":
            self._video_filters.append(FFmpegFilterHflip())
            self._video_filters.append(FFmpegFilterVflip())
        else:
            raise ValueError(f"{_('Invalid mirror axis value')}: {mirror_axis}")
        return self

    def set_deshake_filter(self, deshake: bool) -> Self:
        """
        Set FFmpeg deshake filter.

        :param deshake: Whether to apply deshake filter.
        """
        if deshake:
            self._video_filters.append(FFmpegFilterDeshake())
        return self

    def set_unsharp_filter(self, unsharp: bool) -> Self:
        """
        Set FFmpeg unsharp filter.

        :param unsharp: Whether to apply unsharp filter.
        """
        if unsharp:
            self._video_filters.append(FFmpegFilterUnsharp())
        return self

    def execute(
        self,
        progress_callback: Callable[[float, ProgressManager], Any] | None = None,
    ) -> Self:
        def _callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
            logger.debug(f"Input file: {input_file}")

            logger.debug(f"{_('Audio bitrate')}: [green][bold]{self._audio_bitrate} kbps[/bold][/green]")
            logger.debug(f"{_('Video bitrate')}: [green][bold]{self._video_bitrate} kbps[/bold][/green]")

            self._ffmpeg_backend.set_files(input_file=input_file, output_file=output_file)
            self._ffmpeg_backend.set_audio_codec(
                codec=self._audio_codec,
                bitrate=self._audio_bitrate,
                filters=self._audio_filters,
            )
            self._ffmpeg_backend.set_video_codec(
                codec=self._video_codec,
                bitrate=self._video_bitrate,
                filters=self._video_filters,
                encoding_speed=self._video_encoding_speed,
                quality_setting=self._video_quality,
            )

            progress_update_cb = progress_mgr.update_progress
            if progress_callback is not None:
                def progress_update_cb(step_progress: float): return progress_callback(step_progress, progress_mgr)  # pyright: ignore[reportOptionalCall]

            progress_complete_cb = progress_mgr.complete_step
            if progress_callback is not None:
                def progress_complete_cb(): return progress_callback(progress_mgr.complete_step(), progress_mgr)  # pyright: ignore[reportOptionalCall]

            # display current progress
            self._ffmpeg_backend.execute(
                progress_callback=progress_update_cb,
                pass_num=1 if self._two_pass else 0,
            )
            progress_complete_cb()

            if self._two_pass:
                # display current progress
                self._ffmpeg_backend.execute(
                    progress_callback=progress_update_cb,
                    pass_num=2,
                )
                progress_complete_cb()

        cmd_mgr = CommandManager(self._input_files, output_dir=self._output_dir, steps=2 if self._two_pass else 1, overwrite=self._overwrite_output)
        cmd_mgr.run(_callback, out_suffix=f".{self._file_format}", out_stem=self._out_stem)

        logger.info(f"{_('FFMpeg result')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
        return self


__all__ = [
    "FFmpegCmdHelper",
    "EXTERNAL_DEPENDENCIES",
]
