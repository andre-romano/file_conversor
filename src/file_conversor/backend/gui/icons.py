from flask import send_from_directory

# user-provided modules
from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.config.environment import Environment

icons_path = Environment.get_icons_folder()


def icons(filename):
    return send_from_directory(icons_path, filename)


def routes():
    return [
        FlaskRoute(
            rule="/icons/<path:filename>",
            handler=icons,
        )
    ]


__all__ = ['routes']
