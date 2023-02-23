from __future__ import absolute_import, division, print_function

from octane.api_resources.abstract import CreateableAPIResource
from octane.api_resources.abstract import DeletableAPIResource
from octane.api_resources.abstract import ListableAPIResource
from octane.api_resources.abstract import UpdateableAPIResource


class PricePlan(
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
):
    OBJECT_NAME = "price_plan"
