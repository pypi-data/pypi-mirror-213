import contextlib
import subprocess
import sys
import time
import os
from enum import Enum
from collections import namedtuple
from typing import Annotated
import typer
from rich.ansi import console
from rich.style import Style
from gitease import GitHelper

backgroundcli = typer.Typer(add_completion=False)

Process = namedtuple('Process', ['pid', 'service', 'interval', 'path'])

"""
Automations:
  auto <save|share> <interval> --<detach>: run a service
  list <save|share>: list running services
  stop <save|share>: stop a service
  
## Automation Example
```bash
$ ge auto commit 5 --detach
Running auto commit every 5.0 minutes in the background

$ ge list commit
Auto commit every 5.0 on pid 96641  in repo at /Users/yonatanalexander/development/xethub/gitease

$ ge stop commit
Stopping auto-git commit - in <repo>
Stopping processes for commit...
Stopped auto 96641..
```
"""

class ServiceEnum(str, Enum):
    SAVE = "save"
    SHARE = "share"


def run(key: str, interval: float, path: str = '.'):
    helper = GitHelper(path=path)
    while interval > 0:
        try:
            console.print(f"{key} every {interval} minute", style=Style(color="yellow"))
            if key == ServiceEnum.SAVE:
                helper.add_commit()
            elif key == ServiceEnum.SHARE:
                helper.push()
            else:
                raise ValueError(f"Invalid key: {key}")
            time.sleep(interval * 60)
        except KeyboardInterrupt:
            break


@backgroundcli.command()
def bstart(service: ServiceEnum = typer.Argument(help="Which automation to run"),
           interval: float = typer.Argument(help="The interval in minutes"),
           path: str = typer.Argument(help="The repository local path")):
    console.print(f"Starting auto-git for {service} every {interval} minutes on repo at {path}",
                  style=Style(color="yellow", blink=True, bold=True))
    run(service, interval, path)
    console.print(f"Stopped....",
                  style=Style(color="red", blink=True, bold=True))


def auto(service: ServiceEnum = typer.Argument(help="Which automation to run"),
         interval: float = typer.Argument(help="The interval in minutes"),
         detach: bool = typer.Option(False, '--detach', help="Detach and run in the background")):
    """Automatically add and commit files to git at an interval"""
    path = os.getcwd()  # TODO as an argument
    helper = GitHelper(path=path)  # validate it's a git repo
    stdout = subprocess.PIPE if detach else None
    kill([process.pid for process in _list(service)])

    if not detach:
        console.print(f"Press Ctrl+C to stop...\n", style=Style(color="red", blink=True, bold=True))
    process = subprocess.Popen(["bgitllm", service, str(interval), path], stdout=stdout)
    if detach:
        console.print(f"Running auto {service} every {interval} in the background",
                      style=Style(color="yellow", blink=True, bold=True))
        sys.exit()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        process.terminate()
        process.wait()


def _list(service: str = ''):
    command = ' | '.join(["ps aux", f"grep 'bgitllm {service}'"])
    output = subprocess.check_output(command, shell=True).decode("utf-8").strip().split('\n')
    processes = []
    for row in output:
        row = row.split(' ')
        if len(row) > 2 and 'grep' not in row:
            processes.append(Process(int(row[1]), row[-3], float(row[-2]), row[-1]))
    return processes


def list(service: Annotated[str, typer.Argument(help="Which automation to list - default all")] = ''):
    """List all running automations"""
    processes = _list(service)
    for process in processes:
        console.print(
            f"Auto {process.service} every {process.interval} minutes on pid {process.pid}  in repo at {process.path}",
            style=Style(color="yellow"))
    return processes


def kill(pids):
    for pid in pids:
        with contextlib.suppress(ProcessLookupError):
            os.kill(int(pid), 15)  # Send SIGTERM signal
            console.print(f"Stopped auto {pid}...", style=Style(color="red", blink=True, bold=True))


def stop(service: ServiceEnum = typer.Argument(help="Which service to stop")):
    """Stop automation"""
    console.print(f"Stopping auto-git {service} - in {os.getcwd()}", style=Style(color="red", blink=True, bold=True))
    processes = _list(service)
    if not processes:
        console.print("No processes found.", style=Style(color="red", blink=True, bold=True))
    else:
        kill([process.pid for process in processes])

