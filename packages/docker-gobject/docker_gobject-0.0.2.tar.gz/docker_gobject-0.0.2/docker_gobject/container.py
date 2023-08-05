import gi, json, datetime
gi.require_version("Gtk", "4.0")
gi.require_version('GLib', '2.0')
from gi.repository import GObject, Gtk, GLib, Gio

# Unfortunately it looks like GEnums are broke in the PyGObject bindings
# See: https://gitlab.gnome.org/GNOME/pygobject/-/issues/215

class Mount(GObject.Object):
    __gtype_name__ = "Mount"

    type_: GObject.Property = GObject.Property(type=str)
    """Type of mount - bind, volume, tmfs"""
    source: GObject.Property = GObject.Property(type=str)
    """Path or file directory on the Docker daemon host"""
    mode: GObject.Property = GObject.Property(type=str)
    """ Readonly, etc options """
    rw = GObject.Property(type=bool, default=False)
    """ Whether or not the Mount supports readwrite functions"""
    propagation: GObject.Property = GObject.Property(type=str)
    """ Bind propagation refers to whether or not mounts created within a given bind-mount can be propagated to replicas of that mount."""

    def __init__(self, type, source, mode, rw, propagation, **kwargs):
        super().__init__(**kwargs)
        self.set_property("type_", type)
        self.set_property("source", source)
        self.set_property("mode", mode)
        self.set_property("rw", rw)
        self.set_property("propagation", propagation)

    @staticmethod
    def from_json(data) -> 'Mount':
        return Mount(data["Type"], data["Source"], data["Mode"], data["RW"], data["Propagation"])

class Network(GObject.Object):
    __gtype_name__ = "Network"

    name: GObject.Property = GObject.Property(type=str)
    """ name of the network """
    ipam_config: GObject.Property = GObject.Property(type=str)
    """ IPAM Config """
    links: GObject.Property = GObject.Property(type=Gtk.ListStore)
    """ Network links """
    aliases: GObject.Property = GObject.Property(type=Gtk.ListStore)
    """ Network aliases """
    network_id: GObject.Property = GObject.Property(type=str)
    """ Network ID """
    endpoint_id: GObject.Property = GObject.Property(type=str)
    """ Endpoint ID """
    gateway: GObject.Property = GObject.Property(type=str)
    """ Gateway """
    ip_address: GObject.Property = GObject.Property(type=str)
    """ IP Address """
    ip_prefix_len: GObject.Property = GObject.Property(type=int)
    """ IP prefix length """
    ipv6_gateway: GObject.Property = GObject.Property(type=str)
    """ IPv6 gateway """
    global_ipv6_address: GObject.Property = GObject.Property(type=str)
    """ Global IPv6 address """
    global_ipv6_prefix_len: GObject.Property = GObject.Property(type=int)
    """ Global IPv6 address length"""
    mac_address: GObject.Property = GObject.Property(type=str)
    """ Mac address """
    driver_opts: GObject.Property = GObject.Property(type=str)
    """ Driver Opts """

    def __init__(self, name: str, ipam_config, links, aliases, network_id, endpoint_id, gateway, ip_address, ip_prefix_len, ipv6_gateway, global_ipv6_address, global_ipv6_prefix_len, mac_address, driver_opts, **kwargs):
        super().__init__(**kwargs)
        properties = {
            "name": name,
            "ipam_config": ipam_config,
            "links": links,
            "aliases": aliases,
            "network_id": network_id,
            "endpoint_id": endpoint_id,
            "gateway": gateway,
            "ip_address": ip_address,
            "ip_prefix_len": ip_prefix_len,
            "ipv6_gateway": ipv6_gateway,
            "global_ipv6_address": global_ipv6_address,
            "global_ipv6_prefix_len": global_ipv6_prefix_len,
            "mac_address": mac_address,
            "driver_opts": driver_opts
        }
        for name, value in properties.items():
            self.set_property(name, value)
    @staticmethod
    def from_json(name, data) -> 'Network':
        links = Gtk.ListStore.new((str,))
        aliases = Gtk.ListStore.new((str,))

        # TODO: iterate through links and aliases and add them to their respective list stores
        return Network(
            name=name,
            ipam_config=data.get("IPAMConfig"),
            links=links,
            aliases=aliases,
            network_id=data.get("NetworkID"),
            endpoint_id=data.get("EndpointID"),
            gateway=data.get("Gateway"),
            ip_address=data.get("IPAddress"),
            ip_prefix_len=data.get("IPPrefixLen"),
            ipv6_gateway=data.get("IPv6Gateway"),
            global_ipv6_address=data.get("GlobalIPv6Address"),
            global_ipv6_prefix_len=data.get("GlobalIPv6PrefixLen"),
            mac_address=data.get("MacAddress"),
            driver_opts=data.get("DriverOpts")
        )

