# src/file_conversor/backend/gui/_components/_class.py


class FlexWrap:
    NO_WRAP = "is-flex-wrap-nowrap"
    WRAP = "is-flex-wrap-wrap"
    WRAP_REVERSE = "is-flex-wrap-wrap-reverse"


class FlexDirection:
    ROW = "is-flex-direction-row"
    ROW_REVERSE = "is-flex-direction-row-reverse"
    COLUMN = "is-flex-direction-column"
    COLUMN_REVERSE = "is-flex-direction-column-reverse"


class FlexJustifyContent:
    FLEX_START = "is-justify-content-flex-start"
    FLEX_END = "is-justify-content-flex-end"
    CENTER = "is-justify-content-center"
    SPACE_BETWEEN = "is-justify-content-space-between"
    SPACE_AROUND = "is-justify-content-space-around"
    SPACE_EVENLY = "is-justify-content-space-evenly"


class FlexAlignItems:
    FLEX_START = "is-align-items-flex-start"
    CENTER = "is-align-items-center"
    FLEX_END = "is-align-items-flex-end"
    SELF_START = "is-align-items-self-start"
    SELF_END = "is-align-items-self-end"
    START = "is-align-items-start"
    END = "is-align-items-end"
    BASELINE = "is-align-items-baseline"
    STRETCH = "is-align-items-stretch"


class FlexAlignContent:
    FLEX_START = "is-align-items-flex-start"
    CENTER = "is-align-items-center"
    FLEX_END = "is-align-items-flex-end"
    START = "is-align-items-start"
    END = "is-align-items-end"
    BASELINE = "is-align-items-baseline"
    STRETCH = "is-align-items-stretch"
    SPACE_AROUND = "is-align-items-space-around"
    SPACE_BETWEEN = "is-align-items-space-between"
    SPACE_EVENLY = "is-align-items-space-evenly"


class FlexAlignSelf:
    AUTO = "is-align-self-auto"
    FLEX_START = "is-align-self-flex-start"
    CENTER = "is-align-self-center"
    FLEX_END = "is-align-self-flex-end"
    START = "is-align-self-start"
    END = "is-align-self-end"
    BASELINE = "is-align-self-baseline"
    STRETCH = "is-align-self-stretch"


class FlexGrow:
    GROW_0 = "is-flex-grow-0"
    GROW_1 = "is-flex-grow-1"
    GROW_2 = "is-flex-grow-2"
    GROW_3 = "is-flex-grow-3"
    GROW_4 = "is-flex-grow-4"
    GROW_5 = "is-flex-grow-5"


class FlexShrink:
    SHRINK_0 = "is-flex-shrink-0"
    SHRINK_1 = "is-flex-shrink-1"
    SHRINK_2 = "is-flex-shrink-2"
    SHRINK_3 = "is-flex-shrink-3"
    SHRINK_4 = "is-flex-shrink-4"
    SHRINK_5 = "is-flex-shrink-5"


__all__ = [
    'FlexWrap',
    'FlexDirection',
    'FlexJustifyContent',
    'FlexAlignItems',
    'FlexAlignContent',
    'FlexAlignSelf',
    'FlexGrow',
    'FlexShrink',
]
