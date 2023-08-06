from __future__ import annotations
import csv, _csv, os, locale, logging, sys
from datetime import datetime, timezone
from typing import Any

if sys.version_info[0:2] < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

from . import filemgr
from .base import BaseOut


logger = logging.getLogger(__name__)


class CsvOut(BaseOut):
    def __init__(self, dialect: str|csv.Dialect|type[csv.Dialect] = None, timezone: Literal['local']|timezone = None, **kwargs):
        super().__init__(**kwargs)

        # For CSV files:
        # - Set newline to '', otherwise newlines embedded inside quoted fields will not be interpreted correctly. See footnote of: https://docs.python.org/3/library/csv.html
        # - Set encoding to utf-8-sig (UTF8 with BOM): CSV is for exchanges, encoding should not depend on the exporting operating system. BOM is necessary for correct display with Excel.
        if self._newline is None:
            self._newline = ''
        if self._encoding is None:
            self._encoding = 'utf-8-sig'

        self._dialect = get_dialect(dialect)
        dialect_str = (self._dialect if isinstance(self._dialect, str) else (self._dialect.__name__ if isinstance(self._dialect, type) else type(self._dialect).__name__)).replace('_', '-')

        if dialect_str == 'excel':
            self._excel_dialect = 'default'
        elif dialect_str.startswith('excel-'):
            self._excel_dialect = dialect_str[6:]
        else:
            self._excel_dialect = None
        
        self._timezone = timezone

        self._headers_mapping: dict[int,int] = None


    def _open_path(self):
        if not hasattr(self, '_previous_headers'):
            self._read_existing_file_if_any()

        return super()._open_path()

    
    def _read_existing_file_if_any(self):
        if hasattr(self, 'previous_headers'):
            return
        
        # Determine headers of existing file
        self._previous_headers: list[str] = None
        if self._append and self._path and filemgr.exists(self._path):
            with filemgr.open_file(self._path,  mode='r', newline=self._newline, encoding=self._encoding) as f:
                reader = csv.reader(f, dialect=self._dialect)
                try:
                    self._previous_headers = next(reader)
                except StopIteration:
                    self._previous_headers = None


    @property
    def _writer(self) -> _csv._writer:
        try:
            return self.__writer
        except AttributeError:
            self.__writer = csv.writer(self.file, dialect=self._dialect)
            return self.__writer


    _headers_mapping_actual_len: int


    def _output_headers(self):
        if not hasattr(self, '_previous_headers'):
            self._read_existing_file_if_any()
        
        if self._previous_headers:
            # Determine mapping
            additional_headers = []
            for pos, header in enumerate(self._headers):
                try:
                    previous_pos = self._previous_headers.index(header)
                except ValueError:
                    additional_headers.append(header)
                    previous_pos = len(self._previous_headers) + len(additional_headers) - 1

                if previous_pos != pos:
                    if self._headers_mapping is None:
                        self._headers_mapping = {}
                    self._headers_mapping[pos] = previous_pos

            if additional_headers:
                logger.warning(f"header missing in existing file: {', '.join(additional_headers)} - corresponding data will be appended without the header name")

            self._headers_mapping_actual_len = len(self._headers) + len(additional_headers)

        else:
            self._writer.writerow(self._headers)
            self.file.flush()


    def _on_append(self, row: list):
        if self._headers_mapping:
            # Apply mapping
            reordered_row = [None] * self._headers_mapping_actual_len
            pos = 0
            while pos < len(row):
                reordered_row[self._headers_mapping.get(pos, pos)] = row[pos]
                pos += 1
            row = reordered_row

        self._writer.writerow(row)
        self.file.flush()


    def _format_value(self, value: Any) -> str:
        if value is None:
            return None
        elif isinstance(value, datetime):
            # If output is expected in a given timezone, we make this datetime naive in the target timezone and display it in a format understandable by Excel
            if value.tzinfo:
                if self._timezone:
                    value: datetime = value.astimezone(None if self._timezone == 'local' else self._timezone)
                    use_tzinfo = False
                else:
                    use_tzinfo = True
            else:
                use_tzinfo = False

            # Format microseconds. For excel, remove it if we can make Excel interprete the value as datetime
            if self._excel_dialect or value.microsecond == 0:
                mspart = ''
            else:
                mspart = '.' + value.strftime('%f')
            
            # Format tzinfo and microseconds
            if use_tzinfo:
                tzpart = value.strftime('%z')
                if len(tzpart) == 5:
                    tzpart = tzpart[0:3] + ':' + tzpart[3:]
            else:
                tzpart = ''

            return value.strftime("%Y-%m-%d %H:%M:%S") + mspart + tzpart
        elif isinstance(value, float) and self._excel_dialect == 'fr':
            return str(value).replace('.', ',')
        elif hasattr(value, 'value'): # example: ValueString
            return getattr(value, 'value')
        else:
            return super()._format_value(value)


class excel_fr(csv.excel):
    """ Dialect for French version of Excel. """
    delimiter = ";"


def get_dialect(name: str|csv.Dialect|type[csv.Dialect] = None, default: str|csv.Dialect|type[csv.Dialect] = None) -> str|csv.Dialect|type[csv.Dialect]:
    # Register my own dialects
    available_dialects = csv.list_dialects()

    if 'excel-fr' not in available_dialects:
        csv.register_dialect('excel-fr', excel_fr())
        available_dialects.append('excel-fr')

    # Return if name or default given
    if name:
        return name
    
    if default:
        return default
    
    default = os.environ.get("CSV_DIALECT", None)
    if default:
        return default

    # If nothing provided, try to detect language
    language_code, _ = locale.getlocale()
    lang = language_code[0:2]
    dialect = f"excel-{lang}"
    if dialect in available_dialects:
        return dialect

    return 'excel'
