from unittest.mock import call

import pytest

from transcriber_wrapper.backends.espeak_ng import EspeakNGBackend
from transcriber_wrapper.backends.exceps import BinaryNotFoundException
from transcriber_wrapper.backends.exceps import VersionNotFoundException


def test_should_return_binary_path():
    espeak_path = EspeakNGBackend.discover_binary_location()

    assert espeak_path == "/usr/bin/espeak-ng"


def test_should_raise_exception_given_no_binary_was_found(mocker):
    mocked_spawn = mocker.patch("transcriber_wrapper.backends.espeak_ng.distutils.spawn")
    mocked_find_executable = mocked_spawn.find_executable
    mocked_find_executable.return_value = None

    with pytest.raises(BinaryNotFoundException):
        EspeakNGBackend.discover_binary_location()

    calls = [call("espeak-ng"), call("espeak")]
    mocked_find_executable.assert_has_calls(calls)
    assert mocked_find_executable.call_count == 2


def test_should_return_long_version():
    espeak_path = EspeakNGBackend.version()

    assert espeak_path == "1.49.2"


def test_should_raise_exception_given_no_version_was_found(mocker):
    mocked_re = mocker.patch("transcriber_wrapper.backends.espeak_ng.re")
    mocked_match = mocked_re.match
    mocked_match.return_value = None

    with pytest.raises(VersionNotFoundException):
        EspeakNGBackend.version()

    regex = r".*: ([0-9]+(\.[0-9]+)+(\-dev)?)"
    target = "eSpeak NG text-to-speech: 1.49.2  Data at: /usr/lib/x86_64-linux-gnu/espeak-ng-data"
    mocked_match.called_once_with(regex, target)


def test_should_build_command_properly_for_en_us():
    transcriber = EspeakNGBackend("en-us", ",!")

    built_command = transcriber.build_command("jafar")

    assert built_command == ["/usr/bin/espeak-ng", "jafar", f"-v{transcriber.language}", "-x", "--ipa", "-q"]


def test_should_build_command_properly_for_en_gb():
    transcriber = EspeakNGBackend("en-gb", ",!")

    built_command = transcriber.build_command("jafar")

    assert built_command == ["/usr/bin/espeak-ng", "jafar", f"-v{transcriber.language}", "-x", "--ipa", "-q"]


def test_should_build_command_properly_with_separator():
    transcriber = EspeakNGBackend("pt-br", ",!")

    text = "gambiarra"
    phoneme_separator = " "
    built_command = transcriber.build_command(text, phoneme_separator=phoneme_separator)

    assert built_command == [
        "/usr/bin/espeak-ng",
        "gambiarra",
        f"-v{transcriber.language}",
        "-x",
        "--ipa",
        "-q",
        f"--sep={phoneme_separator}",
    ]
