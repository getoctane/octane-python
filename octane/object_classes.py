from __future__ import absolute_import, division, print_function

from octane import api_resources


OBJECT_CLASSES = {
    # data structures
    api_resources.ListObject.OBJECT_NAME: api_resources.ListObject,
    # business objects
    api_resources.Customer.OBJECT_NAME: api_resources.Customer,
    api_resources.Mapping.OBJECT_NAME: api_resources.Mapping,
    api_resources.Measurement.OBJECT_NAME: api_resources.Measurement,
    api_resources.Meter.OBJECT_NAME: api_resources.Meter,
}
