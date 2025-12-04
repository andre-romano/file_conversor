# src/file_conversor/backend/gui/_components/visibility.py

class Visibility:
    IS_BLOCK = "is-block"
    IS_INLINE = "is-inline"
    IS_INLINE_BLOCK = "is-inline-block"
    IS_FLEX = "is-flex"
    IS_INLINE_FLEX = "is-inline-flex"
    IS_INVISIBLE = "is-invisible"
    IS_HIDDEN = "is-hidden"
    IS_SR_ONLY = "is-sr-only"


class IsFlexOnly:
    MOBILE = "is-flex-mobile"
    TABLET = "is-flex-tablet-only"
    DESKTOP = "is-flex-desktop-only"
    WIDESCREEN = "is-flex-widescreen-only"


class IsFlexUpTo:
    TOUCH = "is-flex-touch"
    TABLET = "is-flex-tablet"
    DESKTOP = "is-flex-desktop"
    WIDESCREEN = "is-flex-widescreen"
    FULLHD = "is-flex-fullhd"


class IsHiddenOnly:
    MOBILE = "is-hidden-mobile"
    TABLET = "is-hidden-tablet-only"
    DESKTOP = "is-hidden-desktop-only"
    WIDESCREEN = "is-hidden-widescreen-only"


class IsHiddenUpTo:
    TOUCH = "is-hidden-touch"
    TABLET = "is-hidden-tablet"
    DESKTOP = "is-hidden-desktop"
    WIDESCREEN = "is-hidden-widescreen"
    FULLHD = "is-hidden-fullhd"


__all__ = [
    'Visibility',
    'IsFlexOnly',
    'IsFlexUpTo',
    'IsHiddenOnly',
    'IsHiddenUpTo',
]
