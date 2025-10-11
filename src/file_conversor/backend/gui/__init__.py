# src\file_conversor\backend\gui\__init__.py

# user-provided modules
from file_conversor.backend.gui.flask_app import FlaskApp
from file_conversor.backend.gui.flask_route import FlaskRoute

# routes
from file_conversor.backend.gui.doc import routes as doc_routes
from file_conversor.backend.gui.pdf import routes as pdf_routes
from file_conversor.backend.gui.ppt import routes as ppt_routes
from file_conversor.backend.gui.xls import routes as xls_routes

from file_conversor.backend.gui.icons import icons
from file_conversor.backend.gui.index import index


from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()

fapp = FlaskApp.get_instance()

fapp.add_route(doc_routes)
fapp.add_route(pdf_routes)
fapp.add_route(ppt_routes)
fapp.add_route(xls_routes)

fapp.add_route(FlaskRoute(
    rule="/icons/<path:filename>",
    handler=icons,
))

fapp.add_route(FlaskRoute(
    rule="/",
    handler=index
))

# # Register the blueprint
# app.register_blueprint(index_bp)
__all__ = ["FlaskApp"]
