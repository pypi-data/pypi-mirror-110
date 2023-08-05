#!/usr/bin/env python3

from wirepas_mqtt_library import WirepasNetworkInterface
import wirepas_mesh_messaging as wmm


def parse_bytes(bytes_):
    """Parse bytes from a bytes, bytearray or hex string object"""

    if isinstance(bytes_, bytearray) or isinstance(bytes_, bytes):
        # Create an immutable copy of bytearray or bytes object
        return bytes(bytes_)
    elif isinstance(bytes_, str):
        # Parse text format
        bytes_ = bytes_.replace(",", " ").split()  # Comma or space delim
        return bytes([int(n, 16) for n in bytes_])  # Text to bytes

    raise TypeError("invalid type for bytes_")


def format_bytes(bytes_):
    """Format bytearray or bytes as hex string"""

    return " ".join(["%02x" % n for n in bytes_])


class Role:
    """Node role object"""

    SINK = 0x01
    HEADNODE = 0x02
    SUBNODE = 0x03
    LOW_LATENCY = 0x10
    AUTOROLE = 0x80

    BASE_ROLE_MASK = 0x07
    INVALID_MASK = 0x6C

    base_role_names = ["sink", "headnode", "subnode"]
    flag_names = {
        LOW_LATENCY: ["ll", "low-latency"],
        AUTOROLE: ["ar", "autorole", "auto-role"],
    }

    def __init__(self, role):
        if isinstance(role, str):
            self.from_string(role)
        elif isinstance(role, Role):
            self.value = role.value
        elif isinstance(role, int):
            self.value = role
        else:
            raise TypeError("invalid parameter type '%s'" % type(role))

        if (self.value & self.INVALID_MASK != 0) or (
            (self.value & self.BASE_ROLE_MASK == self.SINK)
            and (self.value & self.AUTOROLE != 0)
        ):
            raise ValueError("invalid role value 0x%02x" % self.value)

    def from_string(self, role_name):
        role_name = role_name.replace("+", " ").lower()
        flag_names = role_name.split()

        try:
            base_role_name = flag_names.pop(0)
            base_role_value = self.base_role_names.index(base_role_name) + 1
        except (ValueError, IndexError):
            raise ValueError("invalid role name: '%s'" % base_role_name)

        flag_value = 0x00
        for flag_name in flag_names:
            found = False
            flag_name = flag_name
            for flag_weight in self.flag_names:
                if flag_name in self.flag_names[flag_weight]:
                    flag_value |= flag_weight
                    found = True
            if not found:
                raise ValueError("invalid role flag: %s" % flag_name)

        self.value = base_role_value | flag_value

    def __str__(self):
        base_role_name = self.base_role_names[(self.value & self.BASE_ROLE_MASK) - 1]

        flag_names = []
        for flag_weight in self.flag_names:
            if self.value & flag_weight != 0:
                flag_names.append(self.flag_names[flag_weight][0])

        flag_names.insert(0, base_role_name)
        return "+".join(flag_names)


class Qos:
    """Quality-of-Service object"""

    NORMAL = 0
    IMPORTANT = 1

    def __init__(self, qos):
        if isinstance(qos, str):
            self.from_string(qos)
        elif isinstance(qos, Qos):
            self.value = qos.value
        elif isinstance(qos, int):
            self.value = qos
        else:
            raise TypeError("invalid parameter type '%s'" % type(qos))

    def from_string(self, qos_name):
        qos_name = qos_name.lower()
        if qos_name == "normal":
            self.value = self.NORMAL
        elif qos_name in ("high", "important"):
            self.value = self.IMPORTANT
        else:
            raise ValueError("invalid qos name: '%s'" % qos_name)

    def __str__(self):
        if self.value == self.NORMAL:
            return "normal"
        elif self.value == self.IMPORTANT:
            return "important"
        else:
            # Invalid QoS value
            return ""


