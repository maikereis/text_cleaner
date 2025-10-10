"""
text_cleaner/pipeline.py

Defines the TextPipeline class, which provides a simple way to compose and apply
a sequence of text transformations that inherit from `TextTransformation`.

Example:
    >>> from text_cleaner.transformations import StripWhitespace, RemoveAccents
    >>> from text_cleaner.pipeline import TextPipeline
    >>>
    >>> pipeline = TextPipeline()
    >>> pipeline.add_transformation(StripWhitespace())
    >>> pipeline.add_transformation(RemoveAccents())
    >>>
    >>> pipeline.execute("  ação  ")
    'acao'
"""

from __future__ import annotations

from typing import List

from text_cleaner.base import TextTransformation


class TextPipeline:
    """
    A sequential text transformation pipeline.

    The pipeline allows registering multiple text transformations, which are
    executed in the order they were added. Each transformation must inherit
    from `TextTransformation` and implement the `apply(text: str) -> str` method.

    Attributes:
        transformations (list[TextTransformation]): Ordered list of transformations.

    Example:
        >>> from text_cleaner.transformations import StripWhitespace, RemoveAccents
        >>> pipeline = TextPipeline()
        >>> pipeline.add_transformation(StripWhitespace())
        >>> pipeline.add_transformation(RemoveAccents())
        >>> pipeline.execute("  ação  ")
        'acao'
    """

    def __init__(self):
        self.transformations: List[TextTransformation] = []

    def add_transformation(self, transformation: TextTransformation) -> None:
        """
        Adds a transformation to the pipeline.

        Args:
            transformation: An instance of a class implementing TextTransformation.

        Raises:
            TypeError: If the provided object is not a TextTransformation instance.
        """
        if not isinstance(transformation, TextTransformation):
            raise TypeError(
                f"Expected a TextTransformation, got {type(transformation).__name__}"
            )
        self.transformations.append(transformation)

    def execute(self, text: str | None) -> str:
        """
        Applies all transformations sequentially to the input text.

        Args:
            text: The input string. If None, an empty string is returned.

        Returns:
            The transformed string after applying all transformations.
        """
        if text is None:
            return ""
        for transformation in self.transformations:
            text = transformation.apply(text)
        return text
