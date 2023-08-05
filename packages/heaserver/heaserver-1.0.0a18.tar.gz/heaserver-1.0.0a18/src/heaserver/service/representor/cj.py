"""
Collection+JSON representor. It converts a WeSTL document into Collection+JSON form. The Collection+JSON spec is at
http://amundsen.com/media-types/collection/. HEA implements the spec with the following exceptions:
* Data array:
** A section property. When going to/from nvpjson, the nvpjson object will have properties for each section,
each of which will have a nested object with the properties in that section.
** A sectionPrompt property for displaying a section name.
** Periods are reserved and should not be used in name property values.
"""

import json
import uritemplate
import logging
from heaobject import root
from json.decoder import JSONDecodeError
from .error import ParseException
from .. import jsonschemavalidator
from aiohttp.web import Request
from typing import Mapping, Any, Union, Dict, List, Optional, Type, Tuple, Generator
from yarl import URL
from .representor import Representor


MIME_TYPE = 'application/vnd.collection+json'

TEMPLATE_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'properties': {
        'template': {
            'type': 'object',
            'properties': {
                'data': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string'},
                            'value': {},
                        },
                        'required': ['name']
                    }
                }
            },
        }
    },
    'required': ['template']
}


_TEMPLATE_SCHEMA_VALIDATOR = jsonschemavalidator.compile(TEMPLATE_SCHEMA)


class CJ(Representor):
    MIME_TYPE = MIME_TYPE

    async def formats(self, request: Request, wstl_obj: Union[List[Dict[str, Any]], Dict[str, Any]],
                      coll_url: Union[str, URL], dumps=json.dumps) -> bytes:
        """
        Formats a run-time WeSTL document as a Collection+JSON document.

        :param request: the HTTP request.
        :param wstl_obj: dict with run-time WeSTL JSON, or a list of run-time WeSTL JSON dicts.
        :param coll_url: the URL of the collection.
        :param dumps: any callable that accepts dict with JSON and outputs str. Cannot be None.
        :return: str containing Collection+JSON collection JSON.
        """
        def wstl_generator() -> Generator:
            for w in (wstl_obj if isinstance(wstl_obj, list) else [wstl_obj]):
                def extract_data(w_: Dict[str, Any], d_: List[Dict[str, Any]]) -> Dict[str, Any]:
                    w_['wstl']['data'] = d_
                    return w_
                for d in w['wstl'].get('data', []):
                    yield self.__format(request, extract_data(w, [d]), coll_url)
        return dumps(list(w for w in wstl_generator()), default=root.json_encode).encode('utf-8')

    async def parse(self, request: Request) -> Mapping[str, Any]:
        """
        Parses an HTTP request containing a Collection+JSON template JSON document body into a dict-like object.

        :param request: the HTTP request. Cannot be None.
        :return: the data section of the Collection+JSON document transformed into a dict-like object.
        """
        try:
            return to_nvpjson(await request.json())
        except (JSONDecodeError, jsonschemavalidator.ValidationError) as e:
            raise ParseException() from e

    @staticmethod
    def __format(request: Request, wstl_obj: Union[List[Dict[str, Any]], Dict[str, Any]], coll_url: Union[str, URL]) -> Dict[str, Any]:
        """
        Formats a run-time WeSTL document as a Collection+JSON document.

        :param request: the HTTP request.
        :param wstl_obj: dict with run-time WeSTL JSON, or a list of run-time WeSTL JSON dicts.
        :param coll_url: the URL of the collection.
        :return: a Collection+JSON dict.
        """
        collection: Dict[str, Any] = {}

        if isinstance(wstl_obj, list):
            wstl_sections = [wstl_obj_['wstl'] for wstl_obj_ in wstl_obj]
        else:
            wstl_sections = [wstl_obj['wstl']]
        collection['version'] = '1.0'
        collection['href'] = str(coll_url) if coll_url else ''

        for wstl_section in wstl_sections:
            content = _get_content(wstl_section)
            if content:
                collection['content'] = content
                break

        for wstl_section in wstl_sections:
            items, tvars = _get_items(request, wstl_section, wstl_sections)
            if items:
                collection.setdefault('items', []).extend(items)
            links = _get_links(wstl_section['actions'], tvars)
            if links:
                collection.setdefault('links', []).extend(links)
            if 'template' not in collection:
                template = _get_template(wstl_section['actions'], tvars)
                if template:
                    collection['template'] = template

        for wstl_section in wstl_sections:
            queries = _get_queries(wstl_section['actions'])
            if queries:
                collection.setdefault('queries', []).extend(queries)

        if 'template' in collection and 'href' in collection['template']:
            collection['href'] = collection['template']['href']
            del collection['template']['href']

        for wstl_section in wstl_sections:
            if 'error' in wstl_section:
                collection['error'] = _get_error(wstl_section['error'])
                break

        return {'collection': collection}


