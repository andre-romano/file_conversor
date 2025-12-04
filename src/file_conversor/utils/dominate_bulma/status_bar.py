# src\file_conversor\backend\gui\_components\status_bar.py

from file_conversor.utils.dominate_bulma.progress import Progress
from file_conversor.utils.dominate_utils import div, span


def StatusBar(**kwargs):
    with div(
        _id="status_bar",
        _class="status-bar is-fixed-bottom is-flex is-justify-content-space-between "
               "is-align-items-center is-size-6 p-1 pl-3 pr-3",
        **{"x-data": "{ }"},
        **kwargs
    ) as status_bar:

        # Left/start section (status message)
        with div(_class="status-bar-start is-flex is-align-items-center"):
            span(
                "STATUS:",
                _class="has-text-weight-bold mr-2",
                **{
                    ":class": """{
                        'is-flex': $store.status_bar.message !== '', 
                        'is-hidden': $store.status_bar.message === '',
                    }"""
                }
            )
            span("", _class="status-message", **{"x-text": "$store.status_bar.message"})

        # Center section (progress)
        with div(
            _class="status-bar-center is-align-items-center is-flex-grow-1 mx-6 px-6",
            **{
                ":class": """{
                    'is-flex': (typeof $store.status_bar.progress === 'number'), 
                    'is-hidden': (typeof $store.status_bar.progress !== 'number'),
                }"""
            }
        ):
            Progress(_class="status-progress-bar is-small is-success my-0 mr-3")
            span(
                _class="status-progress-text",
                **{
                    ":class": """{
                        'is-hidden': (typeof $store.status_bar.progress !== 'number' || $store.status_bar.progress < 0)
                    }""",
                    "x-text": "`${Math.round($store.status_bar.progress)}%`"
                }
            )

        # Right/end section (time)
        with div(
            _class="status-bar-end is-align-items-center",
            **{
                ":class": """{
                    'is-flex': (typeof $store.status_bar.time === 'number'), 
                    'is-hidden': (typeof $store.status_bar.time !== 'number'),
                }"""
            }
        ):
            span(
                _class="status-time",
                **{
                    "x-text": "new Date($store.status_bar.time * 1000).toISOString().substring(11, 19)"
                }
            )
    return status_bar


__all__ = ["StatusBar"]
