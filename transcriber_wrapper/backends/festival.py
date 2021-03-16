import distutils.spawn
import logging
import re
import shlex
import subprocess

from pathlib import Path
from typing import List

from transcriber_wrapper import logger_name
from transcriber_wrapper.backends.base import Transcriber
from transcriber_wrapper.backends.exceps import BinaryNotFoundException
from transcriber_wrapper.backends.exceps import ScriptFileNotFound
from transcriber_wrapper.backends.exceps import VersionNotFoundException

logger = logging.getLogger(logger_name)


class Festival(Transcriber):
    def __init__(self, language: str, punctuation_marks: str):
        super().__init__(language, punctuation_marks)
        base_directory = Path(__file__).resolve().parent.parent.parent
        self.script_file = f"{base_directory}/scripts/festival.lisp"
        if not Path(self.script_file).exists():
            raise ScriptFileNotFound

    @staticmethod
    def discover_binary_location() -> str:
        festival = distutils.spawn.find_executable("festival")
        if not festival:
            raise BinaryNotFoundException
        return festival

    @classmethod
    def version(cls) -> str:
        espeak_path = cls.discover_binary_location()
        command_list = [espeak_path, "--help"]
        command = shlex.join(command_list)

        output_as_bytes = subprocess.check_output(command, shell=True)
        output_as_str = output_as_bytes.decode("utf8")
        where_the_version_is_located = output_as_str.split("\n")[3]
        logger.debug(f"Full details: {where_the_version_is_located}")

        regex_to_capture_version = r".* ([0-9\.]+[0-9]):"
        matched_object = re.match(regex_to_capture_version, where_the_version_is_located)

        if not matched_object:
            raise VersionNotFoundException

        version = matched_object.group(1)
        logger.debug(f"Version: {version}")

        return version

    @staticmethod
    def apply_gambiarra(transcriptions: List[str], **kwargs) -> List[str]:
        logger.debug("No gambiarra implemented for FESTIVAL backend")
        return transcriptions

    def build_command(self, text, **kwargs) -> List[str]:
        # My strategy to extract the output from festival is like the following:
        # WORD=something festival -b /app/scripts/festival.lisp
        # WORD=house festival -b /app/scripts/festival.lisp
        command_as_list = []
        # The word to be transcribed
        command_as_list.append(f'WORD="{text}"')
        # Binary location
        command_as_list.append(self.binary_location)
        # Script file that will act as the bridge to communicate with festival
        command_as_list.append(self.script_file)

        logger.debug(f"Command built: {command_as_list}")

        return command_as_list
