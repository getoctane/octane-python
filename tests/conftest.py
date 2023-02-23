from __future__ import absolute_import, division, print_function

import pytest

import octane

from tests.request_mock import RequestMock


@pytest.fixture(autouse=True)
def setup_octane():
    orig_attrs = {
        "api_base": octane.api_base,
        "api_key": octane.api_key,
        "client_id": octane.client_id,
        "default_http_client": octane.default_http_client,
    }
    http_client = octane.http_client.new_default_http_client()
    octane.api_base = "http://localhost:8080"
    octane.api_key = "sk_test_123"
    octane.client_id = "ca_123"
    octane.default_http_client = http_client
    yield
    http_client.close()
    octane.api_base = orig_attrs["api_base"]
    octane.api_key = orig_attrs["api_key"]
    octane.client_id = orig_attrs["client_id"]
    octane.default_http_client = orig_attrs["default_http_client"]


@pytest.fixture
def request_mock(mocker):
    return RequestMock(mocker)
