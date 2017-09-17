import logging
from flask_restplus import Api
from setting import FLASK_DEBUG

log = logging.getLogger(__name__)

api = Api(version="1.0 (Edward's scissors)", title='Clipper API',
          description='Clipping geometries with a GeoServer layer.')


@api.errorhandler
def default_error_handler(e):
    print(e)
    message = 'An unhandled exception occurred.'
    log.exception(message)
    if not FLASK_DEBUG:
        return {'message': message}, 500
