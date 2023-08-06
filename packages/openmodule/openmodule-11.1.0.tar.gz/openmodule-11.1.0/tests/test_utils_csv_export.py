from datetime import datetime, timedelta
from decimal import Decimal
from io import BytesIO
from typing import Iterable, Union, List
from unittest import TestCase

from dateutil.tz import gettz
from pydantic import DateTimeError

from openmodule.config import settings
from openmodule.utils.csv_export import render, ColumnDefinition, CsvFormatType, _ENCODING, _ENCODING_CODEC


class CsvExportTest(TestCase):
    def render(self, data: Iterable[Union[dict, object]], column_definitions: List[ColumnDefinition],
               timezone: str = settings.TIMEZONE):
        stream = BytesIO()
        render(stream, data, column_definitions, timezone)
        return stream.getvalue().decode(_ENCODING)

    def test_default_value(self):
        columns = [ColumnDefinition(name="A", field_name="a", format_type=CsvFormatType.number),
                   ColumnDefinition(name="B", field_name="b", format_type=CsvFormatType.number, default_value=0)]
        # column with default value and missing field -> default value
        data = self.render([dict(a=8)], columns)
        self.assertIn('"A"\t"B"', data)
        self.assertIn('"8"\t"0"', data)

        # column with default value and None value -> default value
        data = self.render([dict(a=8, b=None)], columns)
        self.assertIn('"A"\t"B"', data)
        self.assertIn('"8"\t"0"', data)

        # column without default value -> ""
        data = self.render([dict()], columns)
        self.assertIn('"A"\t"B"', data)
        self.assertIn('""\t"0"', data)

    def test_incorrect_default_value(self):
        columns = [ColumnDefinition(name="A", field_name="a", format_type=CsvFormatType.number),
                   ColumnDefinition(name="B", field_name="b", format_type=CsvFormatType.number, default_value="a")]
        with self.assertRaises(AssertionError) as e:
            self.render([dict(a=8)], columns)
        self.assertIn("Number columns allow only int, float, bool, Decimal", str(e.exception))

    def test_static_field(self):
        columns = [ColumnDefinition(name="value", field_name="", format_type=CsvFormatType.static_text,
                                    default_value=123)]

        with self.assertRaises(AssertionError) as e:
            self.render([{}], columns)
        self.assertIn("Static text columns allow only str or enum", str(e.exception))

        columns = [ColumnDefinition(name="value", field_name="", format_type=CsvFormatType.static_text,
                                    default_value="test")]
        data = self.render([dict()], columns)
        self.assertIn('value"\r\n"test"\r\n', data)

    def test_string_field(self):
        columns = [ColumnDefinition(name="value", field_name="value", format_type=CsvFormatType.string)]
        with self.assertRaises(AssertionError) as e:
            self.render([dict(value=type)], columns)
        self.assertIn("String columns allow only str and string enum", str(e.exception))

        with self.assertRaises(AssertionError) as e:
            self.render([dict(value="test\x0dexample")], columns)
        self.assertIn('Forbidden chars "\\x0d" or "\\x09" in string', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            self.render([dict(value="=test")], columns)
        self.assertIn('String must not start with "=" or "@"', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            self.render([dict(value="+test")], columns)
        self.assertIn('Strings starting with "+" must be phone numbers', str(e.exception))

        data = self.render([dict(value="+43 664 12345678")], columns)
        self.assertIn('value"\r\n"+43 664 12345678"\r\n', data)

        data = self.render([dict(value=1)], columns)
        self.assertIn('value"\r\n"1"\r\n', data)

        data = self.render([dict(value="asdf@=")], columns)
        self.assertIn('value"\r\n"asdf@="\r\n', data)

    def test_number_field(self):
        columns = [ColumnDefinition(name="value", field_name="value", format_type=CsvFormatType.number)]

        with self.assertRaises(AssertionError) as e:
            self.render([dict(value="a")], columns)
        self.assertIn("Number columns allow only int, float, bool, Decimal", str(e.exception))

        data = self.render([dict(value=1)], columns)
        self.assertIn('value"\r\n"1"\r\n', data)

        data = self.render([dict(value=1.2)], columns)
        self.assertIn('value"\r\n"1,2"\r\n', data)

        data = self.render([dict(value=True)], columns)
        self.assertIn('value"\r\n"1"\r\n', data)

        data = self.render([dict(value=Decimal("10.12"))], columns)
        self.assertIn('value"\r\n"10,12"\r\n', data)

    def test_percentage_field(self):
        columns = [ColumnDefinition(name="value", field_name="value", format_type=CsvFormatType.percentage)]

        with self.assertRaises(AssertionError) as e:
            self.render([dict(value="a")], columns)
        self.assertIn("Percentage columns allow only int, float, Decimal", str(e.exception))

        data = self.render([dict(value=1)], columns)
        self.assertIn('value"\r\n"1%"\r\n', data)

        data = self.render([dict(value=1.2)], columns)
        self.assertIn('value"\r\n"1,2%"\r\n', data)

        data = self.render([dict(value=Decimal("10.12"))], columns)
        self.assertIn('value"\r\n"10,12%"\r\n', data)

    def test_datetime_field(self):
        columns = [ColumnDefinition(name="value", field_name="value", format_type=CsvFormatType.datetime)]
        with self.assertRaises(AssertionError) as e:
            self.render([dict(value=1)], columns)
        self.assertIn("Datetime columns allow only datetime and str", str(e.exception))
        with self.assertRaises(DateTimeError) as e:
            self.render([dict(value="a")], columns)

        # aware datetime
        timestamp = datetime(2018, 1, 1, 12, 0, 1, tzinfo=gettz(settings.TIMEZONE))
        data = self.render([dict(value=timestamp)], columns)
        self.assertIn(f'value"\r\n"01.01.2018 12:00:01"\r\n', data)

        # utc datetime
        timestamp_utc = timestamp.astimezone(gettz('UTC')).replace(tzinfo=None)
        data = self.render([dict(value=timestamp_utc)], columns)
        self.assertIn(f'value"\r\n"01.01.2018 12:00:01"\r\n', data)

        data = self.render([dict(value=timestamp.isoformat())], columns)
        self.assertIn(f'value"\r\n"01.01.2018 12:00:01"\r\n', data)

        data = self.render([dict(value=timestamp_utc.isoformat())], columns)
        self.assertIn(f'value"\r\n"01.01.2018 12:00:01"\r\n', data)

        data = self.render([dict(value=timestamp_utc)], columns, "UTC")
        self.assertIn(f'value"\r\n"01.01.2018 11:00:01"\r\n', data)  # 11 because of winter

    def test_duration_field(self):
        columns = [ColumnDefinition(name="value", field_name="value", format_type=CsvFormatType.duration)]
        with self.assertRaises(AssertionError) as e:
            self.render([dict(value="a")], columns)
        self.assertIn("Duration columns allow only timedelta, int and float", str(e.exception))

        data = self.render([dict(value=10)], columns)
        self.assertIn(f'value"\r\n"0:00:10"\r\n', data)

        data = self.render([dict(value=12.1)], columns)
        self.assertIn(f'value"\r\n"0:00:12"\r\n', data)

        data = self.render([dict(value=timedelta(hours=12345, minutes=53, seconds=10, milliseconds=125))], columns)
        self.assertIn(f'value"\r\n"12345:53:10"\r\n', data)

    def test_currency_field(self):
        columns = [ColumnDefinition(name="value", field_name="value", format_type=CsvFormatType.currency_amount)]
        with self.assertRaises(AssertionError) as e:
            self.render([dict(value=123.45)], columns)
        self.assertIn("Currency amount columns allow only int", str(e.exception))

        data = self.render([dict(value=123)], columns)
        self.assertIn(f'value"\r\n"1,23"\r\n', data)

    def test_encoding(self):
        columns = [ColumnDefinition(name="value", field_name="value", format_type=CsvFormatType.string)]
        stream = BytesIO()
        render(stream, [dict(value="ÄÖÜß")], columns)
        data = stream.getvalue()
        self.assertEqual(data[:2], _ENCODING_CODEC)
        self.assertIn("ÄÖÜß".encode(_ENCODING), data)
