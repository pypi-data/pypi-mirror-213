import codecs
import csv
import re
from datetime import datetime, timedelta, tzinfo
from decimal import Decimal
from enum import Enum
from typing import List, Union, Optional, Iterable, Any, BinaryIO

from dateutil.tz import gettz, UTC
from openmodule.config import settings
from pydantic.datetime_parse import parse_datetime


class CsvFormatType(str, Enum):
    static_text = "static_text"
    """just inserts static text"""

    string = "string"
    """no reformatting, works for str, int (e.g. for vehicle_id) and enum"""

    number = "number"
    """correct seperator for floating point values, works for int, float, Decimal and bool"""

    percentage = "percentage"
    """added % and correct seperator for floating point values. Does NOT divide by 100. 
    works for float, int and Decimal"""

    datetime = "datetime"
    """converts into specified timezone and prints as iso string. Works for datetime"""

    duration = "duration"
    """formats as HH:MM::SS. Works for timedelta"""

    currency_amount = "currency_amount"
    """formats Cent amounts into € with 2 decimal places (or equivalent for other currencies). 
    does NOT add currency symbol"""


_NUMBER_REGEX = re.compile(r"^\s*-[*\s.,\d]*$")
_PHONE_REGEX = re.compile(r"^\s*\+[*\s\d\(\)]*$")

# some constants which might be turned into parameters later
_COMMA_SEPARATOR = ","
_DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"
_ENCODING = "utf-16-le"
_ENCODING_CODEC = codecs.BOM_UTF16_LE


def _format_static_text(value: Union[str, Enum]) -> str:
    assert isinstance(value, str), "Static text columns allow only str or enum"
    return _format_string(value)


def _format_string(value: Union[str, Enum]) -> str:
    assert isinstance(value, str) or isinstance(value, int), "String columns allow only str and string enum"
    if isinstance(value, str):
        assert all(bad_char not in value for bad_char in ["\x0d", "\x09"]), \
            'Forbidden chars "\\x0d" or "\\x09" in string'
        assert not value or value[0] not in "=@", 'String must not start with "=" or "@"'
        assert (value and value[0]) != "+" or _PHONE_REGEX.match(value), \
            'Strings starting with "+" must be phone numbers'
        assert (value and value[0]) != "-" or _NUMBER_REGEX.match(value), 'Strings starting with "-" must be numbers'
    else:
        value = str(value)
    return value


def _format_number(value: Union[int, float, bool, Decimal]) -> str:
    assert any(isinstance(value, t) for t in [int, float, bool, Decimal]), \
        "Number columns allow only int, float, bool, Decimal"
    if isinstance(value, bool):
        value = int(value)
    return str(value).replace(".", _COMMA_SEPARATOR)


def _format_percentage(value: Union[int, float, Decimal]) -> str:
    assert any(isinstance(value, t) for t in [int, float, Decimal]), \
        "Percentage columns allow only int, float, Decimal"
    return str(value).replace(".", _COMMA_SEPARATOR) + "%"


def _format_datetime(value: Union[datetime, str], timezone: tzinfo) -> str:
    assert isinstance(value, datetime) or isinstance(value, str), "Datetime columns allow only datetime and str"
    if isinstance(value, str):
        value = parse_datetime(value)
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:  # is naive -> assume UTC
        value = value.replace(tzinfo=UTC)
    return value.astimezone(timezone).strftime(_DATETIME_FORMAT)


def _format_duration(value: Union[timedelta, int, float]) -> str:
    assert any(isinstance(value, t) for t in [timedelta, int, float]), \
        "Duration columns allow only timedelta, int and float"
    if isinstance(value, timedelta):
        value = int(value.total_seconds())
    elif isinstance(value, float):
        value = int(value)
    return f"{value//3600:d}:{(value%3600)//60:02d}:{value%60:02d}"


def _format_currency_amount(value: int) -> str:
    assert isinstance(value, int), "Currency amount columns allow only int"
    value = Decimal(value) / Decimal(100.)
    return f"{value:.2f}".replace(".", _COMMA_SEPARATOR)


class ColumnDefinition:
    def __init__(self, name: str, field_name: str, format_type: CsvFormatType, default_value: Optional[Any] = None):
        self.name = name
        self.field_name = field_name
        self.format_type = format_type
        self.default_value = default_value


def _render_row(writer, row: Union[dict, object], column_definitions: List[ColumnDefinition], timezone: tzinfo):
    values = []
    if not isinstance(row, dict):
        row = row.__dict__
    for column in column_definitions:
        value = row.get(column.field_name) if column.format_type != CsvFormatType.static_text else None
        if value is None:
            value = column.default_value
        if value is None:
            values.append(None)
        elif column.format_type == CsvFormatType.static_text:
            values.append(_format_static_text(column.default_value))
        elif column.format_type == CsvFormatType.string:
            values.append(_format_string(value))
        elif column.format_type == CsvFormatType.number:
            values.append(_format_number(value))
        elif column.format_type == CsvFormatType.percentage:
            values.append(_format_percentage(value))
        elif column.format_type == CsvFormatType.datetime:
            values.append(_format_datetime(value, timezone))
        elif column.format_type == CsvFormatType.duration:
            values.append(_format_duration(value))
        elif column.format_type == CsvFormatType.currency_amount:
            values.append(_format_currency_amount(value))
    writer.writerow(values)


def render(file_object: BinaryIO, data: Iterable[Union[dict, object]], column_definitions: List[ColumnDefinition],
           timezone: str = settings.TIMEZONE):
    """
    Renders the data into csv based on column_definitions. If output_fn is given it's rendered directly into file
    otherwise bytearray is returned
    :param file_object: File like object to write csv into (binary write)
    :param data: Iterable of dicts or objects containing data for csv
    :param column_definitions: Defining columns with name, format_type and where data is in objects/dicts
    :param timezone: timezone into which datetime columns are converted
    """

    timezone_obj = gettz(timezone)
    if timezone_obj is None:
        raise ValueError(f"{timezone} is no valid timezone")
    file_object.write(_ENCODING_CODEC)
    out_stream = codecs.getwriter(_ENCODING)(file_object)
    writer = csv.writer(out_stream, quoting=csv.QUOTE_ALL, delimiter="\t")
    headers = [column.name for column in column_definitions]
    writer.writerow(headers)
    for row in data:
        _render_row(writer, row, column_definitions, timezone_obj)
