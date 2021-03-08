from __future__ import absolute_import, division, print_function

from octane.api_resources.abstract.api_resource import APIResource
from octane import api_requestor, util


class CreateableAPIResource(APIResource):
    @classmethod
    def create(
        cls, api_key=None, idempotency_key=None, octane_version=None, **params
    ):
        requestor = api_requestor.APIRequestor(
            api_key, api_version=octane_version
        )
        url = cls.class_url()
        headers = util.populate_headers(idempotency_key)
        response, api_key = requestor.request("post", url, params, headers)

        return util.convert_to_octane_object(response, api_key, octane_version)
