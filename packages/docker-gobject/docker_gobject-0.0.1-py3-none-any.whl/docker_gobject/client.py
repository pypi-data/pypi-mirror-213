import gi, logging, json

gi.require_version("Soup", "3.0")

from gi.repository import GObject, Gio, Soup, GLib
from docker_gobject.session import Session
from docker_gobject.containers import Containers
from docker_gobject.images import Images
from docker_gobject.authentication import AuthenticationMethod
from docker_gobject.monitor import EventMonitor

class DockerClient(GObject.Object):
    __gtype_name__ = "DockerClient"

    authentication_method: AuthenticationMethod
    """
    Authentication method for connecting to the Docker Engine
    """
    url: str = "http://localhost:2375"
    """
    If you are using the (TCP)`docker_gobject.authentication.AuthenticationMethod.TCP` protocol to connect to the Docker Engine, this is the API URL that will be used.
    """

    def __init__(self, authentication_method = AuthenticationMethod.SOCKET, url = "http://localhost:2375", path = "/run/docker.sock", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cancellable = Gio.Cancellable().new()
        sock = Gio.UnixSocketAddress.new(path)
        self.session = Session.get(sock, True)
        self.session.set_authentication_method(authentication_method)
        self.session.set_api_url(url)
        self.session.set_timeout(0)  # docker engine monitoring endpoint
        self.session.set_idle_timeout(0)
        if authentication_method is AuthenticationMethod.SOCKET:
            self.session.set_api_url("http://localhost")
        self.containers = Containers()
        self.images = Images()
        self.event_monitor = EventMonitor()
