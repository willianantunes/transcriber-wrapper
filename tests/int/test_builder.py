import pytest

from transcriber_wrapper.builder import build_transcriber
from transcriber_wrapper.exceps import UnsupportedBackendException


def test_should_raise_exception_given_backend_not_supported():
    with pytest.raises(UnsupportedBackendException):
        build_transcriber(backend="jafar")


def test_transcribe_without_preserve_punctuation_and_stress_scenario_1():
    text_to_be_transcribed = ["Hello", "world!"]

    transcriber = build_transcriber()
    transcription = transcriber.transcribe(text_to_be_transcribed, preserve_punctuation=False, with_stress=False)

    assert " ".join(transcription) == "həloʊ wɜːld"


def test_transcribe_with_preserve_punctuation_and_stress_scenario_1():
    text_to_be_transcribed = ["Hello,", "world!"]

    transcriber = build_transcriber()
    transcription = transcriber.transcribe(text_to_be_transcribed, preserve_punctuation=True, with_stress=True)

    assert " ".join(transcription) == "həlˈoʊ, wˈɜːld!"


def test_transcribe_with_preserve_punctuation_and_without_stress_scenario_1():
    text_to_be_transcribed = ["Hello,", "world!"]

    transcriber = build_transcriber()
    transcription = transcriber.transcribe(text_to_be_transcribed, preserve_punctuation=True, with_stress=False)

    assert " ".join(transcription) == "həloʊ, wɜːld!"
