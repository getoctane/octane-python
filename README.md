# Octane Python Library

TODO
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

TODO

## Contributing

Contributions are welcome!

Prior to submitting a
[pull request](https://github.com/getoctane/octane-python/pulls), please
check the list of [open issues](https://github.com/getoctane/octane-python/issues).
If there is not an existing issue related to your changes, please open a
new issue to first discuss your thoughts with the project maintainers.
