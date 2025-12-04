# src/file_conversor/backend/gui/_components/grid.py

from typing import Any

from file_conversor.utils.dominate_utils import div


def Cell(*content: Any, _class="", **kwargs):
    """
    Create a grid cell.

    :param content: The content of the cell.
    :param _class: Additional CSS classes for the cell.
    """
    with div(_class=f"cell {_class}", **kwargs) as cell:
        for item in content:
            if not item:
                continue
            cell.add(item)
    return cell


def FixedGrid(
        *cells,
        columns: str = 'auto',
        _class="",
        **kwargs,
):
    """
    Create a fixed grid layout.

    :param cells: The cells to be placed in the grid.
    :param columns: The number of columns in the grid. Options are 'auto', '0' upto '12'.
    :param _class: Additional CSS classes for the grid.
    """
    if columns != 'auto' and int(columns) not in range(0, 13):
        raise ValueError("columns must be 'auto' or an integer between 0 and 12.")
    with div(_class=f"fixed-grid has-{columns}-cols {_class}", **kwargs) as grid:
        with div(_class="grid") as inner_grid:
            for cell in cells:
                if not cell:
                    continue
                inner_grid.add(cell)
    return grid


def SmartGrid(
        *cells,
        _class="",
        **kwargs,
):
    """
    Create a smart grid layout.

    :param cells: The cells to be placed in the grid.
    :param _class: Additional CSS classes for the grid.
    """
    with div(_class=f"grid {_class}", **kwargs) as grid:
        for cell in cells:
            if not cell:
                continue
            grid.add(cell)
    return grid


__all__ = [
    'Cell',
    'SmartGrid',
    'FixedGrid',
]
