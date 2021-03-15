import logging
import subprocess

from abc import ABC
from abc import abstractmethod
from subprocess import TimeoutExpired
from typing import List

from transcriber_wrapper import logger_name
from transcriber_wrapper.exceps import TranscriptionTimeoutException
from transcriber_wrapper.restorer import Restorer

logger = logging.getLogger(logger_name)


class Transcriber(ABC):
    def __init__(self, language: str, punctuation_marks: str):
        self.language = language
        self.restorer = Restorer(punctuation_marks)
        self.binary_location = self.discover_binary_location()

    def transcribe(
        self,
        words: List[str],
        with_stress: bool = False,
        preserve_punctuation: bool = False,
        phoneme_separator: str = "",
    ) -> List[str]:
        logger.debug(f"Number of words to be transcribed: {len(words)}")
        transcriptions = [self._retrieve_transcription(word, with_stress, phoneme_separator) for word in words]

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
    def build_command(self, word: str, **kwargs) -> List[str]:
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

    def _retrieve_transcription(self, text: str, with_stress: bool, phoneme_separator: str) -> str:
        command_as_list = self.build_command(text, phoneme_separator=phoneme_separator)
        process = subprocess.Popen(command_as_list, stdout=subprocess.PIPE)

        try:
            outs, errs = process.communicate(timeout=15)
        except TimeoutExpired:
            process.kill()
            process.communicate()
            raise TranscriptionTimeoutException

        transcription = outs.decode("utf8")
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
