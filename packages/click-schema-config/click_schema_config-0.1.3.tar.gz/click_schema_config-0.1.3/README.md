# click-schema-config

click-schema-config allows you to add settings from a config file. Those will be automatically pulled into your program description without having to repeat them. Comments will be used as helper text for click.

# Installation

```sh
poetry add click-schema-config
```

or, using pip

```
pip install click-schema-config
```

# Usage

Decorate your function with

```
@schema_from_inis(files=[...])
```

This will automatically infer the structure of your ini files and its documentation and add it to click.

Example of a config.default.ini:

```ini
initialized_to_none =

[test1]
; Wow, multilines
; Talk about eye candy
multiline_commented="value1"
typed: int = 2
inferred = True

[test2]
inline_commented = "value1" # This comment does not appear in the documentation

; This is a comment
after_paragraph = None
```

Note that you can type values directly. If a parameter appears without = succeding it, it becomes a required parameter.

**main**.py

```python
import pprint
import click
from click_schema_config import schema_from_inis


@click.command()
@schema_from_inis(files=["config.default.ini"])
def main(**kwargs):
    pprint.pprint(kwargs)

if __name__ == "__main__":
    main()
```

This will result in:

```sh
python __main__.py --help

Usage: __main__.py [OPTIONS]

Options:
  --initialized_to_none TEXT
  --test1.multiline_commented TEXT
                                  Wow, multilines
                                  Talk about eye candy  [default: value1]
  --test1.typed INTEGER            [default: 2]
  --test1.inferred / --no-test1.inferred
                                   [default: test1.inferred]
  --test2.inline_commented TEXT    [default: value1]
  --test2.after_paragraph TEXT    This is a comment
  --help                          Show this message and exit.
```

and

````
python __main__.py

{'initialized_to_none': None,
 'required_parameter_overriden': 'not required',
 'test1__inferred': True,
 'test1__multiline_commented': 'value1',
 'test1__typed': 2,
 'test2__after_paragraph': None,
 'test2__inline_commented': 'value1'}
 ```

You can of course override using the options:

```sh
python TODO.py --test2.inline_commented "HEY"

{'initialized_to_none': None,
 'required_parameter_overriden': 'not required',
 'test1__inferred': True,
 'test1__multiline_commented': 'value1',
 'test1__typed': 2,
 'test2__after_paragraph': None,
 'test2__inline_commented': 'HEY'}
````

# Rationale

Having setting files allow for separation of concerns and for users to know what they are expected to tweak and modify. This library is here to provide schema specifications of settings.

# TODO

- [ ] Integration with click types, like click.choices and click.intrange
- [ ] Test suite