def to_nvpjson(cj_template: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts a Collection+JSON template dict into an array of nvpjson object dicts.

    :param cj_template: a dict
    :return: nvpjson
    :raises jsonschemavalidator.ValidationError if invalid Collection+JSON was passed in.
    """
    _TEMPLATE_SCHEMA_VALIDATOR.validate(cj_template)
    data = cj_template['template'].get('data', [])
    result = {}
    for d in data:
        nm = d['name']
        val = d.get('value', None)
        section = d.get('section', None)
        if section:
            result.setdefault(section, {})[nm] = val
        else:
            result[nm] = val
    return result


def _get_content(obj):
    return obj.get('content', {})


def _get_links(actions, tvars=None):
    """
    Get top-level links.
    :param actions: iterator of actions.
    :return:
    """
    rtn = []
    for link in actions:
        if link['type'] == 'safe' \
            and 'app' in link['target'] \
                and 'cj' in link['target'] \
                    and ('inputs' not in link or not link['inputs']):
            url = uritemplate.expand(link['href'], tvars)
            rtn.append({
                'href': url,
                'rel': ' '.join(link['rel']) or '',
                'prompt': link.get('prompt', '')
            })
    return rtn


def _get_items(request: Request, wstl_obj: Dict[str, Any], wstl_sections: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    rtn = []
    tvars = {}
    data_len = sum(len(w.get('data', [])) for w in wstl_sections)
    coll = wstl_obj.get('data', [])
    logger = logging.getLogger(__package__)
    logger.debug(f'{data_len} items')
    for temp in coll:
        item: Dict[str, Any] = {}
        data: List[Dict[str, Any]] = []
        type_str: Optional[str] = temp.get('type', None)
        if type_str:
            type_: Optional[Type[root.HEAObject]] = root.type_for_name(type_str)
        else:
            type_ = None
        local_tvars = {}
        for k, v in temp.items():
            if isinstance(v, dict):
                for kprime, vprime in v.items():
                    if kprime != 'meta' and kprime != 'type':
                        data.append({
                            'section': k,
                            'name': kprime,
                            'value': vprime,
                            'prompt': type_.get_prompt(kprime) if type_ else None,
                            'display': type_.is_displayed(kprime) if type_ else None
                        })
                        if data_len == 1:
                            tvars[f'{k}.{kprime}'] = vprime
                        local_tvars[f'{k}.{kprime}'] = vprime
            else:
                if k != 'meta' and k != 'type':
                    data.append({
                        'name': k,
                        'value': v,
                        'prompt': type_.get_prompt(k) if type_ else None,
                        'display': type_.is_displayed(k) if type_ else None
                    })
                    if data_len == 1:
                        tvars[k] = v
                    local_tvars[k] = v
        item['data'] = data
        local_tvars.update(request.match_info)
        logger.debug(f'local_tvars={local_tvars}')

        link = _get_item_link(wstl_obj['actions'])
        if link:
            if isinstance(link['rel'], list):
                item['rel'] = ' '.join(link['rel'])
            else:
                item['rel'] = link['rel']
            item['href'] = uritemplate.expand(link['href'], local_tvars)

        item['links'] = _get_item_links(wstl_obj['actions'], local_tvars)

        rtn.append(item)
    tvars.update(request.match_info)
    logger.debug(f'tvars={tvars}')
    return rtn, tvars


def _get_queries(actions):
    rtn = []
    for action in actions:
        if 'inputs' in action and action['type'] == 'safe' and \
                _is_in_target('list', action) and _is_in_target('cj', action):
            q = {'rel': ' '.join(action['rel']), 'href': action['href'], 'prompt': action.get('prompt', ''), 'data': []}
            inputs_ = action['inputs']
            for i in range(len(inputs_)):
                d = inputs_[i]
                nm = d.get('name', 'input' + str(i))
                q['data'].append({
                    'name': nm,
                    'value': d.get('value', None),
                    'prompt': d.get('prompt', nm),
                    'required': d.get('required', False),
                    'readOnly': d.get('readOnly', False),
                    'pattern': d.get('pattern', '')
                })
            rtn.append(q)
    return rtn


def _get_template(actions, tvars):
    rtn = {}
    for action in actions:
        if _is_in_target('cj-template', action):
            is_add = _is_in_target('add', action)

            rtn['prompt'] = action.get('prompt', action['name'])
            rtn['rel'] = ' '.join(action['rel'])
            rtn['href'] = uritemplate.expand(action['href'], tvars)

            rtn['data'] = []
            for d in action['inputs']:
                nm = d['name']
                if is_add:
                    value_ = d.get('value', None)
                elif 'section' in d:
                    value_ = tvars.get(f'{d["section"]}.{nm}')
                else:
                    value_ = tvars.get(nm, None)
                data_ = {
                    'name': nm,
                    'value': value_,
                    'prompt': d.get('prompt', nm),
                    'required': d.get('required', False),
                    'readOnly': d.get('readOnly', False),
                    'pattern': d.get('pattern', '')
                }
                if 'section' in d:
                    data_['section'] = d['section']
                rtn['data'].append(data_)
            break
    return rtn


def _get_item_links(actions, tvars):
    coll = []
    for action in actions:
        target = action['target']
        if 'item' in target and 'read' in target and 'cj' in target:
            coll.append({
                'prompt': action['prompt'],
                'rel': ' '.join(action['rel']),
                'href': uritemplate.expand(action['href'], tvars)
            })
    return coll


def _get_item_link(actions):
    rtn = {}
    for action in actions:
        target = action['target']
        if 'item' in target and 'href' in target and 'cj' in target:
            rtn['rel'] = ' '.join(action['rel'])
            rtn['href'] = action['href']
            break
    return rtn


def _get_error(obj):
    return {'title': 'Error', 'message': obj.message or '', 'code': obj.code or '', 'url': obj.url or ''}


def _is_in_target(str_, action):
    return str_ in action['target'].split(' ')