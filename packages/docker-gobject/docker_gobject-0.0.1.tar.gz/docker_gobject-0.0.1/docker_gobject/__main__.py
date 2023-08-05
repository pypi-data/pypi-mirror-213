import dbus, json
from dbus.mainloop.glib import DBusGMainLoop
try:
    from docker_gobject.client import DockerClient
    from docker_gobject.authentication import AuthenticationMethod
    from docker_gobject.image import Image
except:
    print("DOCKER GOBJECT NOT INSTALLED")

from gi.repository import Gio, GLib
client = DockerClient(AuthenticationMethod.SOCKET)


if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    try:
        GLib.MainLoop().run()
    except KeyboardInterrupt:
        GLib.MainLoop().quit()


