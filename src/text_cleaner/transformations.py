"""
text_cleaner/transformations.py

This module defines a set of text transformation classes used for cleaning and
normalizing text data. Each transformation implements a common interface
(`TextTransformation`) with an `apply()` method that takes a string and returns
a transformed version.

These transformations can be combined in text preprocessing pipelines for
machine learning, NLP, or general text normalization tasks.
"""

import re
import unicodedata

from text_cleaner.base import TextTransformation

# === Whitespace & Basic Cleanup ====================================================


class StripWhitespace(TextTransformation):
    """Removes leading and trailing whitespace from the text."""

    def apply(self, text: str) -> str:
        return text.strip()


class ReplaceMultipleSpaces(TextTransformation):
    """Collapses multiple consecutive whitespace characters into a single space."""

    _pattern = re.compile(r"\s+")

    def apply(self, text: str) -> str:
        return self._pattern.sub(" ", text)


# === Character Normalization =======================================================


class RemoveAccents(TextTransformation):
    """
    Removes accentuation from characters using Unicode normalization (NFD).

    Converts accented characters to their base forms:
      - 'é' → 'e'
      - 'ñ' → 'n'

    Example:
        >>> RemoveAccents().apply("ação")
        'acao'
    """

    def apply(self, text: str) -> str:
        return "".join(
            ch
            for ch in unicodedata.normalize("NFD", text)
            if unicodedata.category(ch) != "Mn"
        )


class RemoveNonAsciiExceptAccents(TextTransformation):
    """
    Removes non-ASCII characters except Latin letters (including those with diacritics).
    Removes characters from other scripts (e.g. Chinese, Japanese, Cyrillic).
    """

    def apply(self, text: str) -> str:
        result = []
        for c in text:
            if ord(c) < 128:
                result.append(c)
                continue
            try:
                name = unicodedata.name(c)
                if "LATIN" in name:
                    result.append(c)
            except ValueError:
                # Some characters have no name in Unicode
                pass
        return "".join(result)


# === Symbol & Token Removal ========================================================


class RemoveEmojis(TextTransformation):
    """Removes emoji characters based on Unicode ranges."""

    _emoji_pattern = re.compile(
        "["
        + "\U0001f600-\U0001f64f"  # Emoticons
        + "\U0001f300-\U0001f5ff"  # Symbols & pictographs
        + "\U0001f680-\U0001f6ff"  # Transport & map symbols
        + "\U0001f1e0-\U0001f1ff"  # Flags
        + "]+",
        flags=re.UNICODE,
    )

    def apply(self, text: str) -> str:
        return self._emoji_pattern.sub("", text)


class RemoveEmails(TextTransformation):
    """Removes email addresses from text."""

    _pattern = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w{2,}\b")

    def apply(self, text: str) -> str:
        return self._pattern.sub("", text)


class RemoveUserIDs(TextTransformation):
    """
    Removes user IDs matching 'u' or 'U' followed by digits.

    Example:
        'u5513567' → ''
        'U123456' → ''
    """

    _pattern = re.compile(r"\b[uU]\d+\b")

    def apply(self, text: str) -> str:
        return self._pattern.sub("", text)


class RemoveLongNumbers(TextTransformation):
    """
    Removes numeric sequences longer than 10 digits, such as protocol numbers or IDs.

    Example:
        'Order 12345678901' → 'Order'
    """

    _pattern = re.compile(r"\b\d{10,}\b")

    def apply(self, text: str) -> str:
        return self._pattern.sub("", text)


class RemoveLongAlphanumerics(TextTransformation):
    """
    Removes long alphanumeric tokens with 10 or more characters.

    Useful for removing hash-like strings such as:
        '7434000304c3745cddbee9251a9cb6f5' → ''
    """

    _pattern = re.compile(r"\b[a-zA-Z0-9]{10,}\b")

    def apply(self, text: str) -> str:
        return self._pattern.sub("", text)


class RemoveDateTime(TextTransformation):
    """
    Removes date-time patterns in the format 'DD/MM/YYYY HH:MM:SS'.

    Example:
        'Event on 17/05/2025 17:56:50' → 'Event on'
    """

    _pattern = re.compile(r"\b\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}\b")

    def apply(self, text: str) -> str:
        return self._pattern.sub("", text)


# === Custom Substring Removal ======================================================


class RemoveSubstrings(TextTransformation):
    """
    Removes all occurrences of specific substrings from text (case-insensitive).

    Args:
        substrings: A list of literal substrings to remove.

    Example:
        >>> t = RemoveSubstrings(["CONFIDENCIAL", "TESTE"])
        >>> t.apply("Documento confidencial de teste")
        'Documento  de '
    """

    def __init__(self, substrings: list[str]):
        self.substrings = substrings

    def apply(self, text: str) -> str:
        for substring in self.substrings:
            pattern = re.escape(substring)
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        return text