class Keys:
    """Authentication and Encryption Keys object"""

    # Number of bytes in an authentication or encryption key
    KEY_NUM_BYTES = 16  # 128 bits

    # Unset (empty) key with all bits set
    EMPTY_KEY = bytes([0xFF] * KEY_NUM_BYTES)

    def __init__(self, authentication_key_or_dict, encryption_key=None):
        if isinstance(authentication_key_or_dict, dict):
            self._from_dict(authentication_key_or_dict)
        else:
            if authentication_key_or_dict is None:
                # Key set but not known
                self.authentication = None
            elif authentication_key_or_dict == "":
                # Empty key, i.e. key not set
                self.authentication = self.EMPTY_KEY
            else:
                # Key set
                self.authentication = parse_bytes(authentication_key_or_dict)

            if encryption_key is None:
                # Key set but not known
                self.encryption = None
            elif encryption_key == "":
                # Empty key, i.e. key not set
                self.encryption = self.EMPTY_KEY
            else:
                # Key set
                self.encryption = parse_bytes(encryption_key)

        # Check length of keys
        if (
            self.authentication is not None
            and len(self.authentication) != self.KEY_NUM_BYTES
        ):
            raise ValueError("invalid authentication key length")

        if self.encryption is not None and len(self.encryption) != self.KEY_NUM_BYTES:
            raise ValueError("invalid encryption key length")

    def to_dict(self):
        d = {}

        if self.authentication is None:
            # Key set but not known
            pass
        elif self.authentication == self.EMPTY_KEY:
            # Empty key, i.e. key not set
            d["authentication"] = ""
        else:
            # Key set
            d["authentication"] = format_bytes(self.authentication)

        if self.encryption is None:
            # Key set but not known
            pass
        elif self.encryption == self.EMPTY_KEY:
            # Empty key, i.e. key not set
            d["encryption"] = ""
        else:
            # Key set
            d["encryption"] = format_bytes(self.encryption)

        return d

    def _from_dict(self, dict_):
        if "authentication" not in dict_:
            # Key not present, leave as is
            self.authentication = None
        elif not dict_["authentication"]:  # "", None, False, ...
            # Empty key, i.e. key not set
            self.authentication = self.EMPTY_KEY
        else:
            # Key set
            self.authentication = parse_bytes(dict_["authentication"])

        if "encryption" not in dict_:
            # Key not present, leave as is
            self.encryption = None
        elif not dict_["encryption"]:  # "", None, False, ...
            # Empty key, i.e. key not set
            self.encryption = self.EMPTY_KEY
        else:
            # Key set
            self.encryption = parse_bytes(dict_["encryption"])

    @classmethod
    def placeholder(cls, are_keys_set):
        if are_keys_set:
            # Keys are set but not known, use None as a special value
            return cls(None, None)
        else:
            # Keys are not set, use empty key
            return cls("", "")


class AppConfig:
    """App Config Data object"""

    # Maximum number of bytes in app config data
    MAX_NUM_BYTES = 80

    def __init__(self, seq_or_dict, data=None, diag_interval_s=None):
        if isinstance(seq_or_dict, dict):
            self._from_dict(seq_or_dict)
        else:
            self.seq = int(seq_or_dict)
            self.data = parse_bytes(data)
            self.diag_interval_s = int(diag_interval_s)

        if len(self.data) > self.MAX_NUM_BYTES:
            raise ValueError("app config data too long")

    def to_dict(self):
        return {
            "seq": self.seq,
            "data": format_bytes(self.data),
            "diag_interval_s": self.diag_interval_s,
        }

    def _from_dict(self, dict_):
        self.seq = int(dict_["seq"])
        self.data = parse_bytes(dict_["data"])
        self.diag_interval_s = int(dict_["diag_interval_s"])


