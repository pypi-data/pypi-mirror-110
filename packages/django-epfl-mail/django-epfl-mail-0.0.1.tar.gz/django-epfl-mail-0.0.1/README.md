django-epfl-mail
================

[![Build Status][github-actions-image]][github-actions-url]
[![Coverage Status][codecov-image]][codecov-url]
[![PyPI version][pypi-image]][pypi-url]
[![PyPI Python version][pypi-python-image]][pypi-url]

A Django application with templates for emails.

Requirements
------------

- Python 2.7, 3.5 or later
- Django 1.11, 2.2

Installation
------------

Installing from PyPI is as easy as doing:

```bash
pip install django-epfl-mail
```

Documentation
-------------

Add `'django_epflmail'` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = [
    ...
    'django_epflmail',
]
```

Example template:

```htmldjango
{% extends "epflmail/default.html" %}


{% block main %}
Example
{% endblock %}
```

[github-actions-image]: https://github.com/epfl-si/django-epfl-mail/workflows/Build/badge.svg?branch=main
[github-actions-url]: https://github.com/epfl-si/django-epfl-mail/actions

[codecov-image]:https://codecov.io/gh/epfl-si/django-epfl-mail/branch/main/graph/badge.svg
[codecov-url]:https://codecov.io/gh/epfl-si/django-epfl-mail

[pypi-python-image]: https://img.shields.io/pypi/pyversions/django-epfl-mail
[pypi-image]: https://img.shields.io/pypi/v/django-epfl-mail
[pypi-url]: https://pypi.org/project/django-epfl-mail/
