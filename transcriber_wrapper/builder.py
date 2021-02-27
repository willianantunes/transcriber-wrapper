from transcriber_wrapper.backends.base import Transcriber
from transcriber_wrapper.backends.espeak_ng import EspeakNGBackend
from transcriber_wrapper.exceps import UnsupportedBackendException
from transcriber_wrapper.restorer import Restorer


def build_transcriber(
    language: str = "en-us",
    backend: str = "espeak",
    preserve_punctuation: bool = False,
    punctuation_marks: str = Restorer.default_punctuation_marks,
    with_stress: bool = False,
) -> Transcriber:
    if backend == "espeak":
        return EspeakNGBackend(language, punctuation_marks, preserve_punctuation, with_stress)
    else:
        raise UnsupportedBackendException
