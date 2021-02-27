from transcriber_wrapper.backends.espeak_ng import EspeakNGBackend


def test_should_return_binary_path():
    espeak_path = EspeakNGBackend.discover_binary_location()

    assert espeak_path == "/usr/bin/espeak-ng"


def test_should_return_long_version():
    espeak_path = EspeakNGBackend.version()

    assert espeak_path == "1.49.2"