class NetworkSettings(GObject.Object):
    __gtype_name__ = "NetworkSettings"

    networks: GObject.Property = GObject.Property(type=Gtk.ListStore)
    """ Configured networks """

    def __init__(self, networks, **kwargs):
        super().__init__(**kwargs)
        self.set_property("networks", networks)


class Log(GObject.Object):
    __gtype_name__ = "Log"

    start: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    """ Readonly, etc options """
    end: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    """ Readonly, etc options """
    exit_code: GObject.Property = GObject.Property(type=int)
    """ Readonly, etc options """
    output: GObject.Property = GObject.Property(type=str)

    def __init__(self, start, end, exit_code, output, **kwargs):
        super().__init__(**kwargs)
        self.set_property("start", start)
        self.set_property("end", end)
        self.set_property("exit_code", exit_code)
        self.set_property("output", output)

    @staticmethod
    def from_json(data):
        return Log(datetime.datetime.fromisoformat(data["Start"]),datetime.datetime.fromisoformat(data["End"]), data["exit_code"], data["Output"])
class Health(GObject.Object):
    __gtype_name__ = "Health"

    status: GObject.Property = GObject.Property(type=str)
    failing_streak: GObject.Property = GObject.Property(type=int)
    log: GObject.Property = GObject.Property(type=Gtk.ListStore)

    def __init__(self, status, failing_streak, log, **kwargs):
        super().__init__(**kwargs)
        self.set_property("status", status)
        self.set_property("failing_streak", failing_streak)
        self.set_property("log", log)


    @staticmethod
    def from_json(data):
        if data is not None:
            logs = Gtk.ListStore.new((Log,))
            for log in data["Logs"]:
                logs.append([log])

            return Health(data.get("Status"), data.get("FailingStreak"), logs)
        return None

class State(GObject.Object):
    __gtype_name__ = "State"

    state: GObject.Property = GObject.Property(type=str)
    """ State """
    error: GObject.Property = GObject.Property(type=str)
    """ Error """
    exit_code: GObject.Property = GObject.Property(type=int)
    """ Exit code """
    finished_at: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    """ Finished at time """
    health: GObject.Property = GObject.Property(type=Health)
    """ Health """
    oom_killed: GObject.Property = GObject.Property(type=bool, default=False)
    """ OOM Killed? """
    dead: GObject.Property = GObject.Property(type=bool, default=False)
    """ Dead status """
    paused: GObject.Property = GObject.Property(type=bool, default=False)
    """ Paused? """
    pid: GObject.Property = GObject.Property(type=int)
    """ PID """
    restarting: GObject.Property = GObject.Property(type=bool, default=False)
    """ Restarting? """
    running: GObject.Property = GObject.Property(type=bool, default=False)
    """ Running? """
    started_at: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    """ Started at """
    status: GObject.Property = GObject.Property(type=str)
    """ Status """
    def __init__(self, state, error = None, exit_code = 0, finished_at = None, health = None, oom_killed = None, dead = None, paused = None, pid = 0, restarting = None, running = None, started_at = None, status = None, **kwargs):
        super().__init__(**kwargs)
        properties = {
            "state": state,
            "error": error,
            "exit_code": exit_code,
            "finished_at": finished_at,
            "health": health,
            "oom_killed": oom_killed,
            "dead": dead,
            "paused": paused,
            "pid": pid,
            "restarting": restarting,
            "running": running,
            "started_at": started_at,
            "status": status
        }
        for name, value in properties.items():
            self.set_property(name, value)

    @staticmethod
    def from_json(data):
        if type(data) is str:
            return State(data)
        return State(data.get("Status"), data.get("Error"),
                data.get("ExitCode"),
                datetime.datetime.fromisoformat(data.get("FinishedAt")),
                Health.from_json(data.get("Health")),
                data.get("OOMKilled"),
                data.get("Dead"),
                data.get("Paused"),
                data.get("Pid"),
                data.get("Restarting"),
                data.get("Running"),
                datetime.datetime.fromisoformat(data.get("StartedAt")),
        data.get("Status"))

