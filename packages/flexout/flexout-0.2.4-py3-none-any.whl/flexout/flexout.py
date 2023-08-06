from __future__ import annotations
import sys, re
import os.path
import datetime
from pathlib import Path
from io import IOBase

if sys.version_info[0:2] < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

from .base import BaseOut
from .noop import NoopOut
from .csv import CsvOut
from .tabulate import TabulateOut
from .excel import ExcelOut


def flexout(out: Path|str|IOBase = None, format: Literal['csv']|Literal['tabulate']|Literal['excel']|type[BaseOut] = None,
            headers: list[str] = None, append: bool = False, newline: str = None, encoding: str = None, dialect: str = None, timezone: Literal['local']|Literal['utc']|datetime.timezone = None,
            **kwargs) -> BaseOut:
    """
    Write text or tabular data to a flexible, easily configurable output: CSV or Excel file, or tabulated stdout/stderr.

    Parameters:

    - `out`:
        - `sys.stdout` (or `"stdout"` or `None`) (default): standard output
        - `sys.stderr` (or `"stderr"`): standard error output
        - a `str` or a `Path`: path to a file that will be opened and closed by flexout
        - an `IOBase` (already opened)
        - `False` for a noop (does nothing)

    - `format`: `"csv"` (or `CsvOut`), `"tabulate"` (or `TabulateOut`, requires package `tabulate`) or `"excel"` (or `ExcelOut`, requires packages `openpyxl` and `defusedxml`).
        
    Example 1: export text to stdout or to a file:

    ```
    with flexout(filename or "stdout") as o:
        o.file.write("Content")
    ```
    
    Example 2: export tabular data to stdout or to a file:

    ```
    with flexout(filename or "stdout", headers=["Id", "Word"]) as o:
        o.append(1, "Hello")
        o.append(2, "World")
    ```
    """    
    if out == False or out == "noop":
        return NoopOut()

    if isinstance(format, str):
        if format == 'csv':
            format = CsvOut
        elif format == 'tabulate':
            format = TabulateOut
        elif format == 'excel':
            format = ExcelOut

    if format and not (isinstance(format, type) and issubclass(format, BaseOut)):
        raise ValueError(f"invalid type for argument \"format\": {type(format).__name__}")
    

    target: IOBase|str = None
    
    if not out or out == "stdout" or out == sys.stdout:
        target = sys.stdout
        if format is None:
            format = TabulateOut if TabulateOut.is_available() else CsvOut

    elif out == "stderr" or out == sys.stderr:
        target = sys.stderr
        if format is None:
            format = TabulateOut if TabulateOut.is_available() else CsvOut

    elif isinstance(out, IOBase):
        target = out
        if format is None:
            format = CsvOut

    elif isinstance(out, (Path,str)):
        if not isinstance(out, str):
            target = str(out)
        else:
            target = out
        
        target = os.path.expanduser(target)
        if kwargs:
            target = target.format(**kwargs)

        if format is None:
            if re.search(r'\.xlsx(?:#[^\.]+)?$', target, re.IGNORECASE):
                format = ExcelOut
            else:
                format = CsvOut
    else:
        raise ValueError(f"invalid type for argument \"out\": {type(out).__name__}")


    # Prepare other arguments
    if isinstance(timezone, str):
        if timezone == 'utc':
            timezone = datetime.timezone.utc
            
    safe_kwargs = {key: value for key, value in kwargs.items() if key not in ['target', 'headers', 'append', 'newline', 'encoding', 'dialect', 'timezone']}

    # Instanciate and return format object
    return format(target=target, headers=headers, append=append, newline=newline, encoding=encoding, dialect=dialect, timezone=timezone, **safe_kwargs)
