import json
from typing import Iterator, List, Any

import requests
from pyneoncli.neonliterals import NeonAPIPaths
from pyneoncli.neonapiexceptions import NeonAPIException
from pyneoncli.neon import NeonObject, NeonProject


class Requester:

    def __init__(self, base_url: str = NeonAPIPaths.BASE_URL_V2.value, api_key: str = None):
        self._api_key = api_key
        self._base_url = base_url
        self._headers = {'Authorization': f"Bearer {self._api_key}",
                         'Content-Type': "application/json"}

    def request(self, method: str, operation: str, **kwargs):
        try:
            # print(self._headers)
            # print(kwargs)
            if operation.startswith("http"):
                path = operation
            else:
                path = f"{self._base_url}{operation}"
            r = requests.request(method, path, headers=self._headers, **kwargs)
            r.raise_for_status()
            return r.json()

        except requests.exceptions.HTTPError as err:
            raise NeonAPIException(path=path, method=method, err=err, text=r.text)

    def GET(self, operation: str, **kwargs):
        return self.request("GET", operation, **kwargs)

    def POST(self, operation: str, data: dict = None) -> dict:
        if data is None:
            data = dict()
        self._headers["Accept"] = "application/json"
        return self.request("POST", operation, data=json.dumps(data))

    def PUT(self, operation: str, **kwargs) -> dict:
        return self.request("PUT", operation, **kwargs)

    def DELETE(self, operation: str, **kwargs) -> dict:
        return self.request("DELETE", operation, **kwargs)

    def PATCH(self, operation: str, **kwargs) -> dict:
        return self.request("PATCH", operation, **kwargs)

    def HEAD(self, operation: str, **kwargs):
        return self.request("HEAD", operation, **kwargs)

    def create(self, path: str, payload: dict, selector: str = None) -> dict:
        data = self.POST(path, data=payload)
        if selector:
            item = data[selector]
        else:
            item = data
        return item

    def delete(self, path: str, selector: str = None) -> dict:
        data = self.DELETE(path)
        if selector:
            item = data[selector]
        else:
            item = data
        return item

    def get_one(self, path: str, selector=None) -> dict:
        data = self.GET(path)
        if selector:
            item = data[selector]
        else:
            item = data

        return item

    def get_batch(self, path: str, limit=None, cursor=None, selector=None, how_many=None) -> list[dict]:
        """
        @param path: URL to get batch from
        @param limit: Size of batch size to get from URL
        @param cursor: The location to query from
        @param selector: Do we filter the results to remove the top level key?
        @param how_many: Governs how many of the limit batch to return. if how_many is greater than limit, limit is returned
        @return: list of dicts representing the objects returned from the URL
        """
        params = {}

        if limit is None and how_many is None:
            pass
        elif limit is None:
            limit = how_many
            params["limit"] = how_many
        elif how_many is None:
            params["limit"] = limit
        elif how_many > limit:
            params["limit"] = how_many
        elif how_many == 0:
            params["limit"] = limit

        if cursor:
            params["cursor"] = cursor

        data = self.GET(path, params=params)
        if selector:
            items = data[selector]
        else:
            items = data

        if how_many is None or how_many == 0:
            return items
        elif how_many > len(items):
            return items
        else:
            return items[:how_many]

    def get_cursor(self, path: str, limit=None, cursor=None) -> str | None:
        params = {}
        if limit:
            params["limit"] = limit
        if cursor:
            params["cursor"] = cursor
        doc = self.GET(path, params=params)
        if "pagination" in doc and "cursor" in doc["pagination"]:
            return doc["pagination"]["cursor"]
        else:
            return None

    def paginate(self, path: str, limit=None, cursor=None, selector=None) -> Iterator[dict]:
        params = {}
        if limit:
            params["limit"] = limit
        if cursor:
            params["cursor"] = cursor

        while True:
            data = self.GET(path, params=params)
            if selector:
                iter_data = data[selector]
            else:
                iter_data = data
            if len(iter_data) > 0:  # the end of paginated data
                yield from iter_data
                # for item in iter_data:
                #     yield item
                if "pagination" in data and "cursor" in data["pagination"]:
                    params["cursor"] = data["pagination"]["cursor"]
                else:
                    break
            else:
                break

    def count(self, path: str, limit=None, selector=None) -> int:
        return len([i for i in self.paginate(path, limit=limit, selector=selector)])
