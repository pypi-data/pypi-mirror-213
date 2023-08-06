from flask import Flask
from flask_restx import Api
from os import getenv

from gevent.pywsgi import WSGIServer

DEBUG = getenv('DEBUG',True)
PORT = getenv('PORT',8080)

class ServerInstance():

    
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app
                       ,version='1.0'
                       , title='Best Frame'
                       , description='Liveness Best Frame')
        
    def debug(self):
        self.app.run(
            debug=DEBUG
        )
    
    def production(self):
        http_server = WSGIServer(('0.0.0.0',PORT),self.app)
        http_server.serve_forever()

    def run(self):
        if not DEBUG:
            self.debug()
            return
        self.production()

server = ServerInstance()