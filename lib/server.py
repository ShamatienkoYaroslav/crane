import os
from flask import Flask, jsonify, request
from lib.crane import Crane
from lib.utils import Log
from lib.env import env
from flask_cors import CORS, cross_origin

class Server:
    def __init__(self, crane):
        app = Flask(__name__)
        CORS(app)

        @app.route("/")
        def index():
            Log.info(request)
            image = env('CRANE_IMAGE')
            containerName = env('CRANE_NAME')
            ports = env('CRANE_CONTAINER_PORTS')
            restart = env('CRANE_CONTAINER_RESTART_POLICY', 'always')
            privileged = env('CRANE_CONTAINER_PRIVILEGED', 'true')
            volumes = env('CRANE_CONTAINER_VOLUMES')
            localPath = env('CRANE_PULL_IMAGE_LOCAL_PATH')
            ftp = env('CRANE_FTP_USE', 'false')
            ftpHost = env('CRANE_FTP_HOST')
            ftpUser = env('CRANE_FTP_USER')
            ftpCwd = env('CRANE_FTP_CWD')
            ftpFilename = env('CRANE_FTP_FN')
            info = self.crane.get_info()
            return jsonify(
                image=image,
                containerName=containerName,
                ports=ports,
                restart=restart,
                privileged=privileged,
                volumes=volumes,
                localPath=localPath,
                ftpUse=ftp,
                ftpHost=ftpHost,
                ftpUser=ftpHost,
                ftpCwd=ftpCwd,
                ftpFilename=ftpFilename,
                id=info['id'],
                shortId=info['short_id'],
                status=info['status'],
                attrs=info['attrs'],
                imageId=info['image_id'],
                imageShortId=info['image_short_id'],
                imageAttrs=info['image_attrs']
            )

        @app.route("/about")
        def about():
            Log.info(request)
            return jsonify(name='Crane', version='0.3')

        @app.route("/update")
        def update():
            Log.info(request)
            image_id = self.crane.image_pull();
            self.crane.container_remove()
            container_id = self.crane.container_run()
            return jsonify(imageId=image_id, containerId=container_id)

        @app.route("/start")
        def start():
            Log.info(request)
            container_id = self.crane.container_start();
            return jsonify(containerId=container_id)

        @app.route("/stop")
        def stop():
            Log.info(request)
            container_id = self.crane.container_stop();
            return jsonify(containerId=container_id)

        @app.route("/restart")
        def restart():
            Log.info(request)
            self.crane.container_remove()
            container_id = self.crane.container_run()
            return jsonify(containerId=container_id)

        @app.route("/remove")
        def remove():
            Log.info(request)
            container_id = self.crane.container_remove()
            return jsonify(containerId=container_id)

        @app.route("/pull")
        def pull():
            Log.info(request)
            image_id = self.crane.image_pull();
            return jsonify(imageId=image_id)

        self.app = app
        self.crane = crane

    def run(self):
        self.app.run(host='0.0.0.0')
