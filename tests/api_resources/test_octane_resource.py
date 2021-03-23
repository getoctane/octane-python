from __future__ import absolute_import, division, print_function


class ImproperTestObject(Exception):
    pass


class TestOctaneResource(object):
    TEST_RESOURCE_ID = "abc123"

    def _is_listable(self, request_mock):
        method = "get"
        url = self.BASE_URL
        request_mock.stub_request(
            method,
            url,
            {
                "object": "list",
                "data": [
                    {
                        "object": self.RESOURCE_CLASS.OBJECT_NAME,
                        "name": self.TEST_RESOURCE_ID,
                    }
                ],
            },
        )

        resources = self.RESOURCE_CLASS.list()

        request_mock.assert_requested(method, url)
        assert isinstance(resources.data, list)
        assert isinstance(resources.data[0], self.RESOURCE_CLASS)

    def _is_retrievable(self, request_mock):
        method = "get"
        url = "%s/%s" % (self.BASE_URL, self.TEST_RESOURCE_ID)
        request_mock.stub_request(
            method,
            url,
            {
                "object": self.RESOURCE_CLASS.OBJECT_NAME,
                "name": self.TEST_RESOURCE_ID,
            },
        )

        resource = self.RESOURCE_CLASS.retrieve(self.TEST_RESOURCE_ID)

        request_mock.assert_requested(method, url)
        assert isinstance(resource, self.RESOURCE_CLASS)

    def _is_creatable(self, request_mock):
        method = "post"
        url = self.BASE_URL
        request_mock.stub_request(
            method,
            url,
            {
                "object": self.RESOURCE_CLASS.OBJECT_NAME,
                "name": self.TEST_RESOURCE_ID,
            },
        )

        resource = self.RESOURCE_CLASS.create(name=self.TEST_RESOURCE_ID)

        request_mock.assert_requested("post", self.BASE_URL)
        assert isinstance(resource, self.RESOURCE_CLASS)

    def _is_saveable(self, request_mock):
        method = "put"
        url = "%s/%s" % (self.BASE_URL, self.TEST_RESOURCE_ID)
        request_mock.stub_request(
            method,
            url,
            {
                "object": self.RESOURCE_CLASS.OBJECT_NAME,
                "name": self.TEST_RESOURCE_ID,
            },
        )

        request_mock.stub_request(
            "get",
            "%s/%s" % (self.BASE_URL, self.TEST_RESOURCE_ID),
            {
                "object": self.RESOURCE_CLASS.OBJECT_NAME,
                "name": self.TEST_RESOURCE_ID,
                "key": "old_value",
            },
        )

        resource = self.RESOURCE_CLASS.retrieve(self.TEST_RESOURCE_ID)
        resource.key = "new_value"
        resource.save()

        request_mock.assert_requested(method, url)

    def _is_modifiable(self, request_mock):
        method = "put"
        url = "%s/%s" % (self.BASE_URL, self.TEST_RESOURCE_ID)
        request_mock.stub_request(
            method,
            url,
            {
                "object": self.RESOURCE_CLASS.OBJECT_NAME,
                "name": self.TEST_RESOURCE_ID,
            },
        )

        request_mock.stub_request(
            "get",
            "%s/%s" % (self.BASE_URL, self.TEST_RESOURCE_ID),
            {
                "object": self.RESOURCE_CLASS.OBJECT_NAME,
                "name": self.TEST_RESOURCE_ID,
            },
        )

        _ = self.RESOURCE_CLASS.modify(
            self.TEST_RESOURCE_ID, metadata={"key": "value"}
        )

        request_mock.assert_requested(method, url)

    def _is_deletable(self, request_mock):
        method = "delete"
        url = "%s/%s" % (self.BASE_URL, self.TEST_RESOURCE_ID)
        request_mock.stub_request(method, url)

        request_mock.stub_request(
            "get",
            "%s/%s" % (self.BASE_URL, self.TEST_RESOURCE_ID),
            {
                "object": self.RESOURCE_CLASS.OBJECT_NAME,
                "name": self.TEST_RESOURCE_ID,
            },
        )

        resource = self.RESOURCE_CLASS.retrieve(self.TEST_RESOURCE_ID)
        resource.delete()

        request_mock.assert_requested(method, url)

    def _can_delete(self, request_mock):
        method = "delete"
        url = "%s/%s" % (self.BASE_URL, self.TEST_RESOURCE_ID)
        request_mock.stub_request(method, url)

        self.RESOURCE_CLASS.delete(self.TEST_RESOURCE_ID)

        request_mock.assert_requested(method, url)
