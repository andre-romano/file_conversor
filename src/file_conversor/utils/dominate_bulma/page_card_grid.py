# src\file_conversor\utils\dominate_bulma\page_card_grid.py

from typing import Any

# user-provided modules
from file_conversor.utils.dominate_bulma.breadcrumb import Breadcrumb
from file_conversor.utils.dominate_bulma.card import Card
from file_conversor.utils.dominate_bulma.figure import Figure
from file_conversor.utils.dominate_bulma.grid import Cell, SmartGrid
from file_conversor.utils.dominate_bulma.media import Media
from file_conversor.utils.dominate_bulma.page_base import PageBase

from file_conversor.utils.dominate_utils import a, div, p

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageCardGrid(
        *card_items: dict[str, str],
        nav_items: list[dict[str, Any]],
        _title: str,
        **kwargs,
):
    """
    Create a page with a grid of cards.

    ```python
    card_items = [{
        'image': The URL of the image to display on the card,
        'title': The title text of the card,
        'subtitle': The subtitle text of the card,
        'url': The URL the card links to,
    }]

    nav_items = [{
        'icon': (Optional) The icon name to display alongside the label
        'label': The display text for the item,
        'url': The URL the item links to,
        'active': A boolean indicating if the item is the current page,
    }]
    ```

    :param card_items: The items to display in the card grid. Each item should be a dictionary with 'image', 'title', 'subtitle', and 'url' keys.
    :param nav_items: The breadcrumb navigation items.
    :param _title: The title of the page.
    :param kwargs: Additional keyword arguments for the PageBase.
    """
    return PageBase(
        SmartGrid(
            *[
                Cell(
                    a(
                        Card(
                            Media(
                                left=Figure(_src=item['image'], _class="is-48x48"),
                                content=div(
                                    p(item['title'], _class="title is-4"),
                                    p(item['subtitle'], _class="subtitle is-6"),
                                ),
                            ),
                        ),
                        _href=item['url'],
                    )
                )
                for item in card_items
                if item
            ],
            _class="is-col-min-12 is-gap-2",
        ),
        nav_title=Breadcrumb(*nav_items),
        _title=_title,
        **kwargs,
    )


__all__ = [
    "PageCardGrid",
]
