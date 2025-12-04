# src/file_conversor/backend/gui/image/index.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.image._dom_page import image_index_nav_item

from file_conversor.utils.dominate_bulma import PageCardGrid

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def image_index():
    tools = [
        {

            'image': url_for('icons', filename='convert.ico'),
            'title': _("Convert files"),
            'subtitle': _("Convert a image file to a different format."),

            'url': url_for('image_convert'),
        },
        {

            'image': url_for('icons', filename='svg.ico'),
            'title': _("Render vector"),
            'subtitle': _("Render an image vector file into a different format."),

            'url': url_for('image_render'),
        },
        {

            'image': url_for('icons', filename='pdf.ico'),
            'title': _("To PDF"),
            'subtitle': _("Convert a images to one PDF file, one image per page."),

            'url': url_for('image_to_pdf'),
        },
        {

            'image': url_for('icons', filename='compress.ico'),
            'title': _("Compress file"),
            'subtitle': _("Compress an image file (requires external libraries)."),

            'url': url_for('image_compress'),
        },
        {

            'image': url_for('icons', filename='left_right.ico'),
            'title': _("Mirror / Flip"),
            'subtitle': _("Mirror an image file (vertically or horizontally)."),

            'url': url_for('image_mirror'),
        },
        {

            'image': url_for('icons', filename='rotate_right.ico'),
            'title': _("Rotate"),
            'subtitle': _("Rotate a image file (clockwise or anti-clockwise)."),

            'url': url_for('image_rotate'),
        },
        {

            'image': url_for('icons', filename='resize.ico'),
            'title': _("Resize"),
            'subtitle': _("Resize an image file resolution (upscale or downscale)."),

            'url': url_for('image_resize'),
        },
        {

            'image': url_for('icons', filename='diagonal_line.ico'),
            'title': _("Antialias"),
            'subtitle': _("Applies antialias filter to an image file."),

            'url': url_for('image_antialias'),
        },
        {

            'image': url_for('icons', filename='blur.ico'),
            'title': _("Blur"),
            'subtitle': _("Applies gaussian blur to an image file."),

            'url': url_for('image_blur'),
        },
        {

            'image': url_for('icons', filename='color.ico'),
            'title': _("Enhance"),
            'subtitle': _("Enhance image color, brightness, contrast, or sharpness."),

            'url': url_for('image_enhance'),
        },
        {

            'image': url_for('icons', filename='filter.ico'),
            'title': _("Filter"),
            'subtitle': _("Applies multiples filters to an image file."),

            'url': url_for('image_filter'),
        },
        {

            'image': url_for('icons', filename='sharpener.ico'),
            'title': _("Sharpen"),
            'subtitle': _("Applies unsharp mask to an image file."),

            'url': url_for('image_unsharp'),
        },
        {

            'image': url_for('icons', filename='info.ico'),
            'title': _("Get info"),
            'subtitle': _("Get EXIF information about a image file."),

            'url': url_for('image_info'),
        },
    ]

    return render_template_string(str(
        PageCardGrid(
            *tools,
            nav_items=[
                home_nav_item(),
                image_index_nav_item(active=True),
            ],
            _title=f"{_('Image Tools')} - File Conversor",
        ))
    )
