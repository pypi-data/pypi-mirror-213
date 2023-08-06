import subprocess
from typing import Dict

from rich.console import RenderableType

from .sysinfo import SysInfo


class LoggedInUsers(SysInfo):
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        nb = len(subprocess.run(["who"], capture_output=True).stdout.split(b"\n")) - 1

        infos = {"Users logged in": str(nb)}
        return infos
