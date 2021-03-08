from __future__ import absolute_import, division, print_function

from octane.util import merge_dicts
from octane.octane_object import OctaneObject


class ErrorObject(OctaneObject):
    def refresh_from(
        self,
        values,
        api_key=None,
        partial=False,
        octane_version=None,
        last_response=None,
    ):
        # Unlike most other API resources, the API will omit attributes in
        # error objects when they have a null value. We manually set default
        # values here to facilitate generic error handling.
        values = merge_dicts(
            {
                "charge": None,
                "code": None,
                "decline_code": None,
                "doc_url": None,
                "message": None,
                "param": None,
                "payment_intent": None,
                "payment_method": None,
                "setup_intent": None,
                "source": None,
                "type": None,
            },
            values,
        )
        return super(ErrorObject, self).refresh_from(
            values,
            api_key,
            partial,
            octane_version,
            last_response,
        )
