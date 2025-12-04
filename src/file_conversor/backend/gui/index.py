# src\file_conversor\backend\gui\index.py

from typing import Any
from flask import render_template_string, send_from_directory, url_for

# user-provided modules
from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.utils.dominate_bulma import PageCardGrid

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageIndex(
    *items: dict[str, str],
    nav_items: list[dict[str, Any]],
):
    return PageCardGrid(
        *items,
        nav_items=nav_items,
        _title=f"Home - File Conversor",
    )


def index():
    return render_template_string(str(
        PageIndex(
            # OFFICE tools
            {
                'image': url_for('icons', filename='docx.ico'),
                'title': _("Document Tools"),
                'subtitle': f"{_('Document file manipulation')} {_('(requires LibreOffice)')})",
                'url': url_for('doc_index'),
            },
            {
                'image': url_for('icons', filename='xls.ico'),
                'title': _("Spreadsheet Tools"),
                'subtitle': f"{_('Spreadsheet file manipulation')} {_('(requires LibreOffice)')})",
                'url': url_for('xls_index'),
            },
            {
                'image': url_for('icons', filename='ppt.ico'),
                'title': _("Presentation Tools"),
                'subtitle': f"{_('Presentation file manipulation')} {_('(requires LibreOffice)')})",
                'url': url_for('ppt_index'),
            },

            # OTHER FILES
            {
                'image': url_for('icons', filename='mp3.ico'),
                'title': _("Audio Tools"),
                'subtitle': _("Audio file manipulation (requires FFMpeg external library)"),
                'url': url_for('audio_index'),
            },
            {
                'image': url_for('icons', filename='mp4.ico'),
                'title': _("Video Tools"),
                'subtitle': _("Video file manipulation (requires FFMpeg external library)"),
                'url': url_for('video_index'),
            },
            {
                'image': url_for('icons', filename='jpg.ico'),
                'title': _("Image Tools"),
                'subtitle': _("Image file manipulation"),
                'url': url_for('image_index'),
            },
            {
                'image': url_for('icons', filename='pdf.ico'),
                'title': _("PDF Tools"),
                'subtitle': _("PDF file manipulation."),
                'url': url_for('pdf_index'),
            },
            {
                'image': url_for('icons', filename='epub.ico'),
                'title': _("Ebook Tools"),
                'subtitle': _("Ebook file manipulation (requires Calibre external library)"),
                'url': url_for('ebook_index'),
            },
            {
                'image': url_for('icons', filename='json.ico'),
                'title': _("Text Tools"),
                'subtitle': _("Text file manipulation"),
                'url': url_for('text_index'),
            },
            {
                'image': url_for('icons', filename='sha256.ico'),
                'title': _("Hash Tools"),
                'subtitle': _("Hash file manipulation"),
                'url': url_for('hash_index'),
            },
            {
                'image': url_for('icons', filename='config.ico'),
                'title': _("Configuration"),
                'subtitle': _("Configure application default options"),
                'url': url_for('config_index'),
            },
            nav_items=[
                home_nav_item(active=True),
            ],
        )
    ))


def routes():
    return [
        FlaskRoute(
            rule="/",
            handler=index
        ),
    ]


__all__ = [
    'index',
    'routes',
]
