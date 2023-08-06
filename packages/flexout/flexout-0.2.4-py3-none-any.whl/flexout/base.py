from __future__ import annotations
import logging, sys
from io import IOBase
from enum import Enum

from . import filemgr

logger = logging.getLogger(__name__)

_DICT_KEYS_TYPE = type({}.keys())


class BaseOut:
    def __init__(self, target: IOBase|str = None, headers: list[str] = None, append: bool = False, newline: str = None, encoding: str = None, **kwargs):
        # Management of file and path
        if isinstance(target, IOBase) or not target:
            self._file = target
            self._external_file = True
            self._path = None
            self._table_name = None
            self._name = _get_iobase_name(target)
        else:
            self._file = None
            self._external_file = False
            self._path, self._table_name = _split_path_target(target)
            self._name = target

        self._append = append
        self._newline = newline
        self._encoding = encoding

        # Management of tabular data
        self._headers: list[str] = _get_headers_from_arg(headers) if headers else []
        self._rows: list[list] = []
        self._wait_for_more_headers: bool = True
        self._delayed_rows: list[list] = []
        self._rows_count: int = 0
        self._missing_in_headers: list[str] = []


    # -------------------------------------------------------------------------
    # Open/close
    # -------------------------------------------------------------------------

    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):        
        if exc_type:
            return # forward exception

        self._flush_delayed()
        
        self._before_close()

        if self._file and not self._external_file:
            self._file.close()


    def _open_path(self):
        if not self._path:
            raise ValueError(f'cannot open path for {self._name}')
        return filemgr.open_file(self._path, mode='a' if self._append else 'w', newline=self._newline, encoding=self._encoding, mkdir=True)


    def _flush_delayed(self):
        if self._wait_for_more_headers:
            self._wait_for_more_headers = False
            if self._headers:
                self._output_headers()

        if self._delayed_rows:
            for drow in self._delayed_rows:
                self._actual_append(drow)
            
            self._delayed_rows = []


    def _before_close(self):
        pass


    # -------------------------------------------------------------------------
    # Main public interface
    # -------------------------------------------------------------------------

    @property
    def rows(self):
        return self._rows


    @property
    def headers(self):
        return self._headers
       

    @headers.setter
    def headers(self, value: list[str]):
        if self._headers:
           raise ValueError('cannot add headers anymore')

        self._headers = _get_headers_from_arg(value)
        self._wait_for_more_headers = False
        self._output_headers()


    def append(self, *args, nowait=False):
        """
        Add a tabular row.

        If a single dict is passed as argument, keys of the dict are considered to be table headers :
        - If output has already started, the row will be written immediatly (an exception will be raised if any key of the dict does not match the headers)
        - If output has NOT started yet, writing of the row will be delayed (headers will be updated with the keys of the dict), except if option `nowait` is set to True
        """
        self._rows_count += 1

        if len(args) == 1 and isinstance(args[0], dict):
            # Dict row: keys are headers.

            if self._headers is None:
                self._headers = []
            
            missing_in_headers = []

            row = [None] * len(self._headers)            
            for key, value in args[0].items():
                try:
                    index = self._headers.index(key)
                    row[index] = value
                except:
                    if self._wait_for_more_headers:
                        # add to headers
                        self._headers.append(key)
                        row.append(value)
                    else:
                        # missing in headers: we only warn for the first occurrence                        
                        if not key in self._missing_in_headers:
                            missing_in_headers.append(key)
                            self._missing_in_headers.append(key)

            if missing_in_headers:
                logger.warning(f"ignore value for key not found in headers: {', '.join(missing_in_headers)} (first occurence on row {self._rows_count})")
            
            if self._wait_for_more_headers and not nowait:
                self._delayed_rows.append(row)
            else:
                self._flush_delayed()
                self._actual_append(row)

        else:
            # Row without header information is given: we write the row immediatly
            if len(args) == 1 and _is_row(args[0]):
                # The first argument is an iterable that is considered the actual row
                row = list(args[0])
            else:
                row = list(args)

            self._flush_delayed()
            self._actual_append(row)


    @property
    def file(self) -> IOBase:
        if not self._file:
            self._file = self._open_path()
        return self._file


    def __str__(self) -> str:
        return self._name


    def print_title(self, title: str = None, out = None, level = None):
        if out or (hasattr(self, '_file') and self._file in [sys.stdout, sys.stderr]):
            if not out:
                out = self._file
            print('\n##########%s##########\n' % (f' {title[0].upper()+title[1:]} ' if title else ''), file=out)
        else:
            logger.log(level if level is not None else logging.INFO, 'export %sto %s' % (f'{title} ' if title else '', self._name))


    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _actual_append(self, row: list):
        row = self._format_row(row)
        self._on_append(row)
        self.rows.append(row)


    def _output_headers(self):
        pass # Implemented by subclasses


    def _on_append(self, row: list):
        pass # Implemented by subclasses
        

    def _format_row(self, row: list):
        if self._headers:
            while len(row) < len(self._headers):
                row.append(None)

        for i, value in enumerate(row):
            row[i] = self._format_value(value)

        return row


    def _format_value(self, value) -> str:
        if value is None:
            return None
        elif isinstance(value, Enum):
            return value.name
        elif isinstance(value, list):
            return '|'.join(str(val) for val in value)
        else:
            return value


def _split_path_target(target: str) -> tuple[str,str]:
    """
    Return (path, table_name).
    """
    if not target:
        return (None, None)
    
    pos = target.find('#')
    if pos > 0:
        path = target[0:pos]
        arg = target[pos+1:].replace('-', '_')
    else:
        path = target
        arg = None
    
    return (path, arg)


def _get_headers_from_arg(arg) -> list[str]:
    if isinstance(arg, (tuple,_DICT_KEYS_TYPE)):
        return list(arg)
    elif isinstance(arg, list):
        return arg
    else:
        raise ValueError(f'invalid type for headers: {arg} ({type(arg).__name__})')


def _get_iobase_name(file: str) -> str:
    if not file:
        return '<none>'
    
    try:
        name = file.name
        if not name or not isinstance(name, str):
            name = None
    except AttributeError:
        name = None

    if name:
        if name.startswith('<') and name.endswith('>'):
            return name
        else:
            return f'<{name}>'

    else:
        return f"<{type(file).__name__}>"


def _is_row(arg):
    if isinstance(arg, list):
        return True
    if arg.__class__.__module__ == '__builtin__': # including strings
        return False
    return hasattr(arg, '__iter__') or hasattr(arg, '__getitem__')
