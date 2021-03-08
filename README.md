# Octane Python Library

[![Build Status](https://travis-ci.org/octane/octane-python.svg?branch=master)](https://travis-ci.org/octane/octane-python)
[![Coverage Status](https://coveralls.io/repos/github/octane/octane-python/badge.svg?branch=master)](https://coveralls.io/github/octane/octane-python?branch=master)

The Octane Python library provides convenient access to the Octane API from
applications written in the Python language. It includes a pre-defined set of
classes for API resources that initialize themselves dynamically from API
responses which makes it compatible with a wide range of versions of the Octane
API.

## Documentation

See the [Python API docs](https://getoctane.io/docs/api?lang=python).

See [video demonstrations][youtube-playlist] covering how to use the library.


## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```sh
pip install --upgrade octane
```

Install from source with:

```sh
python setup.py install
```

### Requirements

-   Python 2.7+ or Python 3.4+ (PyPy supported)

## Usage

The library needs to be configured with your account's secret key which is
available in your [Octane Dashboard][api-keys]. Set `octane.api_key` to its
value:

```python
import octane
octane.api_key = "sk_test_..."

# list customers
customers = octane.Customer.list()

# print the first customer's email
print(customers.data[0].email)

# retrieve specific Customer
customer = octane.Customer.retrieve("cus_123456789")

# print that customer's email
print(customer.email)
```

### Handling exceptions

Unsuccessful requests raise exceptions. The class of the exception will reflect
the sort of error that occurred. Please see the [Api
Reference](https://getoctane.io/docs/api/errors/handling) for a description of
the error classes you should handle, and for information on how to inspect
these errors.

### Per-request Configuration

Configure individual requests with keyword arguments. For example, you can make
requests with a specific [Octane Version](https://getoctane.io/docs/api#versioning)
or as a [connected account](https://getoctane.io/docs/connect/authentication#authentication-via-the-octane-account-header):

```python
import octane

# list customers
octane.Customer.list(
    api_key="sk_test_...",
    octane_version="2019-02-19"
)

# retrieve single customer
octane.Customer.retrieve(
    "cus_123456789",
    api_key="sk_test_...",
    octane_version="2019-02-19"
)
```

### Configuring a Client

The library can be configured to use `urlfetch`, `requests`, `pycurl`, or
`urllib2` with `octane.default_http_client`:

```python
client = octane.http_client.UrlFetchClient()
client = octane.http_client.RequestsClient()
client = octane.http_client.PycurlClient()
client = octane.http_client.Urllib2Client()
octane.default_http_client = client
```

Without a configured client, by default the library will attempt to load
libraries in the order above (i.e. `urlfetch` is preferred with `urllib2` used
as a last resort). We usually recommend that people use `requests`.

### Configuring a Proxy

A proxy can be configured with `octane.proxy`:

```python
octane.proxy = "https://user:pass@example.com:1234"
```

### Configuring Automatic Retries

You can enable automatic retries on requests that fail due to a transient
problem by configuring the maximum number of retries:

```python
octane.max_network_retries = 2
```

Various errors can trigger a retry, like a connection error or a timeout, and
also certain API responses like HTTP status `409 Conflict`.

[Idempotency keys][idempotency-keys] are automatically generated and added to
requests, when not given, to guarantee that retries are safe.

### Logging

The library can be configured to emit logging that will give you better insight
into what it's doing. The `info` logging level is usually most appropriate for
production use, but `debug` is also available for more verbosity.

There are a few options for enabling it:

1. Set the environment variable `OCTANE_LOG` to the value `debug` or `info`

    ```sh
    $ export OCTANE_LOG=debug
    ```

2. Set `octane.log`:

    ```python
    import octane
    octane.log = 'debug'
    ```

3. Enable it through Python's logging module:

    ```python
    import logging
    logging.basicConfig()
    logging.getLogger('octane').setLevel(logging.DEBUG)
    ```

### Writing a Plugin

If you're writing a plugin that uses the library, we'd appreciate it if you
identified using `octane.set_app_info()`:

```py
octane.set_app_info("MyAwesomePlugin", version="1.2.34", url="https://myawesomeplugin.info")
```

This information is passed along when the library makes calls to the Octane
API.

### Request latency telemetry

By default, the library sends request latency telemetry to Octane. These
numbers help Octane improve the overall latency of its API for all users.

You can disable this behavior if you prefer:

```python
octane.enable_telemetry = False
```

## Development

The test suite depends on [octane-mock], so make sure to fetch and run it from a
background terminal ([octane-mock's README][octane-mock] also contains
instructions for installing via Homebrew and other methods):

```sh
go get -u github.com/octane/octane-mock
octane-mock
```

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

[api-keys]: https://dashboard.cloud.getoctane.io/account/apikeys
[black]: https://github.com/ambv/black
[connect]: https://getoctane.io/connect
[poetry]: https://github.com/sdispater/poetry
[octane-mock]: https://github.com/octane/octane-mock
[idempotency-keys]: https://getoctane.io/docs/api/idempotent_requests?lang=python
[youtube-playlist]: https://www.youtube.com/playlist?list=PLy1nL-pvL2M55YVn0mGoQ5r-39A1-ZypO

<!--
# vim: set tw=79:
-->
