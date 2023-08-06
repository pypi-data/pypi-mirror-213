# CSV Exporter

The file `utils/csv_export.py` contains a `render` function that can be used to export a list of objects or dicts to a 
csv file. 
Important specifications of the generated csv file:
* encoding "utf-16-le"
* `csv.QUOTE_ALL` setting 
* "," as comma for floats. 
* delimiter is `"\t"` 
* line terminator is `"\r\n"`. 

Important note: None values are converted to empty strings.

## Usage

The render function takes the following arguments:
* `file_object`: A file object to which the csv should be written. It must be opened in binary mode
* `data`: A list of objects or dicts that should be exported
* `column_definitions`: A list of `ColumnDefinition` objects that define the columns of the csv file and how to get the data for each row
* `timezone`: The timezone into which datetime objects should be converted. Default is timezone set in settings

It raises exceptions if wrong datatypes are passed or if timezone is not known or on unexpected errros.

```python
from datetime import datetime
from openmodule.utils.csv_export import render, ColumnDefinition, CsvFormatType
from openmodule.config import settings

class SomeObject:
    def __init__(self, session_id, entry_time, exit_time, price):
        self.session_id = session_id
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.price = price

# export object
objs = [SomeObject("123", datetime.utcnow(), datetime.utcnow(), 123),
        SomeObject("124", datetime.utcnow(), datetime.utcnow(), 123)]
with open("output.csv", 'wb') as f:
    render(f, objs, [ColumnDefinition("garage", "", CsvFormatType.static_text, settings.RESOURCE),
                     ColumnDefinition("session id", "session_id", CsvFormatType.string),
                     ColumnDefinition("exit time", "exit_time", CsvFormatType.datetime, datetime.max),
                     ColumnDefinition("total price", "price", CsvFormatType.currency_amount)])

# export dict
data = [{"session id": objs[0].session_id, "duration": objs[0].exit_time - objs[0].entry_time}]
with open("output2.csv", 'wb') as f:
  render(f, data, [ColumnDefinition("garage", "", CsvFormatType.static_text, settings.RESOURCE),
                   ColumnDefinition("session id", "session id", CsvFormatType.string),
                   ColumnDefinition("duration", "duration", CsvFormatType.duration)])
```

## ColumnDefinition

The `ColumnDefinition` class is used to define the columns of the csv file. It takes the following arguments in constuctor:
* `name`: The name of the column. This is used as header in the csv file
* `field_name`: Attribute name or key in dict of the data object that should be used for this column
* `format_type`: The type of the data in this column. See `CsvFormatType` for possible values
* `default_value`: The default value for this column if the data object does not contain the attribute or key or if value is None. It must be of a type matching format_type. Default is None

## CsvFormatType
* `static_text`: Fills a static text into the column in every row. `default_value` must be a string or enum. `field_name` is ignored
* `string`: Formats data as string. Values must be either string or string enum. Checks
  * does not contain forbidden characters `["\x0d", "\x09"]`
  * string does not start with "@" or "="
  * string does not start with "+" if it is not a valid phone number
  * string does not start with "-" if it is not a valid negative number
* `number`: Formats data as number ("," is comma). Allowed datatypes are int, float, bool, Decimal
* `percentag`: Formats data as percentage ("," is comma and adds "%"). Does not multiply by 100, so 13.3 -> "13,3%". Allowed datatypes are int, float, Decimal
* `datetime`: Converts data into given timezone and formats data as datetime. Allowed datatypes are datetime and string
* `duration`: Formats data in format "H:MM:SS". Allowed datatypes are timedelta, int and float
* `currency_amount`: Formats Cent amounts into € with 2 decimal places (or equivalent for other currencies). Does NOT add currency symbol. Allowed datatype is int
