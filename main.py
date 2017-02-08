#!/usr/bin/env python3

from lib.crane import Crane
from lib.server import Server
from lib.utils import Log

try:
    crane = Crane(container='atom', image='princip/atom2:x')
    server = Server(crane)
    server.run()
except (Crane.SocketError, Crane.ContainersParamError) as ex:
    Log.err(ex)
    Log.info('CRANE WAS NOT STARTED')
