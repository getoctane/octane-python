from __future__ import absolute_import, division, print_function

from octane import util
from octane.api_resources.abstract import (
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
)
from octane.api_resources.customer import Customer
from octane.six.moves.urllib.parse import quote_plus


class Mapping(
    CreateableAPIResource, ListableAPIResource, DeletableAPIResource
):
    OBJECT_NAME = "customer_mapping"

    def instance_url(self):
        customer = util.utf8(self.customer)
        base = Customer.class_url()
        cust_extn = quote_plus(customer)
        return "%s%s/mappings" % (base, cust_extn)

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
