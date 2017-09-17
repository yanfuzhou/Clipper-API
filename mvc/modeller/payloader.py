import json
from mvc.controller.schema.ogc.epsg import code


def xmlwrapper(layer_id, geometries):
    geometries['crs']['properties']['name'] = 'urn:ogc:def:crs:EPSG::' + code[1]
    data = '<?xml version="1.0" encoding="UTF-8"?>' \
           '<wps:Execute version="1.0.0" service="WPS" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
           'xmlns="http://www.opengis.net/wps/1.0.0" xmlns:wfs="http://www.opengis.net/wfs" ' \
           'xmlns:wps="http://www.opengis.net/wps/1.0.0" xmlns:ows="http://www.opengis.net/ows/1.1" ' \
           'xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" ' \
           'xmlns:wcs="http://www.opengis.net/wcs/1.1.1" xmlns:xlink="http://www.w3.org/1999/xlink" ' \
           'xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsAll.xsd">' \
           '<ows:Identifier>gs:Clip</ows:Identifier>' \
           '<wps:DataInputs>' \
           '<wps:Input>' \
           '<ows:Identifier>features</ows:Identifier>' \
           '<wps:Reference mimeType="text/xml" xlink:href="http://geoserver/wfs" method="POST">' \
           '<wps:Body>' \
           '<wfs:GetFeature service="WFS" version="1.0.0" outputFormat="GML2" ' \
           'xmlns:demo="' + layer_id.split(':')[0] + '">' \
           '<wfs:Query typeName="' + layer_id + '"/>' \
           '</wfs:GetFeature>' \
           '</wps:Body>' \
           '</wps:Reference>' \
           '</wps:Input>' \
           '<wps:Input>' \
           '<ows:Identifier>clip</ows:Identifier>' \
           '<wps:Reference mimeType="application/json" xlink:href="http://geoserver/wps" method="POST">' \
           '<wps:Body>' \
           '<wps:Execute version="1.0.0" service="WPS">' \
           '<ows:Identifier>gs:CollectGeometries</ows:Identifier>' \
           '<wps:DataInputs>' \
           '<wps:Input>' \
           '<ows:Identifier>features</ows:Identifier>' \
           '<wps:Data>' \
           '<wps:ComplexData mimeType="application/json"><![CDATA[' + json.dumps(geometries) + ']]></wps:ComplexData>' \
           '</wps:Data>' \
           '</wps:Input>' \
           '</wps:DataInputs>' \
           '<wps:ResponseForm>' \
           '<wps:RawDataOutput mimeType="text/xml; subtype=gml/3.1.1">' \
           '<ows:Identifier>result</ows:Identifier>' \
           '</wps:RawDataOutput>' \
           '</wps:ResponseForm>' \
           '</wps:Execute>' \
           '</wps:Body>' \
           '</wps:Reference>' \
           '</wps:Input>' \
           '</wps:DataInputs>' \
           '<wps:ResponseForm>' \
           '<wps:RawDataOutput mimeType="application/json">' \
           '<ows:Identifier>result</ows:Identifier>' \
           '</wps:RawDataOutput>' \
           '</wps:ResponseForm>' \
           '</wps:Execute>'
    return data
