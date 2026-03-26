# src/file_conversor/gui/_widgets/stacked_router.py


from PySide6.QtWidgets import QAbstractButton, QStackedWidget, QWidget


class StackedRouter(QStackedWidget):
    def _fix_visual_glitches(self, widget: QWidget) -> None:
        widget.resize(self.size())  # ensure the page widget fills the router area
        widget.ensurePolished()  # apply stylesheets and update the widget's appearance NOW
        match widget.layout():
            case None:
                """ page has no layout, so we can just show it without worrying about unpolished child widgets """
            case l:
                l.activate()  # force immediate layout update to ensure all child widgets are properly arranged and styled before showing the page

    def __init__(self, pages: list[tuple[type[QWidget], QAbstractButton]], initial_page: int = 0) -> None:
        super().__init__()

        self._pages: list[QWidget | None] = [None for _ in pages]

        def on_click(i: int, page_type: type[QWidget], btn: QAbstractButton) -> None:
            # create page object if it doesn't exist yet and add it to the stack
            if self._pages[i] is None:
                widget = page_type()
                self._pages[i] = widget
                self.addWidget(widget)  # add page to stack
                self._fix_visual_glitches(widget)
            # show the page
            match self._pages[i]:
                case None:
                    raise RuntimeError(f"Failed to create page widget for {page_type}.")
                case w:
                    self.setCurrentWidget(w)  # show the page
            # update button states (set clicked button as checked and others as unchecked)
            for _, button in pages:
                button.setChecked(button is btn)

        # Add pages to the stack (Index 0 is Home, Index 1 is Settings)
        for idx, (page_type, button) in enumerate(pages):
            # add page to stack and connect button to show the page when clicked
            button.clicked.connect(lambda _checked=False, i=idx, p=page_type, btn=button: on_click(i, p, btn))

        # simulate click on the initial page button to show it
        if not (0 <= initial_page < len(pages) and pages):
            raise RuntimeError("Invalid initial page index or empty pages list.")
        page_type, btn = pages[initial_page]
        on_click(initial_page, page_type, btn)


__all__ = [
    "StackedRouter",
]
