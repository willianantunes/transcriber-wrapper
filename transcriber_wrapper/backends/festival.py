import distutils.spawn
import logging
import re

from pathlib import Path
from typing import List

from pyparsing import OneOrMore
from pyparsing import ParseResults
from pyparsing import nestedExpr

from transcriber_wrapper import logger_name
from transcriber_wrapper.backends.base import CommandDetails
from transcriber_wrapper.backends.base import Transcriber
from transcriber_wrapper.backends.exceps import BinaryNotFoundException
from transcriber_wrapper.backends.exceps import ScriptFileNotFound
from transcriber_wrapper.backends.exceps import VersionNotFoundException
from transcriber_wrapper.dealers.InternationalPhoneticAlphabet import InternationalPhoneticAlphabet
from transcriber_wrapper.support.subprocess_utils import check_output

logger = logging.getLogger(logger_name)


class FestivalBackend(Transcriber):
    supported_languages = ["en-us"]

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
        output = check_output(command_list)

        where_the_version_is_located = output.split("\n")[3]
        logger.debug(f"Full details: {where_the_version_is_located}")

        regex_to_capture_version = r".* ([0-9\.]+[0-9]):"
        matched_object = re.match(regex_to_capture_version, where_the_version_is_located)

        if not matched_object:
            raise VersionNotFoundException

        version = matched_object.group(1)
        logger.debug(f"Version: {version}")

        return version

    @classmethod
    def is_language_supported(cls, language_tag: str) -> bool:
        return language_tag in cls.supported_languages

    @staticmethod
    def apply_gambiarra(transcriptions: List[str], **kwargs) -> List[str]:
        logger.debug("No gambiarra implemented for FESTIVAL backend")
        return transcriptions

    @classmethod
    def extract_transcription_from_computed_command(cls, output, **kwargs) -> str:
        output_as_str = output.decode("utf8")
        logger.debug("Parsing the result of the LISP script")
        data: ParseResults = OneOrMore(nestedExpr()).parseString(output_as_str)
        logger.debug("Extracting some details")
        where_festival_analysis_is = data[0][0].asList()
        about_the_word = where_festival_analysis_is[0][1]
        all_syllables = where_festival_analysis_is[1::]
        logger.debug(f"Details about the word: {about_the_word}")
        logger.debug(f"All syllables: {all_syllables}")
        cleaned_syllables = cls._extract_phonemes(all_syllables)
        # From here, I am supposed to translate the US phoneset to IPA, but how do I do that?
        # This US phoneset seems different from ARPABET
        # https://en.m.wikipedia.org/wiki/ARPABET
        # http://www.festvox.org/bsv/c4711.html
        cleaned_syllables_as_ipa = [
            InternationalPhoneticAlphabet.ipa_format_from_us_phone_set(syllable) for syllable in cleaned_syllables
        ]
        logger.debug(f"Cleaned syllables as IPA: {cleaned_syllables_as_ipa}")
        phoneme_separator: str = kwargs["phoneme_separator"]
        syllable_separator: str = kwargs["syllable_separator"]
        logger.debug(f"Value for phoneme separator: {phoneme_separator}")
        logger.debug(f"Value for syllable separator: {syllable_separator}")
        joined_syllables_phonemes = []
        for syllable in cleaned_syllables_as_ipa:
            joined_syllable = phoneme_separator.join(syllable)
            joined_syllables_phonemes.append(joined_syllable)
        logger.debug(f"After phoneme separator application: {joined_syllables_phonemes}")
        joined_syllables = syllable_separator.join(joined_syllables_phonemes)
        logger.debug(f"After phoneme syllable application: {joined_syllables}")
        return joined_syllables

    def build_command(self, word: str, **kwargs) -> CommandDetails:
        # My strategy to extract the output from festival is like the following:
        # WORD=something festival -b /app/scripts/festival.lisp
        # WORD=house festival -b /app/scripts/festival.lisp
        # Binary location and script file that will act as the bridge to communicate with festival
        command_as_list = [self.binary_location, self.script_file]
        env_variables = {"WORD": word}

        logger.debug(f"Command built and env variables: {command_as_list} / {env_variables}")

        return CommandDetails(command_as_list, env_variables)

    @classmethod
    def _extract_phonemes(cls, syllables):
        logger.debug(f"Number of syllables: {len(syllables)}")

        cleaned_syllables = []
        for syllable_setup in syllables:
            where_phonemes_are = syllable_setup[1:]
            phonemes = []
            for phoneme_section in where_phonemes_are:
                dirty_phoneme: str = phoneme_section[0][0]
                cleaned_phoneme = dirty_phoneme.replace('"', "")
                phonemes.append(cleaned_phoneme)
            cleaned_syllables.append(phonemes)

        return cleaned_syllables
