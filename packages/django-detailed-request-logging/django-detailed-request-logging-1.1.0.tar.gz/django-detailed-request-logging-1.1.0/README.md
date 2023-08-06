[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# django-detailed-request-logging

## Releases

This project follows the [semantic versioning specification](https://semver.org/) for its releases.

## Development

### Requirements

- Python >=3.7
- Django >=3.2
- django-rest-framework >=3.12

### Setup

- Create and activate a python3 venv.
- Install the library in the editable mode `pip install -e .[test]`
- Install dev requirements `pip install -r requirements-dev.txt`.
- Install git hooks to automatically format code using black with `pre-commit install`

## Installation

### From git in `requirements.txt`

To install this package from this git repository, add the `django-detailed-request-logging` package to the `requirements.txt` file.

To use it, add the following entry to `MIDDLEWARE` inside of your `settings.py` file:

```python
MIDDLEWARE = [
    ...,
    "django_detailed_request_logging.middleware.LoggingMiddleware",
]
```

Then, add a new entry `LOGGING_REQUEST_MIDDLEWARE` to your `settings.py` file, changing the value of `apps` to the
names of the apps you want to log requests on and changing the value of `skip_methods` to include all HTTP methods
you do **NOT** want to get logged:

```python
LOGGING_REQUEST_MIDDLEWARE = {
    "apps": ("projects",),
    "skip_methods": ("OPTIONS",),
}
```
