# colorpie
Terminal color style handler.

### Installation:

```commandline
python -m pip install [--upgrade] colorpie
```

### Available tools:

```python

from colorpie import Style4Bit, COLORS, HIGHLIGHTS, ATTRIBUTES as ATTRS

style = Style4Bit(
    color=COLORS.RED,
    highlight=HIGHLIGHTS.BLACK,
    attributes=[ATTRS.BOLD, ATTRS.SLOW_BLINK]
)

if __name__ == '__main__':
    print(style.format('Hello, World!'))
```
