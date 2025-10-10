import pytest

from text_cleaner.base import TextTransformation
from text_cleaner.pipeline import TextPipeline


class MockTransformation(TextTransformation):
    """Mock transformation that records calls and appends a marker to text."""

    def __init__(self, marker: str):
        self.marker = marker
        self.calls = 0

    def apply(self, text: str) -> str:
        self.calls += 1
        return f"{text}{self.marker}"


class UppercaseTransformation(TextTransformation):
    """Simple transformation that uppercases text."""

    def apply(self, text: str) -> str:
        return text.upper()


def test_add_transformation_accepts_valid_instance():
    pipeline = TextPipeline()
    t = MockTransformation("!")
    pipeline.add_transformation(t)
    assert pipeline.transformations == [t]


def test_add_transformation_raises_on_invalid_type():
    pipeline = TextPipeline()
    with pytest.raises(TypeError):
        pipeline.add_transformation("not a transformation")  # type: ignore


def test_pipeline_initially_empty():
    pipeline = TextPipeline()
    assert pipeline.transformations == []


def test_execute_applies_all_transformations_in_order():
    pipeline = TextPipeline()
    t1 = MockTransformation("A")
    t2 = MockTransformation("B")
    pipeline.add_transformation(t1)
    pipeline.add_transformation(t2)

    result = pipeline.execute("x")

    assert result == "xAB"
    assert t1.calls == 1
    assert t2.calls == 1


def test_execute_handles_empty_string():
    pipeline = TextPipeline()
    pipeline.add_transformation(MockTransformation("*"))
    result = pipeline.execute("")
    assert result == "*"


def test_execute_returns_empty_string_for_none_input():
    pipeline = TextPipeline()
    pipeline.add_transformation(MockTransformation("*"))
    assert pipeline.execute(None) == ""


def test_execute_with_no_transformations_returns_input():
    pipeline = TextPipeline()
    assert pipeline.execute("hello") == "hello"


def test_pipeline_is_order_sensitive():
    """Order of transformations affects output."""
    p1 = TextPipeline()
    p2 = TextPipeline()

    p1.add_transformation(MockTransformation("A"))
    p1.add_transformation(MockTransformation("B"))

    p2.add_transformation(MockTransformation("B"))
    p2.add_transformation(MockTransformation("A"))

    assert p1.execute("X") != p2.execute("X")
    assert p1.execute("X") == "XAB"
    assert p2.execute("X") == "XBA"


def test_pipeline_with_realistic_transformation_behavior():
    pipeline = TextPipeline()
    pipeline.add_transformation(UppercaseTransformation())
    pipeline.add_transformation(MockTransformation("!"))

    result = pipeline.execute("hello")
    assert result == "HELLO!"


def test_pipeline_can_chain_multiple_calls():
    """Executing twice should yield consistent, independent results."""
    pipeline = TextPipeline()
    t = MockTransformation("*")
    pipeline.add_transformation(t)

    first = pipeline.execute("a")
    second = pipeline.execute("b")

    assert first == "a*"
    assert second == "b*"
    assert t.calls == 2
