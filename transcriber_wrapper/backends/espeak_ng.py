import distutils.spawn
import logging
import re

from typing import List

from transcriber_wrapper import logger_name
from transcriber_wrapper.backends.base import CommandDetails
from transcriber_wrapper.backends.base import Transcriber
from transcriber_wrapper.backends.exceps import BinaryNotFoundException
from transcriber_wrapper.backends.exceps import VersionNotFoundException
from transcriber_wrapper.support.subprocess_utils import check_output

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
        output = check_output(command_list)

        where_the_version_is_located = output.split("\n")[1]
        logger.debug(f"Full details: {where_the_version_is_located}")

        regex_to_capture_version = r".*: ([0-9]+(\.[0-9]+)+(\-dev)?)"
        matched_object = re.match(regex_to_capture_version, where_the_version_is_located)

        if not matched_object:
            raise VersionNotFoundException

        version = matched_object.group(1)
        logger.debug(f"Version: {version}")

        return version

    @classmethod
    def is_language_supported(cls, language_tag: str) -> bool:
        espeak_path = cls.discover_binary_location()
        command_list = [espeak_path, "--voices"]
        output = check_output(command_list)

        dirty_list_of_supported_languages = output.split("\n")[1:]
        cleaned_list_of_supported_languages = []
        for dirty_row in dirty_list_of_supported_languages:
            if dirty_row:
                column = dirty_row.split()
                supported_language_tag = column[1]
                cleaned_list_of_supported_languages.append(supported_language_tag)

        return language_tag in cleaned_list_of_supported_languages

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

    @classmethod
    def extract_transcription_from_computed_command(cls, output: bytes, **kwargs) -> str:
        return output.decode("utf8")

    def build_command(self, word: str, **kwargs) -> CommandDetails:
        # espeak-ng "Hello my friend, stay awhile and listen." -v en-us -x --ipa -q
        command_as_list = []
        # Binary location
        command_as_list.append(self.binary_location)
        # Text to be transcribed
        command_as_list.append(word)
        # Language
        command_as_list.append(f"-v{self.language}")
        # Write to STDOUT, IPA and quiet options
        command_as_list += ["-x", "--ipa", "-q"]
        # The character to separate phonemes, if applicable
        separator = kwargs.get("phoneme_separator")
        if separator:
            command_as_list.append(f"--sep={separator}")

        logger.debug(f"Command built: {command_as_list}")

        return CommandDetails(command_as_list, {})
