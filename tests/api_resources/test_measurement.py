from __future__ import absolute_import, division, print_function

import octane

BASE_URL = "/measurements"
TEST_RESOURCE_ID = "measurement_123"


class TestMeasurement(object):
    def test_is_creatable(self, request_mock):
        _ = octane.Measurement.create()
        request_mock.assert_requested("post", BASE_URL)
