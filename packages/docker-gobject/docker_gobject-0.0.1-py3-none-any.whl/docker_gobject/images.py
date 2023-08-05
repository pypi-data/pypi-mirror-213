import gi, json
from typing import Callable
gi.require_version("Soup", "3.0")
gi.require_version("Gtk", "4.0")
from docker_gobject.session import Session
from docker_gobject.image import Image
from gi.repository import Gtk, GObject

class Images(GObject.Object):
    """
    Class to control images
    """

    session: Session

    def __init__(self, *args, **kwargs):
        GObject.Object.__init__(self)
        self.session = Session.get()

    def list(self, callback: Callable[[bool, bool, bytes], None]):
        self.session.make_api_call(self.session.api_url + "/images/json?all=true", callback)

    def from_json(self, data) -> Gtk.ListStore:
        """
        Converts the raw JSON image data into a Gtk.ListStore
        """
        images = Gtk.ListStore.new((Image,))
        d = json.loads(data.decode())
        for image in d:
            images.append([Image.from_json(image)])
        return images

    def get(self, name_or_id, callback: Callable[[bool, bool, bytes], None]):
        self.session.make_api_call(self.session.api_url + "/images/" + name_or_id + "/json", callback)
