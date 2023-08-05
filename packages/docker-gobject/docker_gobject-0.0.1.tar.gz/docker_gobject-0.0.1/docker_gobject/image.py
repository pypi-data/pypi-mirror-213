import gi, json, datetime
gi.require_version("Gtk", "4.0")
gi.require_version('GLib', '2.0')
from gi.repository import GObject, Gtk, GLib, Gio
from docker_gobject.container import Config

class Image(GObject.Object):
    __gtype_name__ = "Image"

    id: GObject.Property = GObject.Property(type=str)
    parent_id: GObject.Property = GObject.Property(type=str)
    repo_tags: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    repo_digests: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    parent: GObject.Property = GObject.Property(type=str)
    comment: GObject.Property = GObject.Property(type=str)
    container: GObject.Property = GObject.Property(type=str)
    container_config: GObject.Property = GObject.Property(type=Config)
    docker_version: GObject.Property = GObject.Property(type=str)
    author: GObject.Property = GObject.Property(type=str)
    config: GObject.Property = GObject.Property(type=Config)
    variant: GObject.Property = GObject.Property(type=str)
    os: GObject.Property = GObject.Property(type=str)
    os_version: GObject.Property = GObject.Property(type=str)
    docker_version: GObject.Property = GObject.Property(type=str)
    created: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    size: GObject.Property = GObject.Property(type=int)
    graph_driver: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    rootfs: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    metadata: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)

    shared_size: GObject.Property = GObject.Property(type=int)
    virtual_size: GObject.Property = GObject.Property(type=int)
    labels: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    containers = GObject.Property = GObject.Property(type=int)

    api_properties = {
            "id": "Id",
            "parent_id": "ParentId",
            "repo_tags": "RepoTags",
            "repo_digests": "RepoDigests",
            "parent": "Parent",
            "comment": "Comment",
            "container": "Container",
            "container_config":"ContainerConfig",
            "docker_version": "DockerVersion",
            "author": "Author",
            "config":  "Config",
            "variant":  "Variant",
            "os":  "Os",
            "os_version": "OsVersion",
            "created": "Created",
            "size": "Size",
            "shared_size":  "SharedSize",
            "virtual_size": "VirtualSize",
            "labels": "Labels",
            "containers":  "Containers",
            "graph_driver":  "GraphDriver",
            "rootfs":  "RootFS",
            "metadata":"Metadata",
        }

    def __init__(
                    self,
                    id, parent_id, repo_tags,
                    repo_digests, parent, comment,
                    container, container_config,
                    docker_version, author, config, variant,
                    os, os_version, created,
                    size, shared_size, virtual_size, labels,
                    containers, graph_driver, rootfs, metadata
    ):
        GObject.Object.__init__(self)
        self.properties = {
            "id": [id, "Id"],
            "parent_id": [parent_id, "ParentId"],
            "repo_tags": [repo_tags, "RepoTags"],
            "repo_digests": [repo_digests, "RepoDigests"],
            "parent": [parent, "Parent"],
            "comment": [comment, "Comment"],
            "container": [container, "Container"],
            "container_config": [container_config, "ContainerConfig"],
            "docker_version": [docker_version, "DockerVersion"],
            "author": [author, "Author"],
            "config": [config, "Config"],
            "variant": [variant, "Variant"],
            "os": [os, "Os"],
            "os_version": [os_version, "OsVersion"],
            "created": [created, "Created"],
            "size": [size, "Size"],
            "shared_size": [shared_size, "SharedSize"],
            "virtual_size": [virtual_size, "VirtualSize"],
            "labels": [labels, "Labels"],
            "containers": [containers, "Containers"],
            "graph_driver": [graph_driver, "GraphDriver"],
            "rootfs": [rootfs, "RootFS"],
            "metadata": [metadata, "Metadata"],
        }
        for name, value in self.properties.items():
            self.set_property(name, value[0])

    @staticmethod
    def update_properties(data):
        p = {}
        for name, value in Image.api_properties.items():
            print(name)
            print((name == "size" and data.get("Size") == None))
            if name == "container_config" or name == "config":
                config = Config.from_json(data.get(value))
                p.update({name: config})
            elif (name == "size" and data.get("Size") == None) or (name == "shared_size" and data.get("SharedSize") == None) or (name == "containers" and data.get("Containers") == None):
                p.update({name: 0})
            else:
                p.update({name: data.get(value)})
        return p

    def add_inspect_data(self,data):
        p_dict = Image.update_properties(data)
        for name, value in Image.api_properties.items():
            self.set_property(name, p_dict.get(name))

    @staticmethod
    def from_json(data):
        p_dict = Image.update_properties(data)
        return Image(**p_dict)
