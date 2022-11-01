import json
from logging import getLogger
from pathlib import Path

from django.conf import settings

from V2RayMan.exeptions import InboundNotFoundException

logger = "vtr"


class V2RayConfig:
    def __init__(self, file_path: Path = None):
        self.file_path = file_path or settings.V2RAY_CONFIG_PATH

    @property
    def config_data(self):
        with self.file_path.open() as f_:
            return json.load(f_)

    def iter_inbounds(self):
        for c_, inb in enumerate(self.config_data["inbounds"]):
            if inb.get("tag", None):
                yield inb
            else:
                logger.warning(f"found inbound without tag (inbound {c_ + 1})")

    def get_inbound(self, tag):
        for inb in self.iter_inbounds():
            if inb["tag"] == tag:
                return inb
        raise InboundNotFoundException(tag)

    def iter_inbounds_protocol(self):
        for inb in self.iter_inbounds():
            yield {"tag": inb["tag"], "protocol": inb["protocol"]}

    def get_inbound_protocol(self, tag):
        return self.get_inbound(tag)["protocol"]
