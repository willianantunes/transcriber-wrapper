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

    def transcribe(self, words: List[str], with_stress: bool = False, preserve_punctuation: bool = False) -> List[str]:
        logger.debug(f"Number of words to be transcribed: {len(words)}")
        transcriptions = [self._retrieve_transcription(word, with_stress) for word in words]

        if not preserve_punctuation:
            logger.debug("Not preserving punctuations")
            return transcriptions

        logger.debug("Preserving punctuations")
        transcriptions_with_punctuations = self.restorer.apply_punctuations(words, transcriptions)

        return transcriptions_with_punctuations

    @abstractmethod
    def build_command(self, word):
        pass

    @staticmethod
    @abstractmethod
    def discover_binary_location():
        pass

    @classmethod
    @abstractmethod
    def version(cls):
        pass

    def _retrieve_transcription(self, text: str, with_stress: bool):
        command_as_list = self.build_command(text)
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
