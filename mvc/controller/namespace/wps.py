import json
import logging
from flask import request
from flask_restplus import Resource
from mvc.controller.schema import clipper
from mvc.controller.flaskapi import api
from mvc.modeller import ServiceRegister, GsClipping
from mvc.modeller.payloader import xmlwrapper
from mvc.controller.parser import clipper_arguments, polygon_post
from mvc.controller.parser.label import CLIPPER_LABEL

ns = api.namespace('wps', description='Perform web spatial analysis')
log = logging.getLogger(__name__)


@ns.route('/')
class GetWPSCapabilities(Resource):
    @api.marshal_list_with(clipper)
    @api.response(201, 'clipper is running!')
    def get(self):
        """
        Returns capabilities.
        """
        return ServiceRegister().services


@ns.route('/clip')
class ClipperMethod(Resource):
    @api.response(201, 'Clipper successfully created!')
    @api.doc(params={'layer_id': "usage: [workspace]:[layer]"})
    @api.doc(params={'geoserver_url': "example: http://localhost:6080/geoserver/wps"})
    @api.doc(params={'payload': "single polygon in geojson format with WGS84 projection"})
    @api.expect(polygon_post, clipper_arguments, validate=True)
    def post(self):
        """
        Clipper geometries.
        """
        args = clipper_arguments.parse_args(request)
        layer_id = args.get(CLIPPER_LABEL['layer_id'])
        if ':' in layer_id:
            geoserver_url = args.get(CLIPPER_LABEL['geoserver_url'])
            payload_data = xmlwrapper(layer_id, request.json)
            result = GsClipping(url=geoserver_url, data=payload_data).get_clipper()
            return result
        else:
            return json.loads(str('{"error": "layer_id must be like [workspace]:[layer]"}'))
