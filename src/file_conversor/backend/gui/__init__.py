# src\file_conversor\backend\gui\__init__.py

# user-provided modules
from file_conversor.backend.gui.web_app import *

from file_conversor.backend.gui.flask_api import *
from file_conversor.backend.gui.flask_route import *
from file_conversor.backend.gui.flask_api_status import *

# routes
from file_conversor.backend.gui._api import routes as api_routes

from file_conversor.backend.gui.audio import routes as audio_routes
from file_conversor.backend.gui.config import routes as config_routes
from file_conversor.backend.gui.doc import routes as doc_routes
from file_conversor.backend.gui.ebook import routes as ebook_routes
from file_conversor.backend.gui.hash import routes as hash_routes
from file_conversor.backend.gui.image import routes as image_routes
from file_conversor.backend.gui.pdf import routes as pdf_routes
from file_conversor.backend.gui.ppt import routes as ppt_routes
from file_conversor.backend.gui.text import routes as text_routes
from file_conversor.backend.gui.video import routes as video_routes
from file_conversor.backend.gui.xls import routes as xls_routes

from file_conversor.backend.gui.icons import routes as icons_routes
from file_conversor.backend.gui.index import routes as index_routes


from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()

fapp = WebApp.get_instance()


# add context processors
fapp.add_context_processor(lambda: {
    'app': {
        'title': 'File Conversor',
        'version': Environment.get_version(),
    },
    '_base_status_bar': {
        'modal': {
            'title': _('Status Error'),
            'error': _('An error occurred while fetching the status'),
            'lost_conn': {
                'title': _('Connection Lost'),
                'msg': _('Lost connection to the server. Please check your network connection and try again.'),
            },
        },
        'processing': _('Processing...'),
        'failed': _('Failed'),
        'lost_conn': _('Connection Lost'),
        'completed': _('Completed'),
    },
    '_base_navbar': {
        'shutdown': {
            'btn_label': _('Shutdown'),
            'title': _('Server Shutdown'),
            'success': _('Server has been shut down successfully. Restart the app to use it again.'),
            'error': _('Unable to shut down the server'),
        },
    }
})

# api
fapp.add_route(api_routes())

# office
fapp.add_route(doc_routes())
fapp.add_route(xls_routes())
fapp.add_route(ppt_routes())

# other files
fapp.add_route(audio_routes())
fapp.add_route(video_routes())
fapp.add_route(image_routes())
fapp.add_route(pdf_routes())
fapp.add_route(ebook_routes())
fapp.add_route(text_routes())
fapp.add_route(hash_routes())

# UTILS CONFIG
fapp.add_route(config_routes())

fapp.add_route(icons_routes())
fapp.add_route(index_routes())

# export
__all__ = [
    "WebApp",
    "FlaskApi",
    "FlaskRoute",
    "FlaskApiStatus",
    'FlaskApiStatusCompleted',
    'FlaskApiStatusProcessing',
    'FlaskApiStatusReady',
    'FlaskApiStatusError',
    'FlaskApiStatusUnknown',
]
