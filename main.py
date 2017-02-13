#!/usr/bin/env python3

from lib.crane import Crane
from lib.server import Server
from lib.utils import Log
from lib.env import env

try:
    container = env('CRANE_NAME')
    image = env('CRANE_IMAGE')
    if container is None:
        raise Crane.ContainersParamError('name')
    if image is None:
        raise Crane.ContainersParamError('image')

    crane = Crane(container, image)
    server = Server(crane)
    server.run()
except (Crane.SocketError, Crane.ContainersParamError) as ex:
    Log.err(ex)
    Log.info('CRANE WAS NOT STARTED')
