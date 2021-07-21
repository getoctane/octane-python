# Octane Python Library

[![Version](https://img.shields.io/pypi/v/octane.svg)](https://pypi.org/project/octane/)
[![GitHub Actions status](https://github.com/getoctane/octane-python/workflows/build/badge.svg)](https://github.com/getoctane/octane-python/actions?query=workflow%3Abuild+)

[![Octane](./octane.png)](https://www.getoctane.io/)

The **[Octane](https://www.getoctane.io/)** Python library provides programmatic access
to the Octane API for Python applications.

---

- [Getting started](#getting-started)
- [Example apps](#example-apps)
- [Making API calls](#making-api-calls)
    - [Customers API](#customers-api)
        - [Example: Creating a new customer](#example-creating-a-new-customer)
        - [Example: Subscribe a customer to a price plan](#example-subscribe-a-customer-to-a-price-plan)
    - [Meters API](#meters-api)
        - [Example: Creating a new meter](#example-creating-a-new-meter)
    - [Price Plans API](#price-plans-api)
        - [Example: Creating a new price plan](#example-creating-a-new-price-plan)
    - [Measurements API](#measurements-api)
        - [Example: Sending a measurement](#example-sending-a-measurement)
- [Development](#development)
- [Contributing](#contributing)

## Getting started

First, install the package (`octane`):

```bash
pip install --upgrade octane
```

Next, obtain an API key from within the [Octane portal](http://cloud.getoctane.io/), and set it in your environment:

```shell
export OCTANE_API_KEY="<insert_octane_api_key_here>"
```

Then, from within your application, import the module:

```python
import os, octane
octane.api_key = os.environ.get('OCTANE_API_KEY')
```

## Example apps

The following demo applications found in the [examples/](./examples/) directory display
how to use the Octane Python library in real-world settings:

- [antler-db-cloud-shop](examples/antler-db-cloud-shop/) - Enable your customers to self-service various cloud resources
- [customer-hours-tracker](./examples/customer-hours-tracker/) - Track hours spent working on freelance projects

## Making API calls

The `TODO` class provides programmatic access to the Octane API.

TODO

### Customers API

TODO provides the ability to
make calls to the Octane Customers API.

#### Example: Creating a new customer

```python
TODO
```

#### Example: Subscribe a customer to a price plan

```python
TODO
```

### Meters API

TODO provides the ability to
make calls to the Octane Meters API.

#### Example: Creating a new meter

```python
TODO
```

### Price Plans API

TODO provides the ability to
make calls to the Octane Price Plans API.

#### Example: Creating a new price plan

```python
TODO
```

### Measurements API

TODO provides the ability to
make calls to the Octane Measurements API.

#### Example: Sending a measurement

```python
TODO
```

## Development

Run the following command to set up the development virtualenv:

```sh
make
```

Run all tests on all supported Python versions:

```sh
make test
```

Run all tests for a specific Python version (modify `-e` according to your Python target):

```sh
TOX_ARGS="-e py37" make test
```

Run all tests in a single file:

```sh
TOX_ARGS="-e py37 -- tests/api_resources/abstract/test_updateable_api_resource.py" make test
```

Run a single test suite:

```sh
TOX_ARGS="-e py37 -- tests/api_resources/abstract/test_updateable_api_resource.py::TestUpdateableAPIResource" make test
```

Run a single test:

```sh
TOX_ARGS="-e py37 -- tests/api_resources/abstract/test_updateable_api_resource.py::TestUpdateableAPIResource::test_save" make test
```

Run the linter with:

```sh
make lint
```

The library uses [Black][black] for code formatting. Code must be formatted
with Black before PRs are submitted, otherwise CI will fail. Run the formatter
with:

```sh
make fmt
```

[black]: https://github.com/ambv/black
[octane-mock]: https://github.com/octane/octane-mock

## Contributing

Contributions are welcome!

Prior to submitting a
[pull request](https://github.com/getoctane/octane-python/pulls), please
check the list of [open issues](https://github.com/getoctane/octane-python/issues).
If there is not an existing issue related to your changes, please open a
new issue to first discuss your thoughts with the project maintainers.
