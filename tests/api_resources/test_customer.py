from __future__ import absolute_import, division, print_function

import octane

BASE_URL = "/v1/customers"
TEST_RESOURCE_ID = "customer_123"


class TestCustomer(object):
    def test_is_listable(self, request_mock):
        resources = octane.Customer.list()
        request_mock.assert_requested("get", BASE_URL)
        assert isinstance(resources.data, list)
        assert isinstance(resources.data[0], octane.Customer)

    def test_is_retrievable(self, request_mock):
        resource = octane.Customer.retrieve(TEST_RESOURCE_ID)
        request_mock.assert_requested(
            "get",
            "%s/%s" % (BASE_URL, TEST_RESOURCE_ID),
        )
        assert isinstance(resource, octane.Customer)

    def test_is_creatable(self, request_mock):
        resource = octane.Customer.create()
        request_mock.assert_requested("post", BASE_URL)
        assert isinstance(resource, octane.Customer)

    def test_is_saveable(self, request_mock):
        resource = octane.Customer.retrieve(TEST_RESOURCE_ID)
        resource.metadata["key"] = "value"
        resource.save()
        request_mock.assert_requested(
            "post",
            "%s/%s" % (BASE_URL, TEST_RESOURCE_ID),
        )

    def test_is_modifiable(self, request_mock):
        resource = octane.Customer.modify(
            TEST_RESOURCE_ID, metadata={"key": "value"}
        )
        request_mock.assert_requested(
            "post",
            "%s/%s" % (BASE_URL, TEST_RESOURCE_ID),
        )
        assert isinstance(resource, octane.Customer)

    def test_is_deletable(self, request_mock):
        resource = octane.Customer.retrieve(TEST_RESOURCE_ID)
        resource.delete()
        request_mock.assert_requested(
            "delete",
            "%s/%s" % (BASE_URL, TEST_RESOURCE_ID),
        )
        assert resource.deleted is True

    def test_can_delete(self, request_mock):
        resource = octane.Customer.delete(TEST_RESOURCE_ID)
        request_mock.assert_requested(
            "delete",
            "%s/%s" % (BASE_URL, TEST_RESOURCE_ID),
        )
        assert resource.deleted is True
