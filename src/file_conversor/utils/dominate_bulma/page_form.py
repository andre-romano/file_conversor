# src\file_conversor\utils\dominate_bulma\page_form.py

from typing import Any

# user-provided modules
from file_conversor.utils.bulma_utils.general import OverwriteFilesField

from file_conversor.utils.dominate_bulma.form_button import Button, ButtonsContainer
from file_conversor.utils.dominate_bulma.form import Form
from file_conversor.utils.dominate_bulma.breadcrumb import Breadcrumb
from file_conversor.utils.dominate_bulma.page_base import PageBase

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageForm(
        *form_fields,
        api_endpoint: str,
        nav_items: list[dict[str, Any]],
        _title: str,
        buttons: list[Any] | None = None,
        **kwargs: Any,
):
    """
    Create a page with a form.

    ```python
    nav_items = [{
        'icon': (Optional) The icon name to display alongside the label
        'label': The display text for the item,
        'url': The URL the item links to,
        'active': A boolean indicating if the item is the current page,
    }]
    ```

    :param form_fields: The fields to include in the form.
    :param api_endpoint: The API endpoint to submit the form to.
    :param nav_items: The breadcrumb navigation items.
    :param _title: The title of the page.
    :param buttons: Additional buttons to include in the form (optional).
    """
    return PageBase(
        Form(
            *form_fields,
            OverwriteFilesField(),
            ButtonsContainer(
                Button(
                    _("Execute"),
                    _class="is-primary",
                    _title=_("Execute operation"),
                    **{
                        ':class': """{
                        'is-loading': checkLoading(),
                        'is-cursor-progress': checkLoading(),
                    }""",
                        ':disabled': '!isValid || checkLoading()',
                        '@click': f'$store.form.submit($el.closest("form[x-data]"), `{api_endpoint}`)',
                    },
                ),
                *(buttons or []),
            ),
            _class='is-flex is-flex-direction-column is-align-items-flex-end is-full-width',
            **{'x-data': r"""{ 
                    isValid: false, 
                    elements: [],                    
                    checkLoading() {
                        return this.$store.status_bar.started && !this.$store.status_bar.finished;
                    },
                    updateValidity() {
                        let res = true;     
                        if (!this.elements || this.elements.length === 0) {   
                            this.elements = this.$el.querySelectorAll('.field[x-data]');
                        }
                        this.elements.forEach((item) => {
                            if (item === this.$el) return;
                            const data = Alpine.$data(item);
                            const valid = data.isValid;
                            if (valid === undefined) return;
                            if (!valid) {
                                res = false;
                            }
                        });
                        this.isValid = res;
                    },
                    init() {
                        this.updateValidity();
                    },  
               }"""},
            **kwargs,
        ),
        _title=_title,
        nav_title=Breadcrumb(*nav_items),
    )


__all__ = [
    "PageForm",
]
