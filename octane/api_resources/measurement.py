from __future__ import absolute_import, division, print_function

from octane.api_resources.abstract import CreateableAPIResource


class Measurement(
    CreateableAPIResource,
):
    OBJECT_NAME = "measurement"
