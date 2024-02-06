from loguru import logger
from polyglot.detect import Detector


def is_phrase_valid(phrase: str, language: str) -> bool:
    """
    This is func for check phrase on valid
    :param phrase: str
    :param language: str
    :return: bool
    """
    phrase_words = phrase.split()

    if len(phrase_words) != len(set(phrase_words)):
        return False

    for word in phrase_words:
        if word.isdigit():
            return False

    detector = Detector(phrase, quiet=True)
    if detector.language.code != language:
        return False

    return True


def filter_phrases(phrases: list[str], language: str) -> list[str]:
    """
      This is func for check phrase on valid
      :param phrases: list[str]
      :param language: str
      :return: list[str]
      """
    valid_phrases = []

    logger.info("Filtering generated phrases")
    for phrase in phrases:
        if is_phrase_valid(phrase, language):
            valid_phrases.append(phrase)

    return valid_phrases
