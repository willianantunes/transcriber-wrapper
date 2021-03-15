import inspect

from transcriber_wrapper.backends.base import Transcriber
from transcriber_wrapper.backends.espeak_ng import EspeakNGBackend


def test_must_have_four_methods_or_functions_to_be_implemented():
    methods_and_functions_to_be_implemented = []

    functions_list = inspect.getmembers(Transcriber, predicate=inspect.isfunction)

    for name, function_object in functions_list:
        if "@abstractmethod" in inspect.getsource(function_object):
            methods_and_functions_to_be_implemented.append(name)

    methods_list = inspect.getmembers(Transcriber, predicate=inspect.ismethod)
    for name, method_object in methods_list:
        if "@abstractmethod" in inspect.getsource(method_object):
            methods_and_functions_to_be_implemented.append(name)

    assert len(methods_and_functions_to_be_implemented) == 4


def test_should_clean_transcription_without_stress():
    transcriber = EspeakNGBackend("en-us", ",!")

    fake_transcription = " jˈaˌf'a-r\t\r\n"
    cleared_word = transcriber._clear_transcription(fake_transcription, with_stress=False)

    assert cleared_word == "jafar"


def test_should_clean_transcription_with_stress():
    transcriber = EspeakNGBackend("en-us", ",!")

    fake_transcription = " jˈaˌf'a-r\t\r\n"
    cleared_word = transcriber._clear_transcription(fake_transcription, with_stress=True)

    assert cleared_word == "jˈaˌf'a-r"
