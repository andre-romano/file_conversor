# src/file_conversor/backend/gui/pdf/index.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.utils.dominate_bulma import *

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def pdf_index():
    tools = [
        {
            'image': url_for('icons', filename='padlock_locked.ico'),
            'title': _("Encrypt (protect PDF)"),
            'subtitle': _("Protect PDF file with a password (create encrypted PDF file)."),
            'url': url_for('pdf_encrypt'),
        },
        {
            'image': url_for('icons', filename='padlock_unlocked.ico'),
            'title': _("Decrypt (unprotect PDF)"),
            'subtitle': _("Remove password protection from a PDF file  (create decrypted PDF file)."),
            'url': url_for('pdf_decrypt'),
        },
        {
            'image': url_for('icons', filename='compress.ico'),
            'title': _("Compress"),
            'subtitle': _("Reduce the file size of a PDF document (requires Ghostscript external library)."),
            'url': url_for('pdf_compress'),
        },
        {
            'image': url_for('icons', filename='extract.ico'),
            'title': _("Extract pages"),
            'subtitle': _("Extract specific pages from a PDF document (create a new PDF file)."),
            'url': url_for('pdf_extract'),
        },
        {
            'image': url_for('icons', filename='merge.ico'),
            'title': _("Merge / Join PDFs"),
            'subtitle': _("Merge (join) input PDFs into a single PDF file."),
            'url': url_for('pdf_merge'),
        },
        {
            'image': url_for('icons', filename='rotate_right.ico'),
            'title': _("Rotate pages"),
            'subtitle': _("Rotate PDF pages (clockwise or anti-clockwise)."),
            'url': url_for('pdf_rotate'),
        },
        {
            'image': url_for('icons', filename='split.ico'),
            'title': _("Split PDF"),
            'subtitle': _("Split PDF pages into several 1-page PDFs."),
            'url': url_for('pdf_split'),
        },
        {
            'image': url_for('icons', filename='ocr.ico'),
            'title': _("OCR scanned PDF"),
            'subtitle': _("Create a searchable PDF file from scanned documents using OCR."),
            'url': url_for('pdf_ocr'),
        },
        {
            'image': url_for('icons', filename='convert.ico'),
            'title': _("Convert"),
            'subtitle': _("Convert a PDF file to a different format (might require Microsoft Word / LibreOffice)."),
            'url': url_for('pdf_convert'),
        },
        {
            'image': url_for('icons', filename='separate.ico'),
            'title': _("Extract images"),
            'subtitle': _("Extract images from a PDF document."),
            'url': url_for('pdf_extract_img'),
        },
        {
            'image': url_for('icons', filename='repair.ico'),
            'title': _("Repair PDF"),
            'subtitle': _("Attempt to repair a corrupted PDF file."),
            'url': url_for('pdf_repair'),
        },
    ]

    return render_template_string(str(
        PageCardGrid(
            *tools,
            nav_items=[
                {
                    'label': _("Home"),
                    'url': url_for('index'),
                },
                {
                    'label': _("PDF"),
                    'url': url_for('pdf_index'),
                    'active': True,
                },
            ],
            _title=_("File Conversor - PDF Tools")
        )
    ))
