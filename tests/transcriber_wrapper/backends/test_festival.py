import pytest

from transcriber_wrapper.backends.exceps import BinaryNotFoundException
from transcriber_wrapper.backends.exceps import VersionNotFoundException
from transcriber_wrapper.backends.festival import Festival


def test_should_return_binary_path():
    espeak_path = Festival.discover_binary_location()

    assert espeak_path == "/usr/bin/festival"


def test_should_raise_exception_given_no_binary_was_found(mocker):
    mocked_spawn = mocker.patch("transcriber_wrapper.backends.festival.distutils.spawn")
    mocked_find_executable = mocked_spawn.find_executable
    mocked_find_executable.return_value = None

    with pytest.raises(BinaryNotFoundException):
        Festival.discover_binary_location()

    mocked_find_executable.assert_called_once_with("festival")


def test_should_return_long_version():
    espeak_path = Festival.version()

    assert espeak_path == "2.5.0"


def test_should_raise_exception_given_no_version_was_found(mocker):
    mocked_re = mocker.patch("transcriber_wrapper.backends.festival.re")
    mocked_match = mocked_re.match
    mocked_match.return_value = None

    with pytest.raises(VersionNotFoundException):
        Festival.version()

    regex = r".* ([0-9\.]+[0-9]):"
    target = "Festival Speech Synthesis System: 2.5.0:release December 2017"
    mocked_match.assert_called_once_with(regex, target)


# '/usr/bin/festival -b /tmp/tmpnw3b0qok'
