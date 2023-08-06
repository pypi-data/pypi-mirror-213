import json
import logging
import os
import tornado

import nbformat as nbf

from glob import glob
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VerifyAtlasInNotebook(APIHandler):
    @tornado.web.authenticated
    def post(self):
        environment_info = self.get_json_body()
        logging.info(f"Opened Filename => {environment_info['openedFilename']}")
        logging.info(f"Path to Notebook => {environment_info['pathToNotebook']}")
        logging.info(f"Daskhub URl => {environment_info['daskhubURL']}")
        logging.info(f"Username => {os.environ['JUPYTERHUB_USER']}")
        logging.info(f"User Directory => {os.getcwd()}")
        try:
            notebook = glob(environment_info['pathToNotebook'])
            ntbk = nbf.read(notebook[0], nbf.NO_CONVERT)
            logging.info(f"Notebook Metadata => {ntbk.metadata}")
            logging.info(f"AtlasID => {ntbk.metadata.get('atlas-id', None)}")
        except Exception as e:
            logging.info(f"Couldn't open/read the notebook in the specified path => {e}")
        else:
            logging.info(f"{json.dumps({'atlasId': ntbk.metadata.get('atlas-id', None)})}")
            self.finish(json.dumps({
                "atlasId": ntbk.metadata.get('atlas-id', None)
            }))


class CRUDAtlasId(APIHandler):
    @tornado.web.authenticated
    def post(self):
        environment_info = self.get_json_body()
        logging.info(f"Atlas ID => {environment_info['atlasId']}")
        logging.info(f"Action => {environment_info['action']}")
        logging.info(f"Path to Notebook => {environment_info['pathToNotebook']}")
        try:
            notebook = glob(environment_info['pathToNotebook'])
            ntbk = nbf.read(notebook[0], nbf.NO_CONVERT)
            if environment_info['action'] == 'set': 
                ntbk.metadata['atlas-id'] = environment_info['atlasId']
            
            if environment_info['action'] == 'delete':
                del ntbk.metadata['atlas-id']

            nbf.write(ntbk, notebook[0])
            logging.info(f"Notebook Path => {notebook[0]}")
            logging.info(f"Notebook Metadata => {ntbk.metadata}")
        except Exception as e:
            logging.info(f"Couldn't open/read the notebook in the specified path => {e}")
        else:
            logging.info(f"{json.dumps({'atlasId': ntbk.metadata.get('atlas-id', None)})}")
            self.finish(json.dumps({
                "atlasId": ntbk.metadata.get('atlas-id', None)
            }))


class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({
            "data": "This is /jupyterlab-voiceatlas/get_example endpoint!"
        }))


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupyterlab-voiceatlas", "get_example")
    verify_atlas = url_path_join(base_url, "jupyterlab-voiceatlas", "verify_atlas")
    crud_atlas = url_path_join(base_url, "jupyterlab-voiceatlas", "crud_atlas")
    handlers = [
        (route_pattern, RouteHandler),
        (verify_atlas, VerifyAtlasInNotebook),
        (crud_atlas, CRUDAtlasId)
    ]
    web_app.add_handlers(host_pattern, handlers)
