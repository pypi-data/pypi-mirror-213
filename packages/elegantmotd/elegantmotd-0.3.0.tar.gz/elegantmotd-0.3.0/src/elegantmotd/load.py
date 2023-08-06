import os
from typing import Dict

from rich.console import RenderableType

from .sysinfo import SysInfo


class Load(SysInfo):
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        infos = {
            "System load": str(os.getloadavg()[0])
        }
        return infos
