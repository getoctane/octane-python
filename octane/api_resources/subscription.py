from __future__ import absolute_import, division, print_function

from octane.api_resources.abstract import CreateableAPIResource


class Subscription(CreateableAPIResource):
    OBJECT_NAME = "subscription"

    @classmethod
    def create(cls, sid, **params):
        raise NotImplementedError(
            "Can't create a mapping without a customer name. "
            "Use customer.mappings.create()"
        )

    @classmethod
    def retrieve(cls, id, api_key=None, **params):
        raise NotImplementedError("Can't retrieve a subscription.")
