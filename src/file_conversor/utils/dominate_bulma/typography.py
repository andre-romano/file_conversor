# src/file_conversor/backend/gui/_components/typography.py

class TextSize:
    SIZE_1 = "is-size-1"
    SIZE_2 = "is-size-2"
    SIZE_3 = "is-size-3"
    SIZE_4 = "is-size-4"
    SIZE_5 = "is-size-5"
    SIZE_6 = "is-size-6"
    SIZE_7 = "is-size-7"


class TextAlign:
    LEFT = "has-text-left"
    CENTERED = "has-text-centered"
    RIGHT = "has-text-right"
    JUSTIFIED = "has-text-justified"


class TextTransform:
    UPPERCASE = "is-uppercase"
    LOWERCASE = "is-lowercase"
    CAPITALIZED = "is-capitalized"
    UNDERLINE = "is-underlined"
    ITALIC = "is-italic"


class TextWeight:
    LIGHT = "has-text-weight-light"
    NORMAL = "has-text-weight-normal"
    MEDIUM = "has-text-weight-medium"
    SEMIBOLD = "has-text-weight-semibold"
    BOLD = "has-text-weight-bold"
    EXTRABOLD = "has-text-weight-extrabold"


class TextFont:
    MONOSPACE = "is-family-monospace"
    SANS_SERIF = "is-family-sans-serif"
    PRIMARY = "is-family-primary"
    SECONDARY = "is-family-secondary"
    CODE = "is-family-code"


__all__ = [
    'TextSize',
    'TextAlign',
    'TextTransform',
    'TextWeight',
    'TextFont',
]
