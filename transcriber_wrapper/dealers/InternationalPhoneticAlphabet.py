import re

from typing import List


class InternationalPhoneticAlphabet:
    us_phone_set_to_ipa = {
        # http://www.festvox.org/bsv/c4711.html
        # https://en.m.wikipedia.org/wiki/ARPABET
        # I think this is wrong. A help from a language specialist is welcome!
        "aa": "ɑ",
        "ae": "æ",
        "ah": "ə",
        "ao": "ɔ",
        "aw": "aʊ",
        "ax": "ə",
        "ay": "aɪ",
        "eh": "ɛ",
        "el": "l̩",
        "em": "m̩",
        "en": "n̩",
        "er": "ər",
        "ey": "eɪ",
        "ih": "ɪ",
        "iy": "i",
        "ow": "oʊ",
        "oy": "ɔɪ",
        "uh": "ʊ",
        "uw": "u",
        "b": "b",
        "ch": "ʧ",
        "d": "d",
        "dh": "ð",
        "f": "f",
        "g": "ɡ",
        "hh": "h",
        "jh": "ʤ",
        "k": "k",
        "l": "l",
        "m": "m",
        "n": "n",
        "ng": "ŋ",
        "p": "p",
        "r": "ɹ",
        "s": "s",
        "sh": "ʃ",
        "t": "t",
        "th": "θ",
        "v": "v",
        "w": "w",
        "y": "j",
        "z": "z",
        "zh": "ʒ",
        "pau": "",
    }

    regex_to_capture_ipa_stress_mark = r"([\ˈ\ˌ])"

    @classmethod
    def ipa_format_from_us_phone_set(cls, phonemes: List[str]) -> List[str]:
        phonemes_as_ipa_symbols = []

        for index, phoneme in enumerate(phonemes):
            matches = list(re.finditer(cls.regex_to_capture_ipa_stress_mark, phoneme))
            if not matches:
                ipa_version = cls.us_phone_set_to_ipa[phoneme]
                phonemes_as_ipa_symbols.append(ipa_version)
            else:
                match = matches[0]
                mark_that_was_matched = match.group()
                phoneme_without_stress = phoneme[match.end() :]
                ipa_version = cls.us_phone_set_to_ipa[phoneme_without_stress]
                final_ipa_version = f"{ipa_version}{mark_that_was_matched}"
                phonemes_as_ipa_symbols.append(final_ipa_version)

        return phonemes_as_ipa_symbols
