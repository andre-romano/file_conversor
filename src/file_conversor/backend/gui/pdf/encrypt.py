# src/file_conversor/backend/gui/pdf/encrypt.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.pdf._dom_page import pdf_encrypt_nav_item, pdf_index_nav_item

from file_conversor.utils.bulma_utils import InputFilesField, OutputDirField, PDFEncryptionAlgorithmField, PDFPasswordField
from file_conversor.utils.dominate_bulma import SmartGrid, Cell, FormFieldCheckbox, Tabs, PageForm

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def TabGeneral() -> list | tuple:
    return [
        InputFilesField(
            *PyPDFBackend.SUPPORTED_IN_FORMATS,
            description=_("PDF files"),
        ),
        PDFEncryptionAlgorithmField(),
        PDFPasswordField(
            _validation_expr="value.length > 0",
            _name="owner-password",
            help=_("Owner password used to encrypt the PDF files. Owner has ALL THE PERMISSIONS."),
            label_text=_("Owner Password"),
        ),
        OutputDirField(),
    ]


def TabAdvanced() -> list | tuple:
    return [
        PDFPasswordField(
            _name="user-password",
            help=_("User password used to encrypt the PDF files. User has ONLY THE PERMISSIONS specified below. Leave blank if not needed."),
            label_text=_("User Password"),
        ),
        SmartGrid(
            Cell(
                FormFieldCheckbox(
                    _name="annotate",
                    current_value="off",
                    help=_("Allow annotations (comments, highlight text, etc) in the encrypted PDF files."),
                    label_text=_("Allow annotations"),
                    reverse=True,
                ),
            ),
            Cell(
                FormFieldCheckbox(
                    _name="fill_forms",
                    current_value="off",
                    help=_("Allow fill forms in the encrypted PDF files."),
                    label_text=_("Allow fill forms"),
                    reverse=True,
                ),
            ),
            Cell(
                FormFieldCheckbox(
                    _name="modify",
                    current_value="off",
                    help=_("Allow encrypted PDF modifications."),
                    label_text=_("Allow modify"),
                    reverse=True,
                ),
            ),
            Cell(
                FormFieldCheckbox(
                    _name="modify_pages",
                    current_value="off",
                    help=_("Allow modifying pages (add, delete, rotate, reorder) in the encrypted PDF files."),
                    label_text=_("Allow modify pages"),
                    reverse=True,
                ),
            ),
            Cell(
                FormFieldCheckbox(
                    _name="copy",
                    current_value="off",
                    help=_("Allow copying content from the encrypted PDF files."),
                    label_text=_("Allow copy"),
                    reverse=True,
                ),
            ),
            Cell(
                FormFieldCheckbox(
                    _name="accessibility",
                    current_value="on",
                    help=_("Allow accessibility features (screen readers, etc) in the encrypted PDF files."),
                    label_text=_("Allow accessibility features"),
                    reverse=True,
                ),
            ),
            Cell(
                FormFieldCheckbox(
                    _name="print_lq",
                    current_value="on",
                    help=_("Allow encrypted PDF printing (low quality)."),
                    label_text=_("Allow print low quality"),
                    reverse=True,
                ),
            ), Cell(
                FormFieldCheckbox(
                    _name="print_hq",
                    current_value="on",
                    help=_("Allow encrypted PDF printing (high quality)."),
                    label_text=_("Allow print high quality"),
                    reverse=True,
                ),
            ),
            _class="is-col-min-12 is-gap-2",
        ),
    ]


def PagePDFEncrypt():
    return PageForm(
        Tabs(
            {
                'label': _('General'),
                'icon': 'cog',
                'content': TabGeneral(),
            },
            {
                'label': _('Advanced'),
                'icon': 'tools',
                'content': TabAdvanced(),
            },
            active_tab=_('General'),
            _class="""
                is-toggle 
                is-toggle-rounded 
                is-flex 
                is-full-width 
                is-flex-direction-column 
                is-align-items-center
                mb-4
            """,
            _class_headers="mb-4",
            _class_content="is-full-width",
        ),
        api_endpoint=f"{url_for('api_pdf_encrypt')}",
        nav_items=[
            home_nav_item(),
            pdf_index_nav_item(),
            pdf_encrypt_nav_item(active=True),
        ],
        _title=f"{_('PDF Encrypt')} - File Conversor",
    )


def pdf_encrypt():
    return render_template_string(str(
        PagePDFEncrypt()
    ))
