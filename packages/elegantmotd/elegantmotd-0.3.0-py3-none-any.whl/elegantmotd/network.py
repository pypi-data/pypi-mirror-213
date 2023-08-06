from typing import Dict

import netifaces
from rich.console import RenderableType

from .sysinfo import SysInfo


class Network(SysInfo):
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        infos = {"Network": ""}

        for intf in netifaces.interfaces():
            if intf != "lo":
                addr = netifaces.ifaddresses(intf).get(netifaces.AF_INET, [{}])[0].get("addr")
                if addr:
                    infos[f"  - {intf}"] = addr

        return infos
