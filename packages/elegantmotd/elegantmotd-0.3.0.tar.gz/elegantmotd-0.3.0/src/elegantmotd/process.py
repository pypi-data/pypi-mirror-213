import os
from typing import Dict

from rich.console import RenderableType

from .sysinfo import SysInfo


class Process(SysInfo):
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        infos = {"Processes": str(len(os.listdir("/proc")))}
        return infos
