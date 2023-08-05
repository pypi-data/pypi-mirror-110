"""
WeSTL JSON representor. It just serializes run-time WeSTL to JSON. The WeSTL spec is at
http://rwcbook.github.io/wstl-spec/.
"""

import json
from typing import Union
from yarl import URL
from .representor import Representor
from aiohttp.web import Request
from typing import Mapping, Any, Dict, List
from heaobject.root import json_encode


MIME_TYPE = 'application/vnd.wstl+json'


class WeSTLJSON(Representor):
    MIME_TYPE = MIME_TYPE

    async def formats(self, request: Request, wstl_obj: Union[List[Dict[str, Any]], Dict[str, Any]], coll_url: Union[str, URL], dumps=json.dumps) -> bytes:
        """
        Serializes a run-time WeSTL document to JSON.

        :param request: the HTTP request.
        :param wstl_obj: dict with run-time WeSTL JSON, or a list of run-time WeSTL JSON dicts.
        :param coll_url: the URL of the collection. Not used by this implementation.
        :param dumps: any callable that accepts dict with JSON and outputs str. Cannot be None.
        :return: str containing run-time WeSTL collection JSON.
        """
        return dumps(wstl_obj if isinstance(wstl_obj, list) else [wstl_obj], default=json_encode).encode('utf-8')

    async def parse(self, request: Request) -> Mapping[str, Any]:
        raise NotImplementedError


