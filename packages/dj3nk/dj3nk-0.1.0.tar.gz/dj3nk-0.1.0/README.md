# dj3nk

A simple natural key generator base on redis.

[History.](HISTORY.md)

## Install

```shell script
pip install dj3nk

```

## Examples

```python
# settings.py
NATURAL_KEY = {
    "increment_main_key": "a3:dj:nk",
    "random_bit_length": 16,
    "puzzle_count": 1000000,
    "rdb_conf_name": "default"
}

# models
from dj3nk import NKModel


class XXX(NKModel):
    ...

```
