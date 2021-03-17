from unittest.case import TestCase

import pytest

from transcriber_wrapper.backends.exceps import LanguageNotSupportedException
from transcriber_wrapper.builder import build_transcriber
from transcriber_wrapper.exceps import UnsupportedBackendException


def test_should_raise_exception_given_backend_not_supported():
    with pytest.raises(UnsupportedBackendException):
        build_transcriber(backend="jafar")


class BuilderWithEspeak(TestCase):
    def test_should_should_raise_exception_given_the_selected_language_is_not_supported(self):
        with pytest.raises(LanguageNotSupportedException):
            build_transcriber(language="elvish")

    def test_should_transcribe_without_preserve_punctuation_and_stress_scenario_1(self):
        text_to_be_transcribed = ["Hello", "world!"]

        transcriber = build_transcriber()
        transcription = transcriber.transcribe(text_to_be_transcribed, preserve_punctuation=False, with_stress=False)

        assert " ".join(transcription) == "həloʊ wɜːld"

    def test_should_transcribe_with_preserve_punctuation_and_stress_scenario_1(self):
        text_to_be_transcribed = ["Hello,", "world!"]

        transcriber = build_transcriber()
        transcription = transcriber.transcribe(text_to_be_transcribed, preserve_punctuation=True, with_stress=True)

        assert " ".join(transcription) == "həlˈoʊ, wˈɜːld!"

    def test_should_transcribe_with_preserve_punctuation_and_without_stress_scenario_1(self):
        text_to_be_transcribed = ["Hello,", "world!"]

        transcriber = build_transcriber()
        transcription = transcriber.transcribe(text_to_be_transcribed, preserve_punctuation=True, with_stress=False)

        assert " ".join(transcription) == "həloʊ, wɜːld!"

    def test_should_transcribe_with_preserve_punctuation_and_without_stress_and_separator_scenario_1(self):
        text_to_be_transcribed = ["hello,", "world!"]

        transcriber = build_transcriber()
        extra_options = {"with_stress": False, "preserve_punctuation": True, "phoneme_separator": " "}
        transcription = transcriber.transcribe(text_to_be_transcribed, **extra_options)

        assert " ".join(transcription) == "h ə l oʊ, w ɜː l d!"

        # This is a buggy example!
        # Without the gambiarra, you should receive: k j ʊɹ ɹ ɪ  ɔ s ɪ ɾ i
        text_to_be_transcribed = ["curiosity"]
        transcription = transcriber.transcribe(text_to_be_transcribed, **extra_options)

        assert " ".join(transcription) == "k j ʊɹ ɹ ɪ ɔ s ɪ ɾ i"

        text_to_be_transcribed = ["something"]
        transcription = transcriber.transcribe(text_to_be_transcribed, **extra_options)

        assert " ".join(transcription) == "s ʌ m θ ɪ ŋ"


class BuilderWithFestival(TestCase):
    def test_should_should_raise_exception_given_the_selected_language_is_not_supported(self):
        with pytest.raises(LanguageNotSupportedException):
            build_transcriber(backend="festival", language="en-gb")

    def test_should_transcribe_something(self):
        transcriber = build_transcriber(backend="festival")

        transcription = transcriber.transcribe(["something"])
        assert len(transcription) == 1 and transcription[0] == "səmθəŋ"

        transcription = transcriber.transcribe(["something"], phoneme_separator=" ")
        assert len(transcription) == 1 and transcription[0] == "s ə mθ ə ŋ"

        transcription = transcriber.transcribe(["something"], phoneme_separator=" ", syllable_separator=" • ")
        assert len(transcription) == 1 and transcription[0] == "s ə m • θ ə ŋ"

    def test_should_transcribe_solicitation(self):
        transcriber = build_transcriber(backend="festival")

        transcription = transcriber.transcribe(["solicitation"])
        assert len(transcription) == 1 and transcription[0] == "səlɪsəteɪʃən"

        transcription = transcriber.transcribe(["solicitation"], phoneme_separator=" | ")
        assert len(transcription) == 1 and transcription[0] == "s | əl | ɪs | ət | eɪʃ | ə | n"

        transcription = transcriber.transcribe(["solicitation"], phoneme_separator=" ", syllable_separator=" • ")
        assert len(transcription) == 1 and transcription[0] == "s ə • l ɪ • s ə • t eɪ • ʃ ə n"

    def test_should_transcribe_trip(self):
        transcriber = build_transcriber(backend="festival")

        transcription = transcriber.transcribe(["trip"])
        assert len(transcription) == 1 and transcription[0] == "tɹɪp"

        transcription = transcriber.transcribe(["trip"], phoneme_separator=" ", syllable_separator=" • ")
        assert len(transcription) == 1 and transcription[0] == "t ɹ ɪ p"

    def test_should_transcribe_sold(self):
        transcriber = build_transcriber(backend="festival")

        transcription = transcriber.transcribe(["sold"])
        assert len(transcription) == 1 and transcription[0] == "soʊld"

    def test_should_transcribe_with_preserve_punctuation_and_without_stress_and_separator_scenario_1(self):
        transcriber = build_transcriber(backend="festival")

        text_to_be_transcribed = ["hello,", "world!"]
        extra_options = {"with_stress": False, "preserve_punctuation": True, "phoneme_separator": " "}
        transcription = transcriber.transcribe(text_to_be_transcribed, **extra_options)

        assert " ".join(transcription) == "h əl oʊ, w ər l d!"

        text_to_be_transcribed = ["curiosity"]
        transcription = transcriber.transcribe(text_to_be_transcribed, **extra_options)

        assert len(transcription) == 1 and transcription[0] == "k j ʊɹ iɑs ət i"

        text_to_be_transcribed = ["theoretically"]
        transcription = transcriber.transcribe(text_to_be_transcribed, **extra_options)

        assert len(transcription) == 1 and transcription[0] == "θ iərɛt ək əl i"
