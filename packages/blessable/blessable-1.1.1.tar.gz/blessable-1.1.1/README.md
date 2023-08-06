# Blessable

Blessable is a simple library powered by the Blessed library. Blessable adds a simple markup language that has a similar syntax to HTML.

## Support

Through Blessed, Blessable supports almost all platforms:

 - Windows `NEW`
 - macOS
 - Linux
 - BSD

Please refer to the Blessed documentation for more information.

## Usage

First, install the package:

```python
pip install blessable # or python -m pip install blessable
```

Then, import the `blessable` module:

```python
from blessable import Blessable
```

Then, use `blessable` like this:

```python
blessable = Blessable()
print(blessable.bless('<green>Success</green> - <blue_on_white>Blessable has been installed!</blue_on_white>'))
```

Try it out!

### Blessable Markup Language

Moved to our [Wiki](https://github.com/fakerybakery/blessable/wiki/Documentation#blessable-markup-language).

## Supported Colors

[Supported colors have been moved to our Wiki](https://github.com/fakerybakery/blessable/wiki/Documentation#supported-colors).

## To Do

 - [ ] Support nested styling
 - [ ] Support escaping tags

## FAQs

Please see the [Wiki](https://github.com/fakerybakery/blessable/wiki) for FAQs, comparisons, and more.
