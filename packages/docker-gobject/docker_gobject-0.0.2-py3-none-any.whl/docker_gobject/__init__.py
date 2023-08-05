"""
# Introduction
``docker_gobject`` is PyGObject wrapper for the ``dockerd`` daemon.

# Getting Started

When you connect to the daemon, you need to determine which method you will use. Currently, this library supports two types:

- UNIX socket
- TCP (HTTP requests)

The method you need to pick will be based on your daemon configuration.  By default, the Docker daemon listens on the unix socket and requires either `root` or the current user be apart of the ``docker`` user group.

If you are using a TCP connection, make sure the port matches the port you specified in your ``dockerd`` configuration.

For more information, please reference the [Docker documentation](https://docs.docker.com/engine/reference/commandline/dockerd/#examples).

Afer you have determined which method you will use to connect to the daemon, you need to specify the connection type with the ``docker_gobject.authentication.AuthenticationMethod`` class.

```python3
from docker_gobject import DockerClient, AuthenticationMethod


# UNIX socket
client = DockerClient(AuthenticationMethod.SOCKET)
client.containers.list()

# TCP connection
client = DockerClient(AuthenticationMethod.TCP, "http://localhost:5000")
client.containers.list()
```

# Standalone Example Usage

```python
import gi, json, dbus
from docker_gobject.client import DockerClient
from docker_gobject.authentication import AuthenticationMethod
from dbus.mainloop.glib import DBusGMainLoop

from gi.repository import Gio, GLib

def list_callback(success, error, data):
    containers = client.containers.from_json(data)
    for container in containers:
        print(container[0].id)

client = DockerClient(AuthenticationMethod.SOCKET)
client.containers.list(list_callback)


if __name__ == '__main__':

    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    try:
        GLib.MainLoop().run()
    except KeyboardInterrupt:
        GLib.MainLoop().quit()
```

# Issues
Please report any issues on the GitHub repository.

# Contact
If you need to contact me, please feel free to do so via my email: cameron@camerondahl.com

"""

__all__ = ["container", "containers", "client", "session", "authentication"]

from docker_gobject import *
