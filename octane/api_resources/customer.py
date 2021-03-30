from __future__ import absolute_import, division, print_function
from octane.api_resources.abstract import nested_resource_class_methods

from octane.api_resources.abstract import CreateableAPIResource
from octane.api_resources.abstract import DeletableAPIResource
from octane.api_resources.abstract import ListableAPIResource
from octane.api_resources.abstract import UpdateableAPIResource


@nested_resource_class_methods(
    "mapping", operations=["create", "list", "delete"]
)
class Customer(
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
):
    OBJECT_NAME = "customer"
