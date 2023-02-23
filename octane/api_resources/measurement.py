from __future__ import absolute_import, division, print_function

from datetime import datetime

from octane.api_resources.abstract import CreateableAPIResource
from octane import api_requestor, util


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

        return super(Measurement, cls).create(
            api_key=api_key,
            idempotency_key=idempotency_key,
            octane_version=octane_version,
            **params
        )

    @classmethod
    def create_multi(
        cls,
        api_key=None,
        idempotency_key=None,
        octane_version=None,
        measurements=[],
    ):
        now = datetime.utcnow().isoformat()
        for measurement in measurements:
            if "time" not in measurement:
                measurement["time"] = now
        requestor = api_requestor.APIRequestor(
            api_key, api_version=octane_version
        )
        url = cls.class_url() + "multi"
        headers = util.populate_headers(idempotency_key)
        response, api_key = requestor.request(
            "post", url, measurements, headers
        )
        return util.convert_to_octane_object(response, api_key, octane_version)
