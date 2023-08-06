# Charred

Very simple package with `is_ascii_char`, `is_same_char`, `is_string`, `is_unicode_char` and `repeat_char` methods.

I will probably add more later.

Install package:

```
pip install charred

# or pip3
```

Usage:

```
from charred import is_ascii_char, is_same_char, is_string, is_unicode_char, repeat_char

>>> is_ascii_char('$')
True
>>> is_ascii_char('£')
False

>>> is_same_char('FF')
True
>>> is_same_char('FD')
False

>>> is_string('F')
True
>>> is_string(1)
False

>>> is_unicode_char('£')
True
>>> is_unicode_char('F')
False

>>> repeat_char('F', 6)
FFFFFF
```
