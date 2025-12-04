# src/file_conversor/backend/gui/config/_tab_general.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.utils.dominate_bulma import FormFieldCheckbox, FormFieldHorizontal, FormFieldInput, FormFieldSelect
from file_conversor.utils.bulma_utils import OutputDirField

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import AVAILABLE_LANGUAGES, get_translation, get_language_name

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def TabConfigGeneral() -> tuple | list:
    languages = [
        (k, get_language_name(k))
        for k in AVAILABLE_LANGUAGES
    ]
    languages.sort(key=lambda x: x[1])  # sort by language name

    return (
        OutputDirField(
            _name="gui-output-dir",
            help=_("Select the default output directory for saving converted files."),
            label_text=_("Output Directory"),
        ),
        FormFieldHorizontal(
            FormFieldSelect(
                *languages,
                current_value=CONFIG['language'],
                _name="language",
                help=_("Select the desired language for the user interface."),
            ),
            label_text=_("Language"),
        ),
        FormFieldHorizontal(
            FormFieldInput(
                validation_expr="Number.parseInt(value) >= 1",
                current_value=CONFIG['gui-zoom'],
                _name="gui-zoom",
                _type="number",
                help=_("Set the default zoom level for the user interface. Valid values are >= 1 (100 = normal size, 150 = 1.5x size, etc)."),
                x_init="""
                    let timeout;
                    this.$watch('value', (newValue) => {
                        clearTimeout(timeout);
                        timeout = setTimeout(() => {
                            set_zoom(newValue);
                        }, 1500);
                    });
                """,

            ),
            label_text=_("GUI Zoom Level (%)"),
        ),
        FormFieldHorizontal(
            FormFieldInput(
                validation_expr="Number.parseInt(value) >= 60",
                current_value=CONFIG['cache-expire-after'],
                _name="cache-expire-after",
                _type="number",
                help=_("HTTP cache expiration time in seconds (e.g., 1h = 3600 secs, 1d = 86400 secs). Minimum of 60 seconds."),
            ),
            label_text=_("HTTP Cache Expiration (secs)"),
        ),
        FormFieldCheckbox(
            current_value=CONFIG['cache-enabled'],
            _name="cache-enabled",
            label_text=_('Enable HTTP cache.'),
            help=_('If enabled, the application will use HTTP cache to improve performance.'),
        ),
        FormFieldCheckbox(
            current_value=CONFIG['install-deps'],
            _name="install-deps",
            label_text=_('Automatic install of missing dependencies, on demand.'),
            help=_('If enabled, the application will attempt to automatically install any missing dependencies when needed.'),
        ),
    )


__all__ = ['TabConfigGeneral']
