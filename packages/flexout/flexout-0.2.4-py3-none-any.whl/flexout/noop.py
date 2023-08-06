from __future__ import annotations
from io import IOBase
from .base import BaseOut

class NoopOut(BaseOut):
    def __bool__(self):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    @property
    def file(self) -> IOBase|None:
        return None

    def print_title(self, title: str = None, out = None, level = None):
        return None
