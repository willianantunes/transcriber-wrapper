from types import FunctionType

import transcriber_wrapper


def test_should_build_transcriber_be_defined():
    attr = getattr(transcriber_wrapper, "build_transcriber")

    assert attr
    assert type(attr) == FunctionType
