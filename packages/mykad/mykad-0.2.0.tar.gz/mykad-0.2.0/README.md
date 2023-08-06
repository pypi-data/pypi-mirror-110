# MyKad

A Python package to check if a MyKad number is valid and gets information such as the birthdate, state of birth, etc.

**Warning**: This is still in pre-release so expect API breakages between versions.

## The `MyKad` class

```python
from mykad.mykad import MyKad

mykad = MyKad(MYKAD_NUMBER)
```

The following methods are included in the `MyKad` class:

| Method                     | Comment                                                 | Example return value |
|----------------------------|---------------------------------------------------------|----------------------|
| `get_unformatted()`        | Gets the unformatted MyKad string.                      | `'990111431234'`     |
| `get_formatted()`          | Gets the formatted MyKad string.                        | `'990111-43-1234'`   |
| `get_birth_year()`         | Gets the birthyear of the MyKad holder in YY format.    | `'99'`               |
| `get_pretty_birth_year()`  | Gets the birthyear of the MyKad holder in YYYY format.  | `'1999'`             |
| `get_birth_month()`        | Gets the birth month of the MyKad holder in MM format.  | `'01'`               |
| `get_pretty_birth_month()` | Gets the birth month of the MyKad holder in English.    | `'January'`          |
| `get_birth_day()`          | Gets the day of birth of the MyKad holder in DD format. | `'11'`               |
| `get_pretty_birth_day()`   | Gets the day of birth of the MyKad holder in English.   | `'Monday'`           |
| `get_birthplace_code()`    | Gets the birthplace code of the MyKad holder.           | `'43'`               |
| `get_birthplace()`         | Gets the birthplace of the MyKad holder.                | `'Selangor'`         |
| `is_male()`                | Checks if the MyKad holder is a male.                   | `False`              |
| `is_female()`              | Checks if the MyKad holder is a female.                 | `True`               |
| `get_gender()`             | Gets the gender of the MyKad holder.                    | `'Female'`           |

## Included utility functions

The following utility functions are included under `mykad.utils`:

| Method                    | Comment                                                      | Example return value |
|---------------------------|--------------------------------------------------------------|----------------------|
| `is_mykad_valid`          | Checks if a MyKad is valid.                                  | `False`              |
| `get_state_abbreviation`  | Gets the state abbreviation                                  | `'SGR'`              |
