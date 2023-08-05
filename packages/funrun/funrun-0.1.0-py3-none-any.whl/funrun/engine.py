"""Engine for wrapping shell."""
import subprocess
from dataclasses import dataclass
from typing import Callable, Tuple


@dataclass
class Engine:
    dry_run: bool = False

    def execute(self, command: str, depth: int = 0, info: Callable = None) -> int:
        None


@dataclass
class ShellEngine(Engine):
    def execute(self, command: str, depth: int = 0, info: Callable = None) -> Tuple[str, str]:
        if info:
            info(f"RUN: {command}")
        # indent = '    ' * depth
        # print(f'{indent}RUN: {command}')
        if self.dry_run:
            return "", ""
        else:
            proc = subprocess.run([command], capture_output=True, shell=True, check=True)
            return proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8")
