from label import CLIPPER_LABEL
from mvc.controller.flaskapi import api
from flask_restplus import fields, reqparse

clipper_arguments = reqparse.RequestParser()
clipper_arguments.add_argument(CLIPPER_LABEL['layer_id'], type=str, required=True, default='demo:greene_county_wetland',
                               help='usage: [workspace]:[layer]', location='args')
clipper_arguments.add_argument(CLIPPER_LABEL['geoserver_url'], type=str, required=True,
                               default='http://docker.for.mac.localhost/geoserver/wps',
                               help='example: http://localhost:6080/geoserver/wps', location='args')

crs = api.model('projection', {
    'name': fields.String(required=True, readOnly=True, description='Use OGC newest standard')
})

crs_properties = api.model('crs', {
    'properties': fields.Nested(crs, required=True, readOnly=True),
    'type': fields.String(required=True, readOnly=True, description="Must be 'name'")
})

properties = api.model('properties', {
    'property_1': fields.Date(readOnly=True, description='Date'),
    'property_2': fields.DateTime(readOnly=True, description='Date Time'),
    'property_3': fields.Float(readOnly=True, description='Value'),
    'property_4': fields.Integer(readOnly=True, description='Value'),
    'property_5': fields.String(readOnly=True, description='Text')
})

polygon_geometry = api.model('polygon.geometry', {
    'coordinates': fields.List(fields.List(fields.List(fields.Float)),
                               required=True, readOnly=True,
                               description='[[Longitude, Latitude]]'),
    'type': fields.String(required=True, readOnly=True, description='Polygon')
})

polygon_feature = api.model('polygon.feature', {
    'geometry': fields.Nested(polygon_geometry, required=True, readOnly=True),
    'properties': fields.Nested(properties, readOnly=True),
    'type': fields.String(required=True, readOnly=True, description="Must be 'Feature'")
})

polygon_post = api.model('polygon', {
    'crs': fields.Nested(crs_properties, required=True, readOnly=True),
    'features': fields.List(fields.Nested(polygon_feature), required=True, readOnly=True),
    'type': fields.String(required=True, readOnly=True, description="Must be 'FeatureCollection'")
})
