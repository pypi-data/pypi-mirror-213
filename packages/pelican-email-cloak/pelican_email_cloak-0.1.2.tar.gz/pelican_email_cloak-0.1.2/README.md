# E-mail Cloak: A Plugin for Pelican

[![PyPI Version](https://img.shields.io/pypi/v/pelican-email-cloak)](https://pypi.org/project/pelican-email-cloak/)
![License](https://img.shields.io/pypi/l/pelican-email-cloak?color=blue)

E-mail cloaking plugin for Pelican

## Installation

This plugin can be installed via:

    python -m pip install pelican-email-cloak

## Usage

To use this plugin, add the following to your `pelicanconf.py`:

```python
PLUGINS = [
    # ...
    'email_cloak',
    # ...
]
```

Pelican should automatically discover the plugin after installation under the namespace `pelican.plugins`.

E-mails in articles and pages will be cloaked.

## Changelog

-   0.0.1 up to 0.0.3: Initial release
    -   Version bumped to update PyPI description

## License

This project is licensed under the MIT license.
