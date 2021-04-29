from __future__ import absolute_import, division, print_function

from octane import api_resources


OBJECT_CLASSES = {
    # data structures
    api_resources.ListObject.OBJECT_NAME: api_resources.ListObject,
    # business objects
    api_resources.Customer.OBJECT_NAME: api_resources.Customer,
    api_resources.Mapping.OBJECT_NAME: api_resources.Mapping,
    api_resources.PaymentGatewayCredential.OBJECT_NAME: api_resources.PaymentGatewayCredential,
    api_resources.Measurement.OBJECT_NAME: api_resources.Measurement,
    api_resources.Meter.OBJECT_NAME: api_resources.Meter,
    api_resources.PricePlan.OBJECT_NAME: api_resources.PricePlan,
    api_resources.PriceList.OBJECT_NAME: api_resources.PriceList,
    api_resources.Subscription.OBJECT_NAME: api_resources.Subscription,
}
