from __future__ import absolute_import, division, print_function
from octane.octane_object import OctaneObject

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

        def _add_params(obj, params):
            if isinstance(obj, OctaneObject):
                obj._retreieve_params = params
                return

            if isinstance(obj, list):
                for e in obj:
                    _add_params(e, params)

        _add_params(octane_object, params)

        return octane_object
