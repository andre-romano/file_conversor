
# src\cli\batch_cmd.py

import shlex
import os
import subprocess
import json
import typer

from pathlib import Path
from typing import Annotated

from rich import print
from rich.progress import Progress

# user-provided modules
from config import Configuration, State
from config.locale import get_translation

from utils import File
from utils.rich import get_progress_bar

# get app config
_ = get_translation()
CONFIG = Configuration.get_instance()
STATE = State.get_instance()

CONFIG_FILENAME = ".config_fc.json"

batch_cmd = typer.Typer()


def process_stage(progress: Progress, monitor_dir: str, work_dir: str, command: str) -> bool:
    """
    Process a pipeline stage

    :return: True if success, False otherwise
    """
    SCRIPT_EXECUTABLE: str = STATE['script_executable']
    SCRIPT_WORKDIR: str = STATE['script_workdir']

    mon_dir = Path(monitor_dir)
    cwd_dir = Path(work_dir)
    cmd_template = str(command)
    # print(stage)

    total_files = sum(1 for _ in mon_dir.glob("*"))
    task = progress.add_task(f"{_('Stage')} '{mon_dir.name}' - {_('Processing files')}", total=total_files)
    res = True
    for i, path in enumerate(mon_dir.glob("*")):
        # ignore folders and config file
        if path.is_dir() or path.name == CONFIG_FILENAME:
            continue

        file = File(str(path))
        cmd_list = []
        for cmd in shlex.split(f"{SCRIPT_EXECUTABLE} {cmd_template}"):
            cmd = cmd.replace(f"{{in_file_path}}", f"{file.get_full_path()}")
            cmd = cmd.replace(f"{{in_file_name}}", f"{file.get_filename()}")
            cmd = cmd.replace(f"{{in_file_ext}}", f"{file.get_extension()}")
            cmd = cmd.replace(f"{{monitor_dir}}", f"{mon_dir}")
            cmd = cmd.replace(f"{{work_dir}}", f"{cwd_dir}")
            if "/" in cmd or "\\" in cmd:
                cmd = os.path.normpath(cmd)
            cmd_list.append(cmd)
        # print(cmd_list)
        try:
            process = subprocess.run(
                cmd_list,
                cwd=SCRIPT_WORKDIR,
                capture_output=True,
                check=True,
            )
            print(f"Processing file '{path}': [bold green]{_('SUCCESS')}[/] ({process.returncode})")
        except subprocess.CalledProcessError as e:
            print(f"Processing file '{path}': [bold red]{_('FAILED')}[/] ({e.returncode})")
            print(f"[bold red]{_('ERROR')}[/]: {str(e)}")
            print(f"Stdout:\n{e.stdout}")
            print(f"Stderr:\n{e.stderr}")
            res = False
        except Exception as e:
            print(f"Processing file '{path}': [bold red]{_('FAILED')}[/]")
            print(f"[bold red]{_('ERROR')}[/]: {str(e)}")
            res = False
        finally:
            progress.update(task, completed=i + 1)
    # if success, clean mon dir
    if res:
        for i, path in enumerate(mon_dir.glob("*")):
            if path.is_file() and path.name != CONFIG_FILENAME:
                path.unlink()
    else:
        # failed, clean work dir
        for i, path in enumerate(cwd_dir.glob("*")):
            if path.is_file() and path.name != CONFIG_FILENAME:
                path.unlink()
    # mark as finished
    progress.update(task, total=100, completed=100)
    return res


