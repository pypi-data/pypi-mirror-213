import requests
import json
import os
import sys
import logging

class IE(object):
    def __init__(self):
        try:
            os.environ["API_URL"]
        except KeyError:
            logging.error("Please set the environment variable API_URL")
            sys.exit(1)
        self.url = os.environ['API_URL']
        self.headers = requests.structures.CaseInsensitiveDict()
        self.headers["Accept"] = "application/json"
        self.headers["Content-Type"] = "application/json"
        self.headers["Accept-Encoding"] = "gzip, deflate, br"
        self.headers["Connection"] = "keep-alive"
        self.headers["Authorization"] = ""

    def is_api_online(self):
        return requests.get(self.url)

    def login(self, _email, _pass):
        endpoint = '/rpc/login'
        body = {"_email": _email, "_pass": _pass}
        r = requests.post(self.url + endpoint, json=body, headers=self.headers)
        if r and r.json()['token'] is not None:
            self.headers["Authorization"] = "Bearer " + '{token}'.format(token=r.json()['token'])
        else:
            logging.info('An error has occurred. {e}'.format(e=r.json()))
            quit()
        return

    def isea3h_stats(self):
        """API endpoint for isea3h_stats"""
        endpoint = '/isea3h_stats'
        return requests.get(self.url + endpoint, headers=self.headers)


    def isea3h_cell_by_point(self, _res, _x, _y, _srid):
        """API endpoint /rpc/isea3h_cell_by_point"""
        endpoint = '/rpc/isea3h_cell_by_point'
        if type(_res) != int:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_x) != float:
            logging.error('{}: {} is not {}'.format('_x', _x, 'numeric'))
        if type(_y) != float:
            logging.error('{}: {} is not {}'.format('_y', _y, 'numeric'))
        if type(_srid) != int:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        body = {
                "_res": _res,
                "_x": _x,
                "_y": _y,
                "_srid": _srid
               }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)