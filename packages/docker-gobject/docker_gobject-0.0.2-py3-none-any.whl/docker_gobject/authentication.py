"""
# Connection to the ``dockerd`` daemon

To connect to the ``dockerd`` daemon, specify the connection type by using the  ``AuthenticationMethod`` enum, like so:

```python
client = DockerClient(AuthenticationMethod.SOCKET)
```
"""
from enum import Enum
class AuthenticationMethod(Enum):
     """
     Authentication method for connecting to the Docker daemon

     There are two connection types supported by ``docker_gobject``:
        - Unix socket
        - TCP (HTTP requests)


     By default, the Docker daemon listens on the unix socket and requires either `root` or the current user be apart of the ``docker`` user group.

     For more information, please reference the [Docker documentation](https://docs.docker.com/engine/reference/commandline/dockerd/#examples).
     """
     SOCKET = "SOCKET"
     """ The default socket location is ``/var/run/docker.sock`` """
     TCP = "TCP"
