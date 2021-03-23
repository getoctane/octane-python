from __future__ import absolute_import, division, print_function
from tests.api_resources.test_octane_resource import TestOctaneResource

import octane


class TestOctaneCustomer(TestOctaneResource):
    RESOURCE_CLASS = octane.Customer
    BASE_URL = "/customers"

    def test_is_listable(self, request_mock):
        super()._is_listable(request_mock)

    def test_is_retrievable(self, request_mock):
        super()._is_retrievable(request_mock)

    def test_is_creatable(self, request_mock):
        super()._is_creatable(request_mock)

    def test_is_saveable(self, request_mock):
        super()._is_saveable(request_mock)

    def test_is_modifiable(self, request_mock):
        super()._is_modifiable(request_mock)

    def test_is_deletable(self, request_mock):
        super()._is_deletable(request_mock)

    def test_can_delete(self, request_mock):
        super()._can_delete(request_mock)
