import json
import logging
import requests
from mvc.controller.schema.ogc.epsg import WGS84

log = logging.getLogger(__name__)


class ServiceRegister(object):
    def __init__(self):
        self.services = json.loads(str('['
                                       '{"service": "clipper", "projection": "' + WGS84 + '"}'
                                       ']'))


class GsClipping(object):
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def get_clipper(self):
        headers = {
            'content-type': "application/xml",
            'cache-control': "no-cache"
        }
        response = requests.request("POST", self.url, data=self.data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return str('{"error": "' + str(response.status_code) + ': ' + str(response.content) + '"}')
