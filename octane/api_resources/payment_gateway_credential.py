from __future__ import absolute_import, division, print_function

from octane.api_resources.abstract import (
    CreateableAPIResource,
)


class PaymentGatewayCredential(CreateableAPIResource):
    OBJECT_NAME = "payment_gateway_credential"

    @classmethod
    def retrieve(cls, id, api_key=None, **params):
        raise NotImplementedError(
            "Can't retrieve a payment_gateway_credential."
        )
