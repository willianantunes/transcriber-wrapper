import shlex
import subprocess

from typing import List


def check_output(commands: List[str], encoding: str = "utf8") -> str:
    flatten_command = shlex.join(commands)
    output_as_bytes = subprocess.check_output(flatten_command, shell=True)
    return output_as_bytes.decode(encoding)
