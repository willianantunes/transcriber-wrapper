import distutils.spawn
import logging
import re
import shlex
import subprocess

from typing import List

from transcriber_wrapper import logger_name
from transcriber_wrapper.backends.base import Transcriber
from transcriber_wrapper.backends.exceps import BinaryNotFoundException
from transcriber_wrapper.backends.exceps import VersionNotFoundException

logger = logging.getLogger(logger_name)


class EspeakNGBackend(Transcriber):
    def __init__(self, language: str, punctuation_marks: str):
        super().__init__(language, punctuation_marks)

    @staticmethod
    def discover_binary_location() -> str:
        espeak = distutils.spawn.find_executable("espeak-ng")
        if not espeak:
            espeak = distutils.spawn.find_executable("espeak")
        if not espeak:
            raise BinaryNotFoundException
        return espeak

    @classmethod
    def version(cls) -> str:
        espeak_path = cls.discover_binary_location()
        command_list = [espeak_path, "--help"]
        command = shlex.join(command_list)

        output_as_bytes = subprocess.check_output(command, shell=True)
        output_as_str = output_as_bytes.decode("utf8")
        where_the_version_is_located = output_as_str.split("\n")[1]
        logger.debug(f"Full details: {where_the_version_is_located}")

        regex_to_capture_version = r".*: ([0-9]+(\.[0-9]+)+(\-dev)?)"
        matched_object = re.match(regex_to_capture_version, where_the_version_is_located)

        if not matched_object:
            raise VersionNotFoundException

        version = matched_object.group(1)
        logger.debug(f"Version: {version}")

        return version

    @staticmethod
    def apply_gambiarra(transcriptions: List[str], **kwargs) -> List[str]:
        separator = kwargs.get("phoneme_separator")
        if separator:
            # I don't know why, but if you try to use an empty space as the separator for the word curiosity
            # You may got two spaces, to illustrate: k j ʊɹ ɹ ɪ  ɔ s ɪ ɾ i
            # This gambiarra is to fix that
            buggy_separator = f"{separator}{separator}"
            return [transcription.replace(buggy_separator, separator) for transcription in transcriptions]
        else:
            return transcriptions

    def build_command(self, text, **kwargs) -> List[str]:
        # espeak-ng "Hello my friend, stay awhile and listen." -v en-us -x --ipa -q
        command_as_list = []
        # Binary location
        command_as_list.append(self.binary_location)
        # Text to be transcribed
        command_as_list.append(text)
        # Language
        command_as_list.append(f"-v{self.language}")
        # Write to STDOUT, IPA and quiet options
        command_as_list += ["-x", "--ipa", "-q"]
        # The character to separate phonemes, if applicable
        separator = kwargs.get("phoneme_separator")
        if separator:
            command_as_list.append(f"--sep={separator}")

        logger.debug(f"Command built: {command_as_list}")

        return command_as_list
