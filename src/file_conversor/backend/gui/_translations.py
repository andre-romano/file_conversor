# src/file_conversor/backend/gui/_translations.py

# user-provided modules
from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def ctx_processors():
    return {
        'i18n': {
            'shutdown': {
                'btn_label': _('Shutdown'),
                'title': _('Server Shutdown'),
                'success': _('Server has been shut down successfully. Restart the app to use it again.'),
                'error': _('Unable to shut down the server'),
            }
        }
    }


__all__ = ['ctx_processors']