# batch create
@batch_cmd.command(
    help=f"""
        {_('Creates a batch file processing pipeline (for tasks automation).')}        

        {_('Will ask questions interactively to create a batch file processing pipeline.')}

        [bold]{_('Placeholders available for commands')}[/]:

        - [bold]{{in_file_path}}[/]: {_('Replaced by the first file path found in pipeline stage.')}

            - Ex: C:/Users/Alice/Desktop/pipeline_name/my_file.jpg

        - [bold]{{in_file_name}}[/]: {_('The name of the input file.')}

            - Ex: my_file

        - [bold]{{in_file_ext}}[/]: {_('The extension of the input file.')}

            - Ex: jpg

        - [bold]{{monitor_dir}}[/]: {_('The directory of the previous pipeline stage.')}

            - Ex: C:/Users/Alice/Desktop/pipeline_name

        - [bold]{{work_dir}}[/]: {_('The directory of the current pipeline stage.')}

            - Ex: C:/Users/Alice/Desktop/pipeline_name/1_to_png
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor batch create` 
""")
def create():
    pipeline_path_str: str = typer.prompt(f"{_('Name of the batch pipeline folder (e.g., %USERPROFILE%/Desktop/pipeline_name_here)')}")
    pipeline_path = Path(os.path.expandvars(pipeline_path_str)).resolve()
    pipeline_path.mkdir(parents=True, exist_ok=True)
    print(f"Pipeline created at '{pipeline_path}'")
    print(f"-------------------------------------")

    config_file = pipeline_path / CONFIG_FILENAME
    config_data = []
    prev_stage_path = pipeline_path

    stage_num = 1
    terminate = False
    while not terminate:
        try:
            stage: str = typer.prompt(f"{_('Name of the processing stage (e.g., image_convert)')}")
            stage = f"{stage_num}_{stage}"
            stage_path = (pipeline_path / stage).resolve()
            stage_path.mkdir(exist_ok=True)
            stage_num += 1
            print(f"Pipeline stage created at '{stage_path}'")

            cmd_str: str = typer.prompt(f"{_('Type command here')} ({_('e.g.')}, image convert {{in_file_path}} {{work_dir}}/{{in_file_name}}_converted.png )")
            config_data.append({
                "monitor_dir": str(prev_stage_path),
                "work_dir": str(stage_path),
                "command": str(cmd_str),
            })
            prev_stage_path = stage_path

            terminate = not typer.confirm(f"{_('Need another pipeline stage')}", default=False)
            print(f"-------------------------------------")
        except (KeyboardInterrupt, typer.Abort) as e:
            terminate = True
            raise
        except Exception as e:
            print(f"[bold red]{_('ERROR')}[/]: {str(e)}")

    config_file.write_text(json.dumps(config_data, indent=2, sort_keys=True))
    print(f"{_('Batch creation')}: [bold green]{_('SUCCESS')}[/].")
    print(f"--------------------------------")


# batch execute
@batch_cmd.command(
    help=f"""
        {_('Execute batch file processing pipeline.')}        
    """,
    epilog=f"""
**{_('Examples')}:** 

- `file_conversor batch execute c:/Users/Alice/Desktop/pipeline_name` 
""")
def execute(
    pipeline_folder: Annotated[str, typer.Argument(
        help=f"{_('Pipeline folder')}",
    )],
):
    success = True

    pipeline_path = Path(pipeline_folder)
    config_file = pipeline_path / CONFIG_FILENAME
    if not pipeline_path.exists():
        raise typer.BadParameter(f"{_('Pipeline path')} '{pipeline_path}' {_('does not exist')}")
    if not config_file.exists():
        raise typer.BadParameter(f"{_('Config file')} '{pipeline_path}' {_('does not exist')}")

    config_data: list
    print(f"{_('Loading')} '{config_file}' ...")
    with open(config_file, "r") as f:
        config_data = json.load(f)
    num_stages = len(config_data)
    print(f"{_('Found')} {num_stages} {_('stages')}")
    if num_stages < 1:
        return

    with get_progress_bar() as progress:
        task = progress.add_task(f"{_('Processing stage')}", total=num_stages)
        for i, stage in enumerate(config_data):
            progress.update(task, description=f"{_('Processing stage')} {i + 1}/{num_stages}")

            success = success and process_stage(progress=progress, **stage)

            progress.update(task, completed=i + 1)

    if not success:
        raise RuntimeError(_("One or more pipeline stages have failed. Check logs for more information."))

    print(f"{_('Batch execution')}: [bold green]{_('SUCCESS')}[/].")
    print(f"--------------------------------")
