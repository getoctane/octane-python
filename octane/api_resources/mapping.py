from __future__ import absolute_import, division, print_function

from octane.api_resources.abstract import (
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
)


class Mapping(
    CreateableAPIResource, ListableAPIResource, DeletableAPIResource
):
    OBJECT_NAME = "mapping"

    @classmethod
    def create(cls, sid, **params):
        raise NotImplementedError(
            "Can't create a mapping without a customer name. "
            "Use customer.mappings.create()"
        )

    @classmethod
    def list(cls, sid, **params):
        raise NotImplementedError(
            "Can't list mappings without a customer name. "
            "Use customer.mappings.list()"
        )

    @classmethod
    def retrieve(cls, id, api_key=None, **params):
        raise NotImplementedError("Can't retrieve a mapping.")