class Sink:
    """Sink object"""

    def __init__(
        self,
        gw_id,
        sink_id,
        address_or_dict=None,
        nw_address=None,
        nw_channel=None,
        role=None,
        keys=None,
        is_started=None,
        app_config=None,
    ):
        self.gw_id = gw_id
        self.sink_id = sink_id
        if isinstance(address_or_dict, dict):
            self._from_dict(address_or_dict)
        else:
            self.address = int(address_or_dict)
            self.nw_address = int(nw_address)
            self.nw_channel = int(nw_channel)
            self.role = Role(role)
            self.keys = keys
            self.is_started = bool(is_started)
            self.app_config = app_config

    def to_dict(self):
        return {
            "gw_id": self.gw_id,
            "sink_id": self.sink_id,
            "address": self.address,
            "nw_address": self.nw_address,
            "nw_channel": self.nw_channel,
            "role": str(self.role),
            "keys": self.keys.to_dict(),
            "is_started": self.is_started,
            "app_config": self.app_config.to_dict(),
        }

    def _from_dict(self, dict_):
        self.address = int(dict_["address"])
        self.nw_address = int(dict_["nw_address"])
        self.nw_channel = int(dict_["nw_channel"])
        self.role = Role(dict_["role"])
        self.keys = Keys(dict_["keys"])
        self.is_started = bool(dict_["is_started"])
        self.app_config = AppConfig(dict_["app_config"])


class MqttConnection:
    """MQTT broker connection"""

    def __init__(self, host, port, username, password, use_tls):
        # Connect to an MQTT broker
        self.wni = WirepasNetworkInterface(
            host, port, username, password, insecure=not use_tls
        )

        # Start receiving data in a buffer
        self.rx_data = []  # TODO: check thread safety
        self.wni.register_data_cb(self.on_data_rx)

    def close(self):
        # TODO
        pass

    def get_gateways(self):
        # List gateways
        gw_ids = self.wni.get_gateways()
        gw_ids.sort()
        return gw_ids

    def get_sinks(self, gw_id):
        # List sinks under a gateway
        sinks = self.wni.get_sinks(gateway=(gw_id,))

        def convert(gw_id, sink_id, config):
            # Convert config dict to sink type
            return Sink(
                gw_id,
                sink_id,
                config["node_address"],
                config["network_address"],
                config["network_channel"],
                Role(config["node_role"]),
                Keys.placeholder(config["are_keys_set"]),
                config["started"],
                AppConfig(
                    config["app_config_seq"],
                    config["app_config_data"],
                    config["app_config_diag"],
                ),
            )

        sinks_converted = [convert(s[0], s[1], s[2]) for s in sinks]

        # Sort according to sink_id
        sinks_converted.sort(key=lambda sink: sink.sink_id)

        return sinks_converted

    def configure_sink(self, gw_id, sink_id, config):
        # TODO
        try:
            wni_config = {
                "node_address": config.address,
                "network_address": config.nw_address,
                "network_channel": config.nw_channel,
                "node_role": config.role.value,
                "started": config.is_started,
                # DEBUG
                # "app_config_seq": config.app_config.seq,
                # "app_config_data": config.app_config.data,
                # "app_config_diag": config.app_config.diag_interval_s,
            }

            if config.keys.authentication is not None:
                wni_config["authentication_key"] = config.keys.authentication

            if config.keys.encryption is not None:
                wni_config["cipher_key"] = config.keys.encryption

            print(repr(wni_config))  # DEBUG

            def on_config_set_cb(gw_error_code, param):
                print("on_config_set_cb(%s)" % repr(gw_error_code))

            res = self.wni.set_sink_config(gw_id, sink_id, wni_config, on_config_set_cb)
            if res != wmm.GatewayResultCode.GW_RES_OK:
                # TODO
                print("Cannot set new config to %s:%s res=%s" % (gw_id, sink_id, res))
        except TimeoutError:
            # TODO
            print("Cannot set new config to %s:%s" % (gw_id, sink_id))

    def get_next_rx_data(self):
        data = None
        if len(self.rx_data) > 0:
            # Pop data from buffer
            data = self.rx_data.pop(0)
        return data

    def on_data_rx(self, data):
        # Append data in buffer
        self.rx_data.append(data)

    def send_data(self, payload, dest_addr, src_ep, dest_ep, qos, init_delay_ms):
        # TODO: Send to all sinks on all gateways
        for gw_id in self.get_gateways():
            for sink in self.get_sinks(gw_id):
                self.wni.send_message(
                    sink.gw_id,
                    sink.sink_id,
                    dest_addr,
                    src_ep,
                    dest_ep,
                    bytes(payload),  # Only bytes(), no bytearray()
                    qos.value  # ,
                    # csma_ca_only, # TODO
                    # cb, # TODO
                    # param, # TODO
                )
