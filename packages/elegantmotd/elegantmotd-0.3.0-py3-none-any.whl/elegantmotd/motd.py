import os
import platform
import re
import time
from datetime import datetime, timezone

import rich_click as click
from art import text2art
from rich.console import Console
from rich.live import Live
from rich.padding import Padding
from rich.style import Style
from rich.table import Table

from .cpu import CPU
from .disk import Disk
from .load import Load
from .loggedinusers import LoggedInUsers
from .memory import Memory
from .network import Network
from .process import Process
from .temperature import Temperature


def get_distro_info():
    try:
        with open("/etc/lsb-release") as f:
            content = f.read()
        release_info = dict(re.findall(r'(\w+)=(.*)', content))
        distro = f"{release_info['DISTRIB_ID']} {release_info['DISTRIB_RELEASE']}"
        codename = release_info['DISTRIB_CODENAME']
    except FileNotFoundError:
        distro = "Unknown"
        codename = "unknown"

    return distro, codename


def get_kernel_info():
    return platform.release()


def get_architecture():
    return platform.machine()


@click.command(help="Display system information in a visually appealing manner.")
@click.option("-w", "--watch", is_flag=True, show_default=False, default=False,
              help="Enable live updates of the system information.")
def display(watch: bool) -> None:
    console = Console()
    try:
        distro, codename = get_distro_info()
        kernel = get_kernel_info()
        architecture = get_architecture()

        if watch:
            console.clear()
        console.print(f"💻 [blue bold]{distro} {codename} LTS (GNU/Linux {kernel} {architecture}) [/]💻")
        console.print(f"[orange1 bold]{text2art(os.getlogin(), font='small')}[/]", end="")
        padding = Padding(generate_table(), (0, 0, 1, 0))
        if watch:
            with Live(padding, refresh_per_second=1) as live:
                while True:
                    time.sleep(1)
                    padding.renderable = generate_table()
                    live.update(padding)
        else:
            console.print(padding)
    except KeyboardInterrupt:
        console.clear()


def generate_table() -> Table:
    local_time = datetime.now(timezone.utc).astimezone()
    utc_offset = round(local_time.utcoffset().total_seconds() / 3600)
    table = Table(
        show_header=False,
        box=None,
        title_justify="left",
        title=f"  System information as of {local_time.strftime('%a. %d %B %Y %H:%M:%S')} UTC+{utc_offset}\n",
        title_style=Style(color="white", italic=False, bold=True, ),
        expand=True,
        leading=1,
        padding=(0, 2)
    )
    table.add_column("Info", style="bold CYAN")
    table.add_column("Value", style="bold WHITE")
    sysinfos = [Load(), Disk(), Memory(), Temperature(), Process(), LoggedInUsers(), Network(), CPU()]
    [table.add_row(f"{info}:", sysinfo.infos[info]) for sysinfo in sysinfos for info in sysinfo.infos]
    return table
