from __future__ import absolute_import, division, print_function

import atexit
import os
import sys
from distutils.version import StrictVersion

import pytest

import octane
from octane.six.moves.urllib.request import urlopen
from octane.six.moves.urllib.error import HTTPError

from tests.request_mock import RequestMock
from tests.octane_mock import OctaneMock


# When changing this number, don't forget to change it in `.travis.yml` too.
MOCK_MINIMUM_VERSION = "1.0.0"

# Starts octane-mock if an OpenAPI spec override is found in `openapi/`, and
# otherwise fall back to `OCTANE_MOCK_PORT` or 12111.
if OctaneMock.start():
    MOCK_PORT = OctaneMock.port()
else:
    MOCK_PORT = os.environ.get("OCTANE_MOCK_PORT", 12111)


@atexit.register
def stop_octane_mock():
    OctaneMock.stop()


def pytest_configure(config):
    if not config.getoption("--nomock"):
        try:
            resp = urlopen("http://localhost:%s/" % MOCK_PORT)
            info = resp.info()
            version = info.get("Octane-Mock-Version")
            if version != "master" and StrictVersion(version) < StrictVersion(
                MOCK_MINIMUM_VERSION
            ):
                sys.exit(
                    "Your version of octane-mock (%s) is too old. The minimum "
                    "version to run this test suite is %s. Please "
                    "see its repository for upgrade instructions."
                    % (version, MOCK_MINIMUM_VERSION)
                )

        except HTTPError as e:
            info = e.info()
        except Exception:
            sys.exit(
                "Couldn't reach octane-mock at `localhost:%s`. Is "
                "it running? Please see README for setup instructions."
                % MOCK_PORT
            )


def pytest_addoption(parser):
    parser.addoption(
        "--nomock",
        action="store_true",
        help="only run tests that don't need octane-mock",
    )


def pytest_runtest_setup(item):
    if "request_mock" in item.fixturenames and item.config.getoption(
        "--nomock"
    ):
        pytest.skip(
            "run octane-mock locally and remove --nomock flag to run skipped tests"
        )


@pytest.fixture(autouse=True)
def setup_octane():
    orig_attrs = {
        "api_base": octane.api_base,
        "api_key": octane.api_key,
        "client_id": octane.client_id,
        "default_http_client": octane.default_http_client,
    }
    http_client = octane.http_client.new_default_http_client()
    octane.api_base = "http://localhost:%s" % MOCK_PORT
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
