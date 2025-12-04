# src\file_conversor\backend\gui\flask_api.py

import tempfile
import threading

from pathlib import Path
from typing import Any, Callable, Iterable, Self

from flask import Flask, Response, request, jsonify

# user-provided modules
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus, FlaskApiStatusCompleted, FlaskApiStatusUnknown, FlaskApiStatusError, FlaskApiStatusProcessing, FlaskApiStatusReady

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

from file_conversor.utils.formatters import escape_xml, format_traceback_html, format_traceback_str, parse_js_to_py

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


class FlaskApi:
    _status: dict[str, FlaskApiStatus] = {}

    @classmethod
    def _set_state(cls, params: dict[str, Any]) -> None:
        """Set the application state based on the provided parameters."""
        STATE['quiet'] = bool(params.get('quiet', False))
        STATE['verbose'] = bool(params.get('verbose', False))
        STATE['overwrite-output'] = bool(params.get('overwrite-output', False))

    @classmethod
    def _execute_thread(
        cls,
        params: dict[str, Any],
        callback: Callable[[dict[str, Any], FlaskApiStatus], None],
    ) -> None:
        """Thread to handle file processing."""
        try:
            logger.debug(f"Processing thread started ...")
            cls._set_state(params)

            status = cls._get_status(params['status_id'])
            status.set_progress(-1)  # indeterminate progress

            # run callback
            callback(params, status)

            # finished successfully
            msg_success = _('Processing completed successfully.')
            status.set(FlaskApiStatusCompleted(
                id=status.get_id(),
                message=status.get_message() or msg_success,
            ))
            logger.info(f"[bold]{msg_success}[/]")
        except Exception as e:
            logger.error(format_traceback_str(e, debug=STATE["debug"]))
            progress = status.get_progress()
            status.set(FlaskApiStatusError(
                id=status.get_id(),
                exception=format_traceback_html(e, debug=STATE["debug"]),
                progress=None if progress is None or progress < 0 else progress,
            ))
            raise

    @classmethod
    def _add_status(cls) -> FlaskApiStatus:
        """Add or update the status of a specific operation by its ID."""
        status_id = len(cls._status) + 1
        status = FlaskApiStatusProcessing(id=status_id)
        cls._status[status._id] = status
        return status

    @classmethod
    def _get_status(cls, status_id: str | None) -> FlaskApiStatus:
        """Get the status of a specific operation by its ID."""
        if status_id is None or status_id.lower() in ('', 'none', 'null', '0'):
            return FlaskApiStatusReady()
        status = cls._status.get(status_id)
        # remove completed or error statuses
        if status is not None and isinstance(status, (FlaskApiStatusCompleted, FlaskApiStatusError)):
            del cls._status[status_id]
        return status or FlaskApiStatusUnknown(status_id)

    @classmethod
    def get_args(cls) -> dict[str, Any]:
        """
        Get query parameters from the request.

        :return: dict[str, Any]: A dictionary containing the query parameters.
        """
        data: dict[str, str] = request.args.to_dict()
        logger.debug(f"Received args: {data}")
        for key, value in data.items():
            data[key] = parse_js_to_py(value)
        return data

    @classmethod
    def get_form_data(cls) -> dict[str, Any]:
        """
        Get form data from the request.

        :return: dict[str, Any]: A dictionary containing the form data.
        """
        data: dict[str, str] = request.form.to_dict()
        logger.debug(f"Received data: {data}")
        # Update the configuration with the provided data
        for key, value in data.items():
            data[key] = parse_js_to_py(value)
        return data

    @classmethod
    def get_files_list(cls, key: str) -> tuple[list[Path], Path]:
        """
        Save the uploaded files from the request into temporary dir, for processing.

        :return: tuple[list[Path], Path]: A tuple containing the list of saved file paths and the temporary directory path.
        """
        res: list[Path] = []
        files = request.files.getlist(key)
        temp_dir = Path(tempfile.mkdtemp())
        for file in files:
            if not file.filename:
                continue
            file_path = temp_dir / file.filename
            file.save(file_path)
            res.append(file_path)
        return res, temp_dir

    @classmethod
    def status_response(cls, id: str | None) -> tuple[Response, int]:
        """
        API endpoint to get the application status.

        :param id: str | None: The ID of the status to retrieve.

        :return: tuple[str, int]: ({id:str, status:str, message:str, exception:str, progress:int}, status_code:int)
        """
        status = cls._get_status(id)
        ret_code = 200
        if isinstance(status, FlaskApiStatusUnknown):
            ret_code = 404
        elif isinstance(status, FlaskApiStatusError):
            ret_code = 500
        return jsonify(status.json()), ret_code

    @classmethod
    def execute_response(
        cls,
        callback: Callable[[dict[str, Any], FlaskApiStatus], None],
    ) -> tuple[Response, int]:
        """
        API endpoint to process files.
        ```python
        req={
            'param1': 'Value 1',
            'param2': 'Value 2',
            ...
        }
        ```
        :param callback: Callable[[dict[str, Any]], None]: The function to execute in a separate thread.

        :return: tuple[str, int]: ({status:str, status_id:str, message:str}, 200)
        """
        status = None
        try:
            logger.info(f"[bold]{_('File processing requested via API.')}[/]")
            data = cls.get_form_data()
            status = cls._add_status()
            data['status_id'] = status.get_id()
            threading.Thread(target=cls._execute_thread, args=(data, callback), daemon=True).start()
            return jsonify(status.json()), 200
        except Exception as e:
            logger.error(format_traceback_str(e, debug=STATE["debug"]))
            return jsonify(FlaskApiStatusError(
                id=status.get_id() if status else -1,
                exception=format_traceback_html(e, debug=STATE["debug"]),
            ).json()), 500


__all__ = ["FlaskApi"]
