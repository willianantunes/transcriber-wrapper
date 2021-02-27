from transcriber_wrapper.backends.base import Transcriber
from transcriber_wrapper.backends.espeak_ng import EspeakNGBackend
from transcriber_wrapper.exceps import UnsupportedBackendException
from transcriber_wrapper.restorer import Restorer


def build_transcriber(
    language: str = "en-us", backend: str = "espeak", punctuation_marks: str = Restorer.default_punctuation_marks
) -> Transcriber:
    if backend == "espeak":
        return EspeakNGBackend(language, punctuation_marks)
    else:
        raise UnsupportedBackendException
