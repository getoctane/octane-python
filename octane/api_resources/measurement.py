from __future__ import absolute_import, division, print_function
from datetime import datetime

from octane.api_resources.abstract import CreateableAPIResource


class Measurement(
    CreateableAPIResource,
):
    OBJECT_NAME = "measurement"

    @classmethod
    def create(
        cls, api_key=None, idempotency_key=None, octane_version=None, **params
    ):
        if "time" not in params:
            params["time"] = datetime.utcnow().isoformat()

        return super(Measurement, cls).create(api_key=api_key, idempotency_key=idempotency_key, octane_version=octane_version, **params)