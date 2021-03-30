from __future__ import absolute_import, division, print_function

from octane import api_requestor, error, util, six
from octane.octane_object import OctaneObject
from octane.six.moves.urllib.parse import quote_plus


class APIResource(OctaneObject):
    @classmethod
    def retrieve(cls, name, api_key=None, **params):
        instance = cls(name, api_key, **params)
        instance.refresh()
        return instance

    def refresh(self):
        self.refresh_from(self.request("get", self.instance_url()))
        return self

    @classmethod
    def class_url(cls):
        if cls == APIResource:
            raise NotImplementedError(
                "APIResource is an abstract class.  You should perform "
                "actions on its subclasses (e.g. Charge, Customer)"
            )
        # Namespaces are separated in object names with periods (.) and in URLs
        # with forward slashes (/), so replace the former with the latter.
        base = cls.OBJECT_NAME.replace(".", "/")
        return "/%ss/" % (base,)

    def instance_url(self):
        name = self.get("name")

        if not isinstance(name, six.string_types):
            raise error.InvalidRequestError(
                "Could not determine which URL to request: %s instance "
                "has invalid ID: %r, %s. ID should be of type `str` (or"
                " `unicode`)" % (type(self).__name__, name, type(name)),
                "name",
            )

        name = util.utf8(name)
        base = self.class_url()
        extn = quote_plus(name)
        return "%s%s" % (base, extn)

    # The `method_` and `url_` arguments are suffixed with an underscore to
    # avoid conflicting with actual request parameters in `params`.
    @classmethod
    def _static_request(
        cls,
        method_,
        url_,
        api_key=None,
        idempotency_key=None,
        octane_version=None,
        **params
    ):
        requestor = api_requestor.APIRequestor(
            api_key, api_version=octane_version
        )
        headers = util.populate_headers(idempotency_key)
        response, api_key = requestor.request(method_, url_, params, headers)
        return util.convert_to_octane_object(response, api_key, octane_version)
