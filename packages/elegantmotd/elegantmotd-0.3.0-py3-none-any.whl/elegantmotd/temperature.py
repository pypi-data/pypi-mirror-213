from typing import Dict, Union

import psutil
from rich.console import RenderableType
from rich.text import Text

from .constants import GREEN, YELLOW, ORANGE, RED
from .sysinfo import SysInfo


class Temperature(SysInfo):
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        infos = {"Temperature": ""}
        temp_info = psutil.sensors_temperatures()
        if "coretemp" in temp_info:
            shwtemps = temp_info["coretemp"]
            for shwtemp in shwtemps:
                if "Package" in shwtemp.label:
                    infos["Temperature"] = self.__get_format_temp(shwtemp)
                elif "Core" in shwtemp.label:
                    infos[f"  - {shwtemp.label}"] = self.__get_format_temp(shwtemp)
        else:
            infos["Temperature"] = "Unable to get CPU temperature"
        return infos

    @staticmethod
    def __get_format_temp(shwtemp) -> Union[str, Text]:
        high = shwtemp.high
        current = shwtemp.current
        if not current:
            return "No data"
        if not high:
            return f"{current}°C"
        if current < high - 40:
            return Text(f"{current}°C", style=GREEN)
        if current < high - 20:
            return Text(f"{current}°C", style=YELLOW)
        if current < high:
            return Text(f"{current}°C", style=ORANGE)
        else:
            return Text(f"{current}°C", style=RED)
