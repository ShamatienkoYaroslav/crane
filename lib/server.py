import os
from flask import Flask, jsonify, request
from lib.crane import Crane
from lib.utils import Log

class Server:
    def __init__(self, crane):
        app = Flask(__name__)

        @app.route("/")
        def index():
            return jsonify(name='Crane', version='0.1')

        @app.route("/update")
        def update():
            Log.info(request)
            self.crane.image_pull();
            self.crane.container_remove()
            container_id = self.crane.container_run()
            return jsonify(containerId=container_id)

        @app.route("/restart")
        def restart():
            Log.info(request)
            self.crane.container_remove()
            container_id = self.crane.container_run()
            return jsonify(containerId=container_id)

        @app.route("/pull")
        def pull():
            Log.info(request)
            image_id = self.crane.image_pull();
            return jsonify(imageId=image_id)

        self.app = app
        self.crane = crane

    def run(self):
        self.app.run()
