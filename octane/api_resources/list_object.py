from __future__ import absolute_import, division, print_function

from octane import api_requestor, six, util
from octane.octane_object import OctaneObject

from octane.six.moves.urllib.parse import quote_plus


class ListObject(OctaneObject):
    OBJECT_NAME = "list"

    def list(self, api_key=None, octane_version=None, **params):
        octane_object = self._request(
            "get",
            self.get("url"),
            api_key=api_key,
            octane_version=octane_version,
            **params
        )
        octane_object._retrieve_params = params
        return octane_object

    def create(
        self, api_key=None, idempotency_key=None, octane_version=None, **params
    ):
        return self._request(
            "post",
            self.get("url"),
            api_key=api_key,
            idempotency_key=idempotency_key,
            octane_version=octane_version,
            **params
        )

    def retrieve(self, name, api_key=None, octane_version=None, **params):
        url = "%s/%s" % (self.get("url"), quote_plus(util.utf8(name)))
        return self._request(
            "get",
            url,
            api_key=api_key,
            octane_version=octane_version,
            **params
        )

    def _request(
        self,
        method_,
        url_,
        api_key=None,
        idempotency_key=None,
        octane_version=None,
        **params
    ):
        api_key = api_key or self.api_key
        octane_version = octane_version or self.octane_version

        requestor = api_requestor.APIRequestor(
            api_key, api_version=octane_version
        )
        headers = util.populate_headers(idempotency_key)
        response, api_key = requestor.request(method_, url_, params, headers)
        octane_object = util.convert_to_octane_object(
            response, api_key, octane_version
        )
        return octane_object

    def __getitem__(self, k):
        if isinstance(k, six.string_types):
            return super(ListObject, self).__getitem__(k)
        else:
            raise KeyError(
                "You tried to access the %s index, but ListObject types only "
                "support string keys. (HINT: List calls return an object with "
                "a 'data' (which is the data array). You likely want to call "
                ".data[%s])" % (repr(k), repr(k))
            )

    def __iter__(self):
        return getattr(self, "data", []).__iter__()

    def __len__(self):
        return getattr(self, "data", []).__len__()

    def __reversed__(self):
        return getattr(self, "data", []).__reversed__()

    def auto_paging_iter(self):
        page = self

        while True:
            if (
                "ending_before" in self._retrieve_params
                and "starting_after" not in self._retrieve_params
            ):
                for item in reversed(page):
                    yield item
                page = page.previous_page()
            else:
                for item in page:
                    yield item
                page = page.next_page()

            if page.is_empty:
                break

    @classmethod
    def empty_list(cls, api_key=None, octane_version=None):
        return cls.construct_from(
            {"data": []},
            key=api_key,
            octane_version=octane_version,
            last_response=None,
        )

    @property
    def is_empty(self):
        return not self.data

    def next_page(self, api_key=None, octane_version=None, **params):
        if not self.has_more:
            return self.empty_list(
                api_key=api_key,
                octane_version=octane_version,
            )

        last_id = self.data[-1].name

        params_with_filters = self._retrieve_params.copy()
        params_with_filters.update({"starting_after": last_id})
        params_with_filters.update(params)

        return self.list(
            api_key=api_key,
            octane_version=octane_version,
            **params_with_filters
        )

    def previous_page(self, api_key=None, octane_version=None, **params):
        if not self.has_more:
            return self.empty_list(
                api_key=api_key,
                octane_version=octane_version,
            )

        first_id = self.data[0].name

        params_with_filters = self._retrieve_params.copy()
        params_with_filters.update({"ending_before": first_id})
        params_with_filters.update(params)

        return self.list(
            api_key=api_key,
            octane_version=octane_version,
            **params_with_filters
        )
