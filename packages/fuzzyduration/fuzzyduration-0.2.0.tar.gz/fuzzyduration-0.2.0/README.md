# Fuzzy Duration

A simple package to convert a number of seconds to the approximate duration of the largest time unit.

## install

```
python3 -m pip install fuzzyduration --user
```

## Usage

```python
from fuzzyduration import fuzzyDuration

secs = 60 * 60 * 24 * 1 + 1234

result = fuzzyDuration(secs)

print(result) # "1 day"

secs = secs * 8 * 2

print(result) # "2 weeks"

secs = secs * 60

print(result) # "2 years"
```
