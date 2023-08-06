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
* `data`: A list of objects or dicts that should be exported
* `column_definitions`: A list of `ColumnDefinition` objects that define the columns of the csv file and how to get the data for each row
* `filename`: The filename of the csv file to be generated. If None, no file is written
* `timezone`: The timezone into which datetime objects should be converted. Default is timezone set in settings

It returns the csv as encoded byte array. 
It raises exceptions if wrong datatypes are passed or if timezone is not known or on unexpected errros.

```python
from datetime import datetime
from openmodule.utils.csv_export import render, ColumnDefinition, CsvFormatType
from openmodule.config import settings

data = [{"session id": "123", "entry time": datetime.utcnow()}, 
        {"session id": "456", "entry time": None}]
render(data, [ColumnDefinition("garage", "", CsvFormatType.static_text, settings.RESOURCE),
              ColumnDefinition("session id", "session id", CsvFormatType.string),
              ColumnDefinition("entry time", "entry time", CsvFormatType.datetime, datetime.max)], "output.csv")
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
