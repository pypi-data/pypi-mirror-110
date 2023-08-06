# Tuneup Technology App Python Client Library

The Python client library for the Tuneup Technology App.

[![Build Status](https://github.com/tuneuptechnology/tuneuptechnology-python/workflows/build/badge.svg)](https://github.com/tuneuptechnology/tuneuptechnology-python/actions)
[![Coverage Status](https://coveralls.io/repos/github/tuneuptechnology/tuneuptechnology-python/badge.svg?branch=main)](https://coveralls.io/github/tuneuptechnology/tuneuptechnology-python?branch=main)
[![PyPi](https://img.shields.io/pypi/v/tuneuptechnology-python)](https://pypi.org/project/tuneuptechnology-python)
[![Licence](https://img.shields.io/github/license/tuneuptechnology/tuneuptechnology-python)](LICENSE)

This library allows you to interact with the customers, tickets, inventory, and locations objects without needing to do the hard work of binding your calls and data to endpoints. Simply call an action such as `Customer.create` and pass some data and let the library do the rest.

## Install

```bash
# Install client library
pip3 install tuneuptechnology

# Install locally
make install

# Get Makefile help
make help
```

## Example

```python
import os

import tuneuptechnology

API_EMAIL = os.getenv('API_EMAIL')
API_KEY = os.getenv('API_KEY')

client = tuneuptechnology.Client(API_EMAIL, API_KEY)

customer = client.Customers.create(
    {
        'firstname': 'Jake',
        'lastname': 'Peralta',
        'email': 'jake@example.com',
        'phone': '8015551234',
        'user_id': 1,
        'notes': 'Believes he is a good detective.',
        'location_id': 2,
    }
)

print(customer)
```

Other examples can be found in the `/examples` directory. Alter according to your needs.

## Usage

```bash
API_EMAIL=email@example.com API_KEY=123... venv/bin/python create_customer.py
```

## Documentation

Up-to-date API documentation can be [found here](https://app.tuneuptechnology.com/docs/api).

## Development

```bash
# Lint the project
make lint

# Run tests
API_EMAIL=email@example.com API_KEY=123... make test

# Run test coverage
API_EMAIL=email@example.com API_KEY=123... make coverage
```

## Releasing

As a separate PR from the feature/bug PR:

1. Update the Version constant in `client.py` & `setup.py`
1. Update `CHANGELOG`
1. Create a GitHub tag with proper Python version semantics (eg: v1.0.0)
1. Publish to PyPI
