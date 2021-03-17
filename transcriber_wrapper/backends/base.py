import logging
import subprocess

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from subprocess import TimeoutExpired
from typing import Dict
from typing import List

from transcriber_wrapper import logger_name
from transcriber_wrapper.backends.exceps import LanguageNotSupportedException
from transcriber_wrapper.exceps import TranscriptionTimeoutException
from transcriber_wrapper.restorer import Restorer

logger = logging.getLogger(logger_name)


@dataclass(frozen=True)
class CommandDetails:
    commands: List[str]
    env_variables: Dict[str, str]


class Transcriber(ABC):
    def __init__(self, language: str, punctuation_marks: str):
        if not self.is_language_supported(language):
            raise LanguageNotSupportedException
        self.language = language
        self.restorer = Restorer(punctuation_marks)
        self.binary_location = self.discover_binary_location()

    def transcribe(
        self,
        words: List[str],
        with_stress: bool = False,
        preserve_punctuation: bool = False,
        phoneme_separator: str = "",
        syllable_separator: str = "",
    ) -> List[str]:
        logger.debug(f"Number of words to be transcribed: {len(words)}")
        transcriptions = [
            self._retrieve_transcription(word, with_stress, phoneme_separator, syllable_separator) for word in words
        ]

        logger.debug("Maybe the target back-end has some issues, applying a gambiarra if available...")
        transcriptions = self.apply_gambiarra(
            transcriptions,
            with_stress=with_stress,
            preserve_punctuation=preserve_punctuation,
            phoneme_separator=phoneme_separator,
        )

        if not preserve_punctuation:
            logger.debug("Not preserving punctuations")
            return transcriptions

        logger.debug("Preserving punctuations")
        transcriptions_with_punctuations = self.restorer.apply_punctuations(words, transcriptions)

        return transcriptions_with_punctuations

    @abstractmethod
    def build_command(self, word: str, **kwargs) -> CommandDetails:
        pass

    @staticmethod
    @abstractmethod
    def apply_gambiarra(transcriptions: List[str], **kwargs) -> List[str]:
        pass

    @staticmethod
    @abstractmethod
    def discover_binary_location() -> str:
        pass

    @classmethod
    @abstractmethod
    def version(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def is_language_supported(cls, language_tag: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def extract_transcription_from_computed_command(cls, output, **kwargs) -> str:
        pass

    def _retrieve_transcription(
        self, text: str, with_stress: bool, phoneme_separator: str, syllable_separator: str
    ) -> str:
        extra_options = {"phoneme_separator": phoneme_separator, "syllable_separator": syllable_separator}
        command_details = self.build_command(text, **extra_options)
        process = subprocess.Popen(command_details.commands, stdout=subprocess.PIPE, env=command_details.env_variables)

        try:
            outs, errs = process.communicate(timeout=15)
        except TimeoutExpired:
            process.kill()
            process.communicate()
            raise TranscriptionTimeoutException

        transcription = self.extract_transcription_from_computed_command(outs, **extra_options)
        cleaned_transcription = self._clear_transcription(transcription, with_stress)

        return cleaned_transcription

    def _clear_transcription(self, transcription: str, with_stress: bool) -> str:
        transcription = transcription.strip(" \t\r\n")

        if not with_stress:
            transcription = transcription.replace("ˈ", "")
            transcription = transcription.replace("ˌ", "")
            transcription = transcription.replace("'", "")
            transcription = transcription.replace("-", "")

        return transcription
