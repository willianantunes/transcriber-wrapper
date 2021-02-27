import logging
import re

from typing import List
from typing import Optional

from transcriber_wrapper import logger_name

logger = logging.getLogger(logger_name)


class Restorer:
    default_punctuation_marks = ';:,.!?¡¿—…"«»“”'

    def __init__(self, marks: Optional[str] = None):
        if not marks:
            marks = self.default_punctuation_marks
        self.marks_as_regex = re.compile(fr"(\s*[{re.escape(marks)}]+\s*)+")

    def apply_punctuations(self, words_with_punctuations: List[str], words_to_receive_them: List[str]) -> List[str]:
        for index, word in enumerate(words_with_punctuations):
            matches = list(re.finditer(self.marks_as_regex, word))

            if not matches:
                continue

            for match in matches:
                mark_that_was_matched = match.group()

                # Only compute when necessary
                is_mark_in_the_beginning = lambda: word.startswith(mark_that_was_matched)
                is_mark_in_the_end = lambda: word.endswith(mark_that_was_matched)

                if is_mark_in_the_beginning():
                    words_to_receive_them[index] = f"{mark_that_was_matched}{words_to_receive_them[index]}"
                elif is_mark_in_the_end():
                    words_to_receive_them[index] = f"{words_to_receive_them[index]}{mark_that_was_matched}"

                logger.debug("Is it in the middle or alone? Won't support these now...")

        return words_to_receive_them
