from aiohttp.test_utils import unittest_run_loop, AioHTTPTestCase
from aiohttp import hdrs
from ..oidcclaimhdrs import SUB
from heaobject import user
from ..representor import wstljson, cj, nvpjson, xwwwformurlencoded
from urllib.parse import urlencode
from typing import TYPE_CHECKING
from .mongotestcase import MongoTestCase
from .. import jsonschemavalidator
import logging


if TYPE_CHECKING:
    _Base = MongoTestCase
else:
    _Base = object


class PostMixin(_Base):
    @unittest_run_loop
    async def test_post(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        str(self._resource_path / ''),
                                        json=self._body_post,
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual('201: Created', await obj.text())

    @unittest_run_loop
    async def test_post_nvpjson(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        str(self._resource_path / ''),
                                        json={e['name']: e['value'] for e in self._body_post['template']['data']}, # type: ignore[index]
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual('201: Created', await obj.text())

    @unittest_run_loop
    async def test_post_xwwwformurlencoded(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        str(self._resource_path / ''),
                                        data=self._post_data(),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual('201: Created', await obj.text())

    @unittest_run_loop
    async def test_post_status(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        str(self._resource_path / ''),
                                        json=self._body_post,
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(201, obj.status)

    @unittest_run_loop
    async def test_post_status_nvpjson(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        str(self._resource_path / ''),
                                        json={e['name']: e['value'] for e in self._body_post['template']['data']}, # type: ignore[index]
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(201, obj.status)

    @unittest_run_loop
    async def test_post_status_xwwwformurlencoded(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        str(self._resource_path / ''),
                                        data=self._post_data(),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual(201, obj.status)

    @unittest_run_loop
    async def test_post_status_empty_body(self) -> None:
        obj = await self.client.request('POST',
                                        str(self._resource_path / ''),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(400, obj.status)

    @unittest_run_loop
    async def test_post_status_empty_body_nvpjson(self) -> None:
        obj = await self.client.request('POST',
                                        str(self._resource_path / ''),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    @unittest_run_loop
    async def test_post_status_empty_body_xwwwformurlencoded(self) -> None:
        obj = await self.client.request('POST',
                                        str(self._resource_path / ''),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual(400, obj.status)

    @unittest_run_loop
    async def test_post_status_invalid_type(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        await self._test_invalid({'type': 'foobar'})

    @unittest_run_loop
    async def test_invalid_url(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        str(self._resource_path / '1'),
                                        json=self._body_post,
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(405, obj.status)

    async def _test_invalid(self, changes) -> None:
        changed = _copy_heaobject_dict_with(self._body_post, changes)
        obj = await self.client.request('POST',
                                        str(self._resource_path / ''),
                                        json=changed,
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    def _post_data(self):
        return _to_xwwwformurlencoded_data(self._body_post)


class PutMixin(_Base):
    @unittest_run_loop
    async def test_put(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        str(self._resource_path / self._id()),
                                        json=self._body_put,
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual('', await obj.text())

    @unittest_run_loop
    async def test_put_nvpjson(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        str(self._resource_path / self._id()),
                                        json={e['name']: e['value'] for e in self._body_put['template']['data']}, # type: ignore[index]
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual('', await obj.text())

    @unittest_run_loop
    async def test_put_xwwwformurlencoded(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        try:
            data_ = self._put_data()
        except jsonschemavalidator.ValidationError:
            self.skipTest('_body_put cannot be converted xwwwformurlencoded form')
        else:
            obj = await self.client.request('PUT',
                                            str(self._resource_path / self._id()),
                                            data=data_,
                                            headers={SUB: user.NONE_USER,
                                                     hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                     hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
            self.assertEqual('', await obj.text())

    @unittest_run_loop
    async def test_put_status(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        str(self._resource_path / self._id()),
                                        json=self._body_put,
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(204, obj.status)

    @unittest_run_loop
    async def test_put_status_wrong_format(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        str(self._resource_path / self._id()),
                                        json=cj.to_nvpjson(self._body_put),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(400, obj.status)

    @unittest_run_loop
    async def test_put_status_nvpjson(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        str(self._resource_path / self._id()),
                                        json=cj.to_nvpjson(self._body_put),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(204, obj.status)

    @unittest_run_loop
    async def test_put_status_nvpjson_wrong_format(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        try:
            data_ = self._put_data()
        except jsonschemavalidator.ValidationError:
            self.skipTest('_body_put cannot be converted xwwwformurlencoded form')
        else:
            obj = await self.client.request('PUT',
                                            str(self._resource_path / self._id()),
                                            json=data_,
                                            headers={SUB: user.NONE_USER,
                                                     hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                     hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    @unittest_run_loop
    async def test_put_status_xwwwformurlencoded(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        try:
            data_ = self._put_data()
        except jsonschemavalidator.ValidationError:
            self.skipTest('_body_put cannot be converted xwwwformurlencoded form')
        else:
            obj = await self.client.request('PUT',
                                            str(self._resource_path / self._id()),
                                            data=data_,
                                            headers={SUB: user.NONE_USER,
                                                     hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                     hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
            self.assertEqual(204, obj.status)

    @unittest_run_loop
    async def test_put_status_xwwwformurlencoded_wrong_format(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        str(self._resource_path / self._id()),
                                        json=self._body_put,
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual(400, obj.status)

    @unittest_run_loop
    async def test_put_status_empty_body(self) -> None:
        obj = await self.client.request('PUT',
                                        str(self._resource_path / '666f6f2d6261722d71757578'),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(400, obj.status)

    @unittest_run_loop
    async def test_put_status_empty_body_nvpjson(self) -> None:
        obj = await self.client.request('PUT',
                                        str(self._resource_path / '666f6f2d6261722d71757578'),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    @unittest_run_loop
    async def test_put_status_empty_body_xwwwformurlencoded(self) -> None:
        obj = await self.client.request('PUT',
                                        str(self._resource_path / '666f6f2d6261722d71757578'),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual(400, obj.status)

    @unittest_run_loop
    async def test_put_status_missing_id(self) -> None:
        obj = await self.client.request('PUT',
                                        str(self._resource_path),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(405, obj.status)

    @unittest_run_loop
    async def test_put_status_missing_id_nvpjson(self) -> None:
        obj = await self.client.request('PUT',
                                        str(self._resource_path),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(405, obj.status)

    @unittest_run_loop
    async def test_put_status_invalid_type(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        await self._test_invalid({'type': 'foobar'})

    async def _test_invalid(self, changes) -> None:
        changed = _copy_heaobject_dict_with(self._body_put, changes)
        obj = await self.client.request('PUT',
                                        str(self._resource_path / '666f6f2d6261722d71757578'),
                                        json=changed,
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    def _put_data(self):
        return _to_xwwwformurlencoded_data(self._body_put)

    def _id(self):
        logging.getLogger(__name__).debug(f'Template is {self._body_put}')
        for e in self._body_put['template']['data']:
            if e['name'] == 'id':
                return e.get('value')


class GetOneMixin(_Base):
    @unittest_run_loop
    async def test_get(self) -> None:
        obj = await self.client.request('GET',
                                        str(self._resource_path / '666f6f2d6261722d71757578'),
                                        headers={SUB: user.NONE_USER, hdrs.X_FORWARDED_HOST: 'localhost:8080'})
        self.assertEqual(_ordered(self._expected_one), _ordered(await obj.json()))

    @unittest_run_loop
    async def test_get_status(self) -> None:
        obj = await self.client.request('GET',
                                        str(self._resource_path / '666f6f2d6261722d71757578'),
                                        headers={SUB: user.NONE_USER, hdrs.X_FORWARDED_HOST: 'localhost:8080'})
        self.assertEqual(200, obj.status)

    @unittest_run_loop
    async def test_get_wstl(self) -> None:
        if not self._expected_one_wstl:
            self.skipTest('self._expected_one_wstl is not defined')
        obj = await self.client.request('GET',
                                        str(self._resource_path / '666f6f2d6261722d71757578'),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.ACCEPT: wstljson.MIME_TYPE
                                                 })
        self.assertEqual(_ordered(self._expected_one_wstl), _ordered(await obj.json()))

    @unittest_run_loop
    async def test_get_properties_form(self) -> None:
        if not self._expected_one_properties_form:
            self.skipTest('self._expected_one_properties_form is not defined')
        obj = await self.client.request('GET',
                                        str(self._resource_path / '666f6f2d6261722d71757578' / 'properties'),
                                        headers={SUB: user.NONE_USER, hdrs.X_FORWARDED_HOST: 'localhost:8080'})
        self.assertEqual(_ordered(self._expected_one_properties_form), _ordered(await obj.json()))

    @unittest_run_loop
    async def test_get_duplicate_form(self) -> None:
        if not self._expected_one_duplicate_form:
            self.skipTest('self._expected_one_duplicate_wstl is not defined')
        obj = await self.client.request('GET',
                                        str(self._resource_path / '666f6f2d6261722d71757578' / 'duplicator'),
                                        headers={SUB: user.NONE_USER, hdrs.X_FORWARDED_HOST: 'localhost:8080'})
        self.assertEqual(_ordered(self._expected_one_duplicate_form), _ordered(await obj.json()))


class GetAllMixin(_Base):
    @unittest_run_loop
    async def test_get_all(self) -> None:
        obj = await self.client.request('GET',
                                        str(self._resource_path / ''),
                                        headers={SUB: user.NONE_USER, hdrs.X_FORWARDED_HOST: 'localhost:8080'})
        self.assertEqual(200, obj.status)

    @unittest_run_loop
    async def test_get_all_json(self) -> None:
        obj = await self.client.request('GET',
                                        str(self._resource_path / ''),
                                        headers={SUB: user.NONE_USER, hdrs.X_FORWARDED_HOST: 'localhost:8080'})
        self.assertEqual(_ordered(self._expected_all), _ordered(await obj.json()))

    @unittest_run_loop
    async def test_get_all_wstl(self) -> None:
        if not self._expected_all_wstl:
            self.skipTest('self._expected_all_wstl is not defined')
        obj = await self.client.request('GET',
                                        str(self._resource_path / ''),
                                        headers={SUB: user.NONE_USER,
                                                 hdrs.X_FORWARDED_HOST: 'localhost:8080',
                                                 hdrs.ACCEPT: wstljson.MIME_TYPE
                                                 })
        self.assertEqual(_ordered(self._expected_all_wstl), _ordered(await obj.json()))


class DeleteMixin(_Base):
    @unittest_run_loop
    async def test_delete_success(self) -> None:
        obj = await self.client.request('DELETE',
                                        str(self._resource_path / '666f6f2d6261722d71757578'),
                                        headers={SUB: user.NONE_USER, hdrs.X_FORWARDED_HOST: 'localhost:8080'})
        self.assertEqual(204, obj.status)

    @unittest_run_loop
    async def test_delete_fail(self) -> None:
        obj = await self.client.request('DELETE',
                                        str(self._resource_path / '3'),
                                        headers={SUB: user.NONE_USER, hdrs.X_FORWARDED_HOST: 'localhost:8080'})
        self.assertEqual(404, obj.status)


def _copy_heaobject_dict_with(d, changes):
    copied_dict = dict(d)
    copied_dict.update(changes)
    return copied_dict


_TEMPLATE_SCHEMA_VALIDATOR = jsonschemavalidator.compile(cj.TEMPLATE_SCHEMA)


def _to_xwwwformurlencoded_data(template) -> str:
    _logger = logging.getLogger(__name__)
    _logger.debug(f'Encoding {template}')
    e = {}
    _TEMPLATE_SCHEMA_VALIDATOR.validate(template)
    for e_ in template['template']['data']:
        if 'section' in e_:
            raise jsonschemavalidator.ValidationError('XWWWFormUrlEncoded does not support the section property')
        if e_['value'] is not None:
            e[e_['name']] = e_['value']
    result = urlencode(e, True)
    _logger.debug(f'Returning {result}')
    return result


def _ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, _ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(_ordered(x) for x in obj)
    else:
        return obj