class Config(GObject.Object):
    __gtype_name__ = "Config"

    attach_stderr: GObject.Property = GObject.Property(type=bool, default=False)
    "Attach stderr (bool)"
    attach_stdin: GObject.Property = GObject.Property(type=bool, default=False)
    "Attach stdin (bool)"
    attach_stdout: GObject.Property = GObject.Property(type=bool, default=False)
    "Attach stdout"
    cmd: GObject.Property = GObject.Property(type=Gtk.ListStore)
    "cmd"
    domain_name: GObject.Property = GObject.Property(type=str)
    "Domain name"
    env = GObject.Property(type=Gtk.ListStore)
    "Env"
    health_check: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    "Health check"
    host_name: GObject.Property = GObject.Property(type=str)
    "Host name"
    image: GObject.Property = GObject.Property(type=str)
    "Image"
    labels: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    "Labels"
    mac_address: GObject.Property = GObject.Property(type=str)
    "Mac address"
    network_disabled: GObject.Property = GObject.Property(type=bool, default=False)
    "Network disabled"
    open_stdin: GObject.Property = GObject.Property(type=bool, default=False)
    "Open stdin?"
    stdin_once: GObject.Property = GObject.Property(type=bool, default=False)
    "Stdin once?"
    tty: GObject.Property = GObject.Property(type=bool, default=False)
    "Tty?"
    user: GObject.Property = GObject.Property(type=str)
    "User"
    volumes: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    "Volumes"
    working_dir: GObject.Property = GObject.Property(type=str)
    "Working dir"
    stop_signal: GObject.Property = GObject.Property(type=str)
    "Stop signal"
    stop_timeout: GObject.Property = GObject.Property(type=int)
    "Stop timeout"

    def __init__(self, attach_stderr, attach_stdin, attach_stdout, cmd, domain_name, env, health_check, exec_ids, host_name, image, labels, mac_address, network_disabled, open_stdin, stdin_once, tty, user, volumes, working_dir, stop_signal, stop_timeout, **kwargs):
        super().__init__(**kwargs)
        properties = {
            "attach_stderr": attach_stderr,
            "attach_stdin": attach_stdin,
            "attach_stdout": attach_stdout,
            "cmd": cmd,
            "domain_name": domain_name,
            "env": env,
            "health_check": health_check,
            "host_name": exec_ids,
            "image": image,
            "labels": labels,
            "mac_address": mac_address,
            "network_disabled": network_disabled,
            "open_stdin": open_stdin,
            "stdin_once": stdin_once,
            "tty": tty,
            "user": user,
            "volumes": volumes,
            "working_dir": working_dir,
            "stop_signal": stop_signal,
            "stop_timeout": stop_timeout
        }
        for name, value in properties.items():
            self.set_property(name, value)

    @staticmethod
    def from_json(data):
        env = Gtk.ListStore(str,)
        cmd = Gtk.ListStore(str,)
        print(data)

        for var in data.get("Env", []):
            env.append([var],)

        if data.get("Cmd") is not None:
            for c in data.get("Cmd"):
                cmd.append([c],)

        return Config(
                data.get("AttachStderr"),
                data.get("AttachStdin"),
                data.get("AttachStdout"),
                cmd,
                data.get("DomainName"),
                env,
                data.get("HealthCheck"),
                data.get("ExecIds"),
                data.get("HostName"),
                data.get("Image"),
                data.get("Labels"),
                data.get("MacAddress"),
                data.get("NetworkDisabled"),
                data.get("OpenStdin"),
                data.get("StdinOnce"),
                data.get("Tty"),
                data.get("User"),
                data.get("Volumes"),
                data.get("WorkingDir"),
                data.get("StopSignal"),
                data.get("StopTimeout", 0)
            )

