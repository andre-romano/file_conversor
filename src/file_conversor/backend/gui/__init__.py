# src\file_conversor\backend\gui\__init__.py

# user-provided modules
from file_conversor.backend.gui.flask_app import FlaskApp
from file_conversor.backend.gui.flask_route import FlaskRoute

# routes
from file_conversor.backend.gui._api import routes as api_routes

from file_conversor.backend.gui.audio import routes as audio_routes
from file_conversor.backend.gui.config import routes as config_routes
from file_conversor.backend.gui.doc import routes as doc_routes
from file_conversor.backend.gui.ebook import routes as ebook_routes
from file_conversor.backend.gui.hash import routes as hash_routes
from file_conversor.backend.gui.image import routes as image_routes
from file_conversor.backend.gui.pdf import routes as pdf_routes
from file_conversor.backend.gui.pipeline import routes as pipeline_routes
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

fapp = FlaskApp.get_instance()

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
fapp.add_route(pipeline_routes())

fapp.add_route(icons_routes())
fapp.add_route(index_routes())

# export
__all__ = ["FlaskApp"]
