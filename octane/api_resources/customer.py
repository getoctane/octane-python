from __future__ import absolute_import, division, print_function
from octane.api_resources.abstract.custom_method import custom_method
from octane.api_resources.abstract import nested_resource_class_methods

from octane import util
from octane.api_resources.abstract import CreateableAPIResource
from octane.api_resources.abstract import DeletableAPIResource
from octane.api_resources.abstract import ListableAPIResource
from octane.api_resources.abstract import UpdateableAPIResource


@nested_resource_class_methods("subscription", operations=["create"])
@nested_resource_class_methods(
    "mapping", operations=["create", "list", "delete"]
)
@nested_resource_class_methods(
    "payment_gateway_credential", operations=["create"]
)
@custom_method("revenue", "get")
@custom_method("usage", "get")
class Customer(
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
):
    OBJECT_NAME = "customer"

    def revenue(self, idempotency_key=None, **params):
        url = self.instance_url() + "/revenue"
        headers = util.populate_headers(idempotency_key)
        self.refresh_from(self.request("get", url, params, headers))
        return self

    def usage(self, idempotency_key=None, **params):
        url = self.instance_url() + "/usage"
        headers = util.populate_headers(idempotency_key)
        self.refresh_from(self.request("get", url, params, headers))
        return self