class Container(GObject.Object):
    __gtype_name__ = "Container"

    app_armor_profile = GObject.Property(type=str)
    "App armor profile"
    args = GObject.Property(type=Gtk.ListStore)
    "Args"
    config = GObject.Property(type=Config)
    "Config"
    id: GObject.Property = GObject.Property(type=str)
    "Container ID"
    names: GObject.Property = GObject.Property(type=Gtk.ListStore)
    "Name of the container"
    image: GObject.Property = GObject.Property(type=str)
    "Name of the image the container is using"
    image_id: GObject.Property = GObject.Property(type=str)
    "ID of the image the container is using"
    command: GObject.Property = GObject.Property(type=str)
    "Start command"
    created: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    "Created date"
    driver: GObject.Property = GObject.Property(type=str)
    "Driver"
    exec_ids: GObject.Property = GObject.Property(type=Gtk.ListStore)
    "exec ids"
    hostname_path: GObject.Property = GObject.Property(type=str)
    "Hostname path"
    hosts_path: GObject.Property = GObject.Property(type=str)
    "Hosts path"
    log_path: GObject.Property = GObject.Property(type=str)
    "Log path"
    mount_label: GObject.Property = GObject.Property(type=str)
    "Mount label"
    process_label: GObject.Property = GObject.Property(type=str)
    "Process label"
    resolv_conf_path: GObject.Property = GObject.Property(type=str)
    "Resolve config path"
    restart_count: GObject.Property = GObject.Property(type=int)
    "Restart count"
    ports: GObject.Property = GObject.Property(type=Gtk.ListStore)
    "Ports the container is using"
    labels: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    "Labels assigned to the container"
    host_config: GObject.Property = GObject.Property(type=GObject.TYPE_PYOBJECT)
    "Host config assigned to the container"
    network_settings: GObject.Property = GObject.Property(type=NetworkSettings)
    "`NetworkSettings` assigned to the container"
    mounts: GObject.Property = GObject.Property(type=Gtk.ListStore)
    "Container mount points"
    state: GObject.Property = GObject.Property(type=State)
    "Current state of the container"
    status: GObject.Property = GObject.Property(type=str)
    "Status of the container"




    def __init__(self, container_id, names, image, image_id, command, created, driver, exec_ids, hostname_path, hosts_path, log_path, mount_label, process_label, resolv_conf_path, restart_count, ports, labels, state, status, host_config, network_settings, mounts, **kwargs):
        super().__init__(**kwargs)
        properties = {
            "id": container_id,
            "names": names,
            "image": image,
            "image_id": image_id,
            "command": command,
            "created": created,
            "driver": driver,
            "exec_ids": exec_ids,
            "hostname_path": hostname_path,
            "hosts_path": hosts_path,
            "log_path": log_path,
            "mount_label": mount_label,
            "process_label": process_label,
            "resolv_conf_path": resolv_conf_path,
            "restart_count": restart_count,
            "ports": ports,
            "labels": labels,
            "host_config": host_config,
            "network_settings": network_settings,
            "mounts": mounts,
            "state": state,
            "status": status
        }
        for name, value in properties.items():
            self.set_property(name, value)


    @staticmethod
    def from_json(data) -> 'Container':
        Names = Gtk.ListStore(str,)
        for name in data.get("Names", []):
            Names.append([name])
        Mounts = Gtk.ListStore(Mount,)
        for mount in data["Mounts"]:
            Mounts.append([Mount.from_json(mount)])
        Ports = Gtk.ListStore(str,)

        for port in data.get("Ports", ()):
            Ports.append([port],)
        Networks = Gtk.ListStore(Network,)
        for network in data["NetworkSettings"]["Networks"]:
            Networks.append([Network.from_json(network, data["NetworkSettings"]["Networks"][network])])

        state = State.from_json(data.get("State"))


        Network_settings = NetworkSettings(Networks)
        return Container(
            data.get("Id"),
            Names,
            data.get("Image"),
            data.get("ImageID"),
            data.get("Command"),
            data.get("Created"),
            data.get("Driver"),
            data.get("ExecIDs"),
            data.get("HostnamePath"),
            data.get("HostsPath"),
            data.get("LogPath"),
            data.get("MountLabel"),
            data.get("ProcessLabel"),
            data.get("ResolvConfPath"),
            data.get("RestartCount", 0),
            Ports,
            data.get("Labels"),
            state,
            data.get("Status"),
            data.get("HostConfig"),
            Network_settings,
            Mounts
        )



