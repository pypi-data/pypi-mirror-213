import gi, json
from docker_gobject.session import Session

gi.require_version("Soup", "3.0")

from gi.repository import Soup, GObject, Gio, GLib

class EventMonitor(GObject.Object):
    __gsignals__ = {
        "image_deleted": (
            GObject.SIGNAL_RUN_LAST,
            None,
            (str,),
        ),
        "image_pull": (
            GObject.SIGNAL_RUN_LAST,
            None,
            (str,),
        ),
        "finished_loading": (
            GObject.SIGNAL_RUN_LAST,
            None,
            (),
        ),
        "start_loading": (
            GObject.SIGNAL_RUN_LAST,
            None,
            (),
        ),
        "monitor_status_changed": (
            GObject.SIGNAL_RUN_LAST,
            None,
            (bool,),
        ),
    }
    session: Session

    def __init__(self):
        GObject.Object.__init__(self)
        self.session = Session.get()

    def monitor_events(self):
        def on_response(source: Soup.Session, res: Gio.Task, data: Soup.Message):
            input_stream = None
            try:
                input_stream: Gio.InputStream = source.send_finish(res)
                self.emit("monitor_status_changed", True)
            except Exception as e:
                self.emit("monitor_status_changed", False)

            def on_callback(dataInputStream, res, user_data):
                json_data = {}
                try:
                    lineout, _ = dataInputStream.read_line_finish(res)
                    out = lineout.decode()
                    json_data = json.loads(out)
                    print(json_data)
                except Exception as e:
                    self.emit("monitor_status_changed", False)
                if "status" in json_data:
                    if json_data["status"] == "delete":
                        self.emit("image_delete", json_data["id"])
                    elif json_data["status"] == "pull":
                        self.emit("image_pull", json_data["id"])
                    data_input_stream.read_line_async(
                        GLib.PRIORITY_DEFAULT, self.session.cancellable, on_callback, None
                    )

            if input_stream:
                data_input_stream = Gio.DataInputStream.new(input_stream)
                data_input_stream.read_line_async(
                    GLib.PRIORITY_DEFAULT, self.session.cancellable, on_callback, None
                )

        message = Soup.Message.new("GET", self.session.api_url + "/events")
        self.session.send_async(
            message, GLib.PRIORITY_DEFAULT, self.session.cancellable, on_response, message
        )


