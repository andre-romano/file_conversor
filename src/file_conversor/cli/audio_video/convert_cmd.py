
# src\file_conversor\cli\audio_video\convert_cmd.py

import typer

from rich import print

from typing import Annotated, List
from pathlib import Path

# user-provided modules
from file_conversor.backend import FFmpegBackend
from file_conversor.backend.audio_video.ffmpeg_filter import FFmpegFilter, FFmpegFilterDeshake, FFmpegFilterEq, FFmpegFilterHflip, FFmpegFilterMInterpolate, FFmpegFilterScale, FFmpegFilterTranspose, FFmpegFilterUnsharp, FFmpegFilterVflip

from file_conversor.cli.audio_video._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.audio_video._typer import COMMAND_NAME, CONVERT_NAME
from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.formatters import parse_ffmpeg_filter
from file_conversor.utils.validators import check_positive_integer, check_valid_options, check_video_resolution
from file_conversor.utils.typer_utils import AxisOption, FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.system.win import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = FFmpegBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    # FFMPEG commands
    icons_folder_path = Environment.get_icons_folder()
    for ext in FFmpegBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="to_avi",
                description="To AVI",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "avi"',
                icon=str(icons_folder_path / 'avi.ico'),
            ),
            WinContextCommand(
                name="to_mkv",
                description="To MKV",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "mkv"',
                icon=str(icons_folder_path / 'mkv.ico'),
            ),
            WinContextCommand(
                name="to_mp4",
                description="To MP4",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "mp4"',
                icon=str(icons_folder_path / 'mp4.ico'),
            ),
            WinContextCommand(
                name="to_mp3",
                description="To MP3",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "mp3"',
                icon=str(icons_folder_path / 'mp3.ico'),
            ),
            WinContextCommand(
                name="to_m4a",
                description="To M4A",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "m4a"',
                icon=str(icons_folder_path / 'm4a.ico'),
            ),
            WinContextCommand(
                name="to_webm",
                description="To WEBM",
                command=f'{Environment.get_executable()} "{COMMAND_NAME}" "{CONVERT_NAME}" "%1" -f "webm"',
                icon=str(icons_folder_path / 'webm.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


@typer_cmd.command(
    name=CONVERT_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Convert a audio/video file to a different format.')}

        {_('This command can be used to convert audio or video files to the specified format.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.webm -od output_dir/ -f mp4 --audio-bitrate 192`

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.mp4 -f mp3`

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.mp4 -f mkv -r 90`

        - `file_conversor {COMMAND_NAME} {CONVERT_NAME} input_file.mkv -f avi -rs 1280x720`
    """)
def convert(
    input_files: Annotated[List[Path], InputFilesArgument(FFmpegBackend)],

    format: Annotated[str, FormatOption(FFmpegBackend)],

    audio_bitrate: Annotated[int, typer.Option("--audio-bitrate", "-ab",
                                               help=_("Audio bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["audio-bitrate"],

    video_bitrate: Annotated[int, typer.Option("--video-bitrate", "-vb",
                                               help=_("Video bitrate in kbps"),
                                               callback=check_positive_integer,
                                               )] = CONFIG["video-bitrate"],

    audio_codec: Annotated[str | None, typer.Option("--audio-codec", "-ac",
                                                    help=f'{_("Audio codec. Available options are:")} {", ".join(FFmpegBackend.get_supported_audio_codecs())}. Not all codecs are available for all file formats (check FFmpeg for supportted containers). Defaults to None (use the default for the file container).',
                                                    callback=lambda x: check_valid_options(x, FFmpegBackend.get_supported_audio_codecs()),
                                                    )] = None,

    video_codec: Annotated[str | None, typer.Option("--video-codec", "-vc",
                                                    help=f'{_("Video codec. Available options are:")} {", ".join(FFmpegBackend.get_supported_video_codecs())}. Not all codecs are available for all file formats (check FFmpeg for supportted containers). Defaults to None (use the default for the file container).',
                                                    callback=lambda x: check_valid_options(x, FFmpegBackend.get_supported_video_codecs()),
                                                    )] = None,

    audio_filters: Annotated[List[str], typer.Option("--audio-filter", "-af",
                                                     help=f'{_("Apply a custom FFmpeg audio filter (advanced option, use with caution). Uses the same format as FFmpeg filters (e.g., filter=option1=value1:option2=value2:...). Filters are applied in the order they appear in the command.")}. {_('Defaults to None (do not apply custom filters)')}.',
                                                     )] = [],

    video_filters: Annotated[List[str], typer.Option("--video-filter", "-vf",
                                                     help=f'{_("Apply a custom FFmpeg video filter (advanced option, use with caution). Uses the same format as FFmpeg filters (e.g., filter=option1=value1:option2=value2:...). Filters are applied in the order they appear in the command.")}. {_('Defaults to None (do not apply custom filters)')}.',
                                                     )] = [],

    resolution: Annotated[str | None, typer.Option("--resolution", "-rs",
                                                   help=f'{_("Video target resolution. Format WIDTH:HEIGHT (in pixels). Defaults to None (use same resolution as video source)")}',
                                                   callback=check_video_resolution,
                                                   )] = None,

    fps: Annotated[int | None, typer.Option("--fps", "-fp",
                                            help=f'{_("Target video FPS (frames per second). Uses ``minterpolate`` filter to adjust fps. Defaults to None (use same fps as video source)")}',
                                            min=1,
                                            )] = None,

    brightness: Annotated[float, typer.Option("--brightness", "-b",
                                              help=f'{_("Adjust brightness")}. {_('Defaults to 1.0 (do not adjust)')}.',
                                              min=1.0, max=3.0,
                                              )] = 1.0,

    contrast: Annotated[float, typer.Option("--contrast", "-c",
                                            help=f'{_("Adjust contrast")}. {_('Defaults to 1.0 (do not adjust)')}.',
                                            min=1.0, max=3.0,
                                            )] = 1.0,

    saturation: Annotated[float, typer.Option("--saturation", "-s",
                                              help=f'{_("Adjust saturation")}. {_('Defaults to 1.0 (do not adjust)')}.',
                                              min=1.0, max=3.0,
                                              )] = 1.0,

    gamma: Annotated[float, typer.Option("--gamma", "-g",
                                         help=f'{_("Adjust gamma")}. {_('Defaults to 1.0 (do not adjust)')}.',
                                         min=1.0, max=3.0,
                                         )] = 1.0,

    rotation: Annotated[int | None, typer.Option("--rotation", "-r",
                                                 help=f'{_("Rotate video (clockwise). Available options are:")} {", ".join(['-180', '-90', '90', '180'])}. {_('Defaults to None (do not rotate)')}.',
                                                 callback=lambda x: check_valid_options(x, [-180, -90, 90, 180]),
                                                 )] = None,

    mirror_axis: Annotated[str | None, AxisOption()] = None,

    deshake: Annotated[bool, typer.Option("--deshake", "-d",
                                          help=f'{_("Deshake video (attempt to fix vertical/horizontal span from handrecoding)")}. {_('Defaults to False (do not apply filter)')}.',
                                          is_flag=True,
                                          )] = False,

    unsharp: Annotated[bool, typer.Option("--unsharp", "-u",
                                          help=f'{_("Increase video sharpness (using unsharp mask). May increase image noise.")}. {_('Defaults to False (do not apply filter)')}.',
                                          is_flag=True,
                                          )] = False,

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    # init ffmpeg
    ffmpeg_backend = FFmpegBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
        overwrite_output=STATE["overwrite-output"],
    )

    # set filters
    audio_filters_obj: list[FFmpegFilter] = list()
    video_filters_obj: list[FFmpegFilter] = list()

    for filter in audio_filters:
        name, args = parse_ffmpeg_filter(filter)
        audio_filters_obj.append(FFmpegFilter(name, *args))

    for filter in video_filters:
        name, args = parse_ffmpeg_filter(filter)
        video_filters_obj.append(FFmpegFilter(name, *args))

    # VIDEO FILTERS
    if resolution is not None:
        video_filters_obj.append(FFmpegFilterScale(*resolution.split(":")))

    if fps is not None:
        video_filters_obj.append(FFmpegFilterMInterpolate(fps=fps))

    if brightness != 1.0 or contrast != 1.0 or saturation != 1.0 or gamma != 1.0:
        video_filters_obj.append(FFmpegFilterEq(brightness=brightness, contrast=contrast, saturation=saturation, gamma=gamma))

    if rotation is not None:
        if rotation in (90, -90):
            direction = {90: 1, -90: 2}[rotation]
            video_filters_obj.append(FFmpegFilterTranspose(direction=direction))
        else:
            video_filters_obj.append(FFmpegFilterTranspose(direction=1))
            video_filters_obj.append(FFmpegFilterTranspose(direction=1))

    if mirror_axis is not None:
        if mirror_axis == "x":
            video_filters_obj.append(FFmpegFilterHflip())
        else:
            video_filters_obj.append(FFmpegFilterVflip())

    if deshake:
        video_filters_obj.append(FFmpegFilterDeshake())

    if unsharp:
        video_filters_obj.append(FFmpegFilterUnsharp())

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        ffmpeg_backend.set_files(input_file=input_file, output_file=output_file)
        ffmpeg_backend.set_audio_codec(codec=audio_codec, bitrate=audio_bitrate, filters=audio_filters_obj)
        ffmpeg_backend.set_video_codec(codec=video_codec, bitrate=video_bitrate, filters=video_filters_obj)

        # display current progress
        process = ffmpeg_backend.execute(
            progress_callback=progress_mgr.update_progress
        )
        progress_mgr.complete_step()

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_suffix=f".{format}")

    logger.info(f"{_('FFMpeg convertion')}: [green][bold]{_('SUCCESS')}[/bold][/green]")
