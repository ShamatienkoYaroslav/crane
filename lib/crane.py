import os, stat
import docker
from lib.utils import Log

VOLUMES_IO_MODE                 = 'rw'
PATH_DOCKER_SOCKET              = 'unix://var/run/docker.sock'
RESTART_POLICY_MAX_RETRY_COUNT  = 5

class Crane:
    def __init__(self, container, image):
        self.containers = None;
        self.images     = None;

        self.container  = container
        self.image      = image

        # container params
        self.ports          = Crane.generate_ports_dict()
        self.restart_policy = Crane.generate_restart_policy()
        self.volumes        = Crane.generate_volumes()
        self.privileged     = Crane.is_privileged()

        # Docker remote API
        if Crane.docker_server_is_running():
            client = docker.DockerClient(base_url=PATH_DOCKER_SOCKET)
            self.containers = client.containers
            self.images     = client.images
        else:
            raise Crane.SocketError


    ### CONTAINER

    def container_remove(self):
        try:
            container = self.containers.get(self.container)
            container.remove(force=True)
            Log.info('Container %s was removed' % (container.short_id))
        except docker.errors.NotFound:
            Log.info('Can\'t find running container')
        except docker.errors.APIError:
            Log.err('Can\'t remove container')
        except AttributeError as ex:
            Log.err(ex)

    def container_run(self):
        container_id = None
        try:
            container = self.containers.run(self.image, detach=True, name=self.container, ports=self.ports, restart_policy=self.restart_policy, privileged=self.privileged, volumes=self.volumes)
            container_id = container.short_id
            Log.info('Container %s started' % (container_id))
        except docker.errors.ContainerError:
            Log.err('Can\'t run container')
        except docker.errors.ImageNotFound:
            Log.err('Can\'t find image %s' % (self.image))
        except docker.errors.APIError as ex:
            Log.err(ex, 'Some docker server error occurred while trying to run container with image %s' % (self.image))
        except AttributeError as ex:
            Log.err(ex)
        return container_id


    ### IMAGE

    def image_pull(self):
        image_id = None;
        try:
            image = self.images.pull(self.image)
            image_id = image.short_id
            Log.info('Pulled image %s' % (image_id))
        except docker.errors.APIError:
            Log.err('Some docker server error occurred while trying to pull image %s' % (self.image))
        except AttributeError as ex:
            Log.err(ex)
        return image_id


    ### OTHER
    @classmethod
    def docker_server_is_running(cls):
        path = os.environ.get('DOCKER_SOCKET')
        if path is None:
            path = '/var/run/docker.sock'

        mode = os.stat(path).st_mode
        if not stat.S_ISSOCK(mode):
            return False
        else:
            return True

    @classmethod
    def generate_ports_dict(cls):
        ports = os.environ.get('CRANE_CONTAINER_PORTS');
        if ports is not None:
            ports           = ports.split(':')
            host_ports      = ports[0].split('-')
            container_ports = ports[1].split('-')

            if len(host_ports) != len(container_ports):
                raise Crane.ContainersParamError('ports')

            ports = {}

            try:
                host_first_port      = int(host_ports[0])
                container_first_port = int(container_ports[0])

                quantity = len(host_ports)
                if quantity > 1:
                    host_last_port = int(host_ports[1])
                    quantity = host_last_port - host_first_port + 1

                    container_last_port = int(container_ports[1])
                    if host_last_port != container_last_port:
                        raise Crane.ContainersParamError('ports')
            except ValueError:
                raise Crane.ContainersParamError('ports')

            for enlarger in range(quantity):
                ports[str(container_first_port + enlarger) + '/tcp'] = host_first_port + enlarger

            return ports
        return {}

    @classmethod
    def generate_restart_policy(cls):
        restart_policy = os.environ.get('CRANE_CONTAINER_RESTART_POLICY');
        if restart_policy is not None:
            if restart_policy == 'always':
                return {'Name': 'always'}
            elif restart_policy == 'on-failure':
                return {'Name': 'on-failure', 'MaximumRetryCount': RESTART_POLICY_MAX_RETRY_COUNT}
            else:
                raise Crane.ContainersParamError('restart_policy')
        return {}

    @classmethod
    def is_privileged(cls):
        privileged = os.environ.get('CRANE_CONTAINER_PRIVILEGED');
        if privileged is not None:
            if privileged == 'True' or privileged == 'true':
                return True
            else:
                raise Crane.ContainersParamError('privileged')
        return False

    @classmethod
    def generate_volumes(cls):
        volumes = os.environ.get('CRANE_CONTAINER_VOLUMES');
        if volumes is not None:
            volumes_array = volumes.split(',')
            volumes = {}
            for volume in volumes_array:
                dirs = volume.split(':')
                if len(dirs) != 2:
                    raise Crane.ContainersParamError('volumes')

                host_dir      = dirs[0]
                container_dir = dirs[1]

                volumes[host_dir] = {'bind': container_dir, 'mode': VOLUMES_IO_MODE}
            return volumes
        return {}


    ### ERRORS

    class SocketError(BaseException):
        def __init__(self):
            self.message = 'No socket was specified';
        def __str__(self):
            return self.message

    class ContainersParamError(BaseException):
        def __init__(self, param):
            self.message = 'Parameter \"%s\" set incorrectly' % (param);
        def __str__(self):
            return self.message
