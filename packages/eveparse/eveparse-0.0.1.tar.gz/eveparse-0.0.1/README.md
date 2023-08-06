# Eve Parse

Parser for Eve Online - extract item name and quantity from a string, and return values with type_id

## Install

```shell
pip install eveparse
```

## Usage

The `parse()` function takes a single-line string. It is designed to fail fast and will raise ParserError if it is unable to parse the string.

```python
import eveparse

string = "Ragnarok 1"

try:
    type_id, name, quantity = eveparse.parse(string)
except eveparse.ParserError as error:
    print(error)
else:
    print(type_id, name, quantity)
```
