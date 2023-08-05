""" 
A contribution from Gabriel de Jesus (https://www.linkedin.com/in/gabrieljesus/)
as part of his Ph.D. research work. 

The Tetun tokenizer supports the following tokenization techniques:
* tokenize the input string by word, punctuations, or special characters delimiters.
* tokenize the input string by whitespace delimiter.
* Tokenize sentence by .?! delimiters.
* tokenize the input string by blank lines delimiter.
* tokenize the input string by extracting only string and number and ignore punctuations and special characters.
* tokenize the input string by extracting only string and ignore numbers, punctuations, and special characters.

Note: please cite tetun-tokenizer if you use it for scientific publication purposes or contribute to a community.
"""
import re
from typing import List
from . import tetun_patterns


class TetunRegexTokenizer:
    """ The base tokenizer class. """

    def __init__(self, patterns: str, split: bool = False) -> None:
        """
        :param patterns: regular expression patterns to match the tokens.
        :param split: if True, use re.split() to tokenize text, else use re.findall().            
        """
        self.patterns = patterns
        self.split = split

    def tokenize(self, text: str) -> List[str]:
        """ 
        :param text: the text to be tokenized.
        :return: a list of tokens.
        """
        if self.split:
            tokens = re.split(self.patterns, text)
        else:
            tokens = re.findall(self.patterns, text)
        return tokens


class TetunStandardTokenizer(TetunRegexTokenizer):
    """ Tokenize text by word, punctuations, symbols, or special characters delimiters. """

    def __init__(self) -> None:
        patterns = f"{tetun_patterns.TETUN_TEXT_PATTERN}|{tetun_patterns.DIGITS_PATTERN}|{tetun_patterns.PUNCTUATIONS_SYMBOLS_PATTERN}"
        super().__init__(patterns)


class TetunWhiteSpaceTokenizer(TetunRegexTokenizer):
    """ Tokenize text by whitespace delimiter. """

    def __init__(self) -> None:
        patterns = f"{tetun_patterns.WHITESPACE_PATTERNS}"
        super().__init__(patterns, split=True)


class TetunSentenceTokenizer(TetunRegexTokenizer):
    """ Tokenize text by .?! delimiters. """

    def __init__(self) -> None:
        patterns = f"{tetun_patterns.SENTENCE_DELIMITER_PATTERN}"
        super().__init__(patterns, split=True)


class TetunBlankLineTokenizer(TetunRegexTokenizer):
    """ Tokenize a text, treating any sequence of blank lines as a delimiter. """

    def __init__(self) -> None:
        patterns = f"{tetun_patterns.SEQUENCE_BLANKLINES_PATTERN}"
        super().__init__(patterns, split=True)


class TetunSimpleTokenizer(TetunRegexTokenizer):
    """ Tokenize strings and numbers and ignore punctuations and special characters. """

    def __init__(self) -> None:
        patterns = f"{tetun_patterns.TETUN_TEXT_PATTERN}|{tetun_patterns.DIGITS_PATTERN}"
        super().__init__(patterns)


class TetunWordTokenizer(TetunRegexTokenizer):
    """ Tokenize strings and ignore numbers, punctuations and special characters. """

    def __init__(self) -> None:
        patterns = f"{tetun_patterns.TETUN_TEXT_PATTERN}"
        super().__init__(patterns)
