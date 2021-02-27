import pytest

from transcriber_wrapper.restorer import Restorer


@pytest.fixture
def standard_restorer():
    return Restorer()


def test_should_apply_punctuations_scenario_1(standard_restorer: Restorer):
    words_with_punctuations = ["Hello,", "world!"]
    words_that_should_receive_punctuations = ["həlˈoʊ", "wˈɜːld"]

    words = standard_restorer.apply_punctuations(words_with_punctuations, words_that_should_receive_punctuations)

    assert words == ["həlˈoʊ,", "wˈɜːld!"]
