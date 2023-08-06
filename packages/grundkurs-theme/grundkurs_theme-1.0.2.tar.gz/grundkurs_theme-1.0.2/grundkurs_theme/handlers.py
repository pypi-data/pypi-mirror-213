import os
import json
import hashlib

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join

import tornado
from tornado.web import StaticFileHandler

import requests


class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def post(self):
        data = self.get_json_body()
        headers = {
            "Content-Type": "application/json"
        }


        # Get and hash user name
        try:
            username = os.environ["RENKU_USERNAME"] 
            user_hash = hashlib.sha256(username.encode('utf-8')).hexdigest()
        except:
            print("Warning: username not found!")
            # NOTE: For now we only allow loged in renku users to submit feedback
            return

        # Setup data
        url = data['url']
        data = {
            'cell_id': data['cellId'],
            'value': data['value'],
            'user_hash': user_hash
        }
        
        response = requests.post(url, json=data, headers=headers)
        self.finish(json.dumps(data))


def setup_handlers(web_app, url_path):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]

    # Prepend the base_url so that it works in a JupyterHub setting
    route_pattern = url_path_join(base_url, url_path, "feedback")
    handlers = [(route_pattern, RouteHandler)]
    web_app.add_handlers(host_pattern, handlers)