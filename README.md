# Text Cleaner

![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)

---

A lightweight, composable text preprocessing library for Python.
It provides reusable, well-tested transformations for cleaning and normalizing text — such as removing emojis, emails, IDs, long numbers, and accents — and a flexible `TextPipeline` for chaining them together.

## Installation

pip install git+https://github.com/maikereis/text_cleaner.git


## Code Structure

```
text_cleaner/
    ├── base.py              # Abstract base class for transformations
    ├── transformations.py   # Built-in transformations (accents, emojis, etc.)
    └── pipeline.py          # Composable text pipeline
tests/
    ├── test_pipeline.py
    └── test_transformations.py
```
