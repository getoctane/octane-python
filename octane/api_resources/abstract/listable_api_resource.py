from __future__ import absolute_import, division, print_function

from octane import api_requestor, util
from octane.api_resources.abstract.api_resource import APIResource


class ListableAPIResource(APIResource):
    @classmethod
    def auto_paging_iter(cls, *args, **params):
        return cls.list(*args, **params).auto_paging_iter()

    @classmethod
    def list(cls, api_key=None, octane_version=None, **params):
        requestor = api_requestor.APIRequestor(
            api_key,
            api_base=cls.api_base(),
            api_version=octane_version,
        )
        url = cls.class_url()
        response, api_key = requestor.request("get", url, params)
        octane_object = util.convert_to_octane_object(
            response, api_key, octane_version
        )
        octane_object._retrieve_params = params
        return octane_object
