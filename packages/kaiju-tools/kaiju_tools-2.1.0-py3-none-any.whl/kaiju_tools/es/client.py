import re
from asyncio import gather
from typing import *

from aiohttp import ClientResponseError
from multidict import MultiDict

from .schema import Index
from ..http.client import HTTPService
from ..serialization import dumps as encoder

__all__ = ('ESService', 'BulkError')


class BulkError(RuntimeError):
    """A bulk error.

    During ES bulk operations there is the case when a request fails
    only partially. In this case a `BulkError` is risen, which contains an
    information about all exceptions occurred during the request as well as
    a sets of failed and accepted document IDs.
    """

    msg = 'An error during a bulk ES request.'

    def __init__(self, body: dict):

        errors, failed, accepted = [], [], []

        for doc in body.get('items', []):
            for op_name, data in doc.items():
                status = data['status']
                _id = data['_id']
                if status >= 400:
                    failed.append(_id)
                    errors.append({'id': _id, 'status': data['status'], 'error': data['error']})
                else:
                    accepted.append(_id)

        self._errors = tuple(errors)
        self._failed = frozenset(failed)
        self._accepted = frozenset(accepted)

    @property
    def failed(self) -> FrozenSet[str]:
        """A set of failed document IDs."""
        return self._failed

    @property
    def accepted(self) -> FrozenSet[str]:
        """A set of accepted document IDs."""
        return self._accepted

    @property
    def errors(self) -> tuple:
        """A tuple of occurred ES errors."""
        return self._errors

    def __str__(self):
        return self.msg

    def __len__(self):
        return len(self._failed)


class ESService(HTTPService):
    """A ES client service."""

    service_name = 'es'
    query_stripper = re.compile(r'(^[\W_]+|[\W_]+$)', re.UNICODE)

    def __init__(self, app, *args, **kws):
        HTTPService.__init__(self, *args, app=app, **kws)

    async def request(self, method: str, uri, json: Union[dict, list, str] = None, params: dict = None, **kws) -> dict:
        """Send ES request.

        :param method: HTTP request method
        :param uri: a string or a Elastic schema object
        :param json: may be a dict, or a list (for a bulk request) or an already
            encoded JSON string (for performance)
        :param params: request query params
        :param kws:
        :returns: an ES response (usually it's a dict)
        :raises BulkError: if an error in bulk op occurred, a bulk error object
            will contain a detailed information about which part of the request
            has been invalidated
        """
        if isinstance(json, dict):
            json = encoder(json)
        elif isinstance(json, (Iterable, Collection)):
            json = '\n'.join((encoder(d) for d in json)) + '\n'
        uri = str(uri)
        text = await super().request(method, uri, data=json, params=params, accept_json=True, **kws)
        if isinstance(text, dict):
            if text.get('errors') is True:
                self.logger.error('A bulk error occurred: %s.', text)
                raise BulkError(text)
        return text

    async def get_aliases(self) -> dict:
        """Get a map of all existing aliases.

        Currently it is expected that one alias can have only one index.

        :returns: { <alias>: <index>,  ... } dictionary
        """
        data = await self.request('get', '/_cat/aliases', params={'format': 'json', 'h': 'alias,index'})
        data = {record['alias']: record['index'] for record in data}
        return data

    async def index_exists(self, index: Union[str, Index]) -> bool:
        """Return True if index exists."""
        try:
            await self.request('get', str(index))
        except ClientResponseError as err:
            if err.status == 404:
                status = False
            else:
                raise
        else:
            status = True

        return status

    async def delete_index(self, index: Union[str, Index]):
        """Remove an index completely if it exists."""
        if await self.index_exists(index):
            index = str(index)
            self.logger.debug('Removing index "%s".', index)
            await self.request('delete', index)
            self.logger.info('Removed index "%s".', index)

    async def get_index_alias(self, index: Union[str, Index]) -> Optional[str]:
        """Return an index alias (if it has any). Currently it is expected that a single index has a single alias."""
        data = await self.request('get', f'/{index}/_alias/*')
        aliases = data[str(index)]['aliases']
        alias = next(iter(aliases.keys()), None)
        return alias

    async def get_index(self, index: Union[str, Index]) -> Index:
        """Create and returns a new index from the settings present on a ES server, if such index exists."""
        index = str(index)
        self.logger.debug('Getting index settings for "%s".', index)
        settings = await self.request('get', index)
        self.logger.info('Received index settings for "%s".', index)
        index_name = next(iter(settings.keys()))
        settings = settings[index_name]
        meta = settings.get('mappings', {}).get('_meta', {})
        name = settings['settings']['index']['provided_name']
        index = Index(name, **settings, **meta)
        return index

    async def create_index(self, index: Index):
        """Create a completely new index on a ES server."""
        self.logger.debug('Adding a new index "%s".', index.name)
        await self.request('put', str(index), json=index.repr())
        self.logger.info('Added a new index "%s".', index.name)
        return await self.get_index(index)

    async def reindex(self, old: Union[str, Index], new: Union[str, Index]):
        """Copy data from one index to another."""
        return await self.request('post', '_reindex', {'source': {'index': str(old)}, 'dest': {'index': str(new)}})

    async def switch_alias(self, old: Union[str, Index], new: Union[str, Index], alias: str):
        """Switch indices."""
        actions = {
            'actions': [{'remove': {'alias': alias, 'index': str(old)}}, {'add': {'alias': alias, 'index': str(new)}}]
        }
        return await self.request('post', '_aliases', json=actions)

    async def get_index_mapping(self, index: Union[Index, str]):
        """Get index info."""
        return await self.request('get', f'/{index}/_mapping')

    async def update_index(self, index: Index, allow_reindexing=True):
        """Update index schema."""
        old_index = await self.get_index(index.alias)
        index = await self.create_index(index)
        if old_index.mapping.uuid != index.mapping.uuid:
            if allow_reindexing:
                await self.reindex(old_index, index)
                await self.switch_alias(old_index, index, index.alias)
                await self.delete_index(old_index)
                return await self.get_index(index)
            else:
                raise RuntimeError('Cannot update index "%s" because it must be reindexed.')
        elif old_index.settings.uuid != index.settings.uuid:
            await self.delete_index(index)
            old_settings = old_index.settings.repr()
            new_settings = index.settings.repr()
            settings = {
                key: val for key, val in new_settings.items() if key not in old_settings or old_settings[key] != val
            }
            return await self.update_index_settings(index.alias, settings)
        else:
            await self.delete_index(index)
            return old_index

    async def get_index_doc_count(self, index: Union[str, Index]) -> int:
        """Get total number of active docs in an index."""
        data = await self.request('get', f'{index}/_stats', params={'format': 'json'})
        docs_count = int(data['_all']['primaries']['docs']['count'])
        return docs_count

    async def get_indices_doc_count(self) -> dict:
        """Return doc count for all existing indices.

        :returns: { <index name>: <docs count>, ... } map
        """
        data = await self.request('get', '_cat/indices', params={'format': 'json', 'h': 'index,docs.count'})

        return {record['index']: int(record['docs.count']) for record in data}

    async def check_index_health(self, index: Index) -> List[Exception]:
        """Check an index for various health metrics.

        :returns: a list of occurred errors and warnings
        """
        errors = []
        try:
            data = await self.request('get', index / '_stats', params={'format': 'json'})
        except Exception as err:
            err = RuntimeError('Error connecting to index %s. [%s]: %s.' % (index, type(err), str(err)))
            errors.append(err)
        else:
            ok_shards = int(data['_shards']['successful'])
            failed_shards = int(data['_shards']['failed'])
            docs_count = int(data['_all']['primaries']['docs']['count'])

            if docs_count == 0:
                exc = Warning('No documents in index %s.' % index)
                errors.append(exc)

            if ok_shards == 0:
                exc = RuntimeError('No valid shards in index %s.' % index)
                errors.append(exc)

            if failed_shards > 0:
                exc = RuntimeError('%s failed shards found in index %s.' % (index, failed_shards))
                errors.append(exc)

        return errors

    async def get_index_settings(self, index: Index) -> (str, dict):
        """Return an index real name and index settings."""
        self.logger.debug('Request index %s settings.', index.name)
        data = await self.request('get', index.alias)
        name, data = next(iter(data.items()))
        self.logger.info('Requested index %s settings.', index.name)
        return name, data

    async def update_index_settings(self, index: Union[Index, str], settings: dict) -> Index:
        """Update index /_settings."""
        self.logger.debug('Updating index "%s" settings.', index)
        await self.request('put', f'{index}/_settings', json=settings)
        self.logger.debug('Updated index "%s" settings.', index)
        return await self.get_index(index)

    async def refresh(self, index: Index):
        """Refresh an index after the update (usually elastic does this automatically)."""
        await self.request('get', index / '_refresh')

    async def force_merge(self, index: Index):
        """Optimize index storage."""
        await self.request('post', index / '_forcemerge')

    async def get(self, index: Index, keys: Collection[str], fields: Collection[str] = None) -> List[dict]:
        """Get multiple documents from an index by their IDs.

        The method will return only existing documents. Fields parameter is needed only if you
        need only specific fields returned.

        > await es.get(idx, {'1', '2', '3'}, fields=['id', 'name'])
        [
          {'_doc_id': '1', 'id': '1', 'name': 'abc'},
          {'_doc_id': '1', 'id': '3', 'name': 'sht'}
        ]

        """
        self.logger.debug('Receiving %d objects from %s.', len(keys), index.name)
        key = index.primary_key

        data = {'ids': list(set(keys))}
        params = {'realtime': 'false', 'preference': '_local', 'filter_path': 'docs._id,docs._source,docs.found'}

        if fields is None:
            params['_source_includes'] = '*'
        elif len(fields) == 0:
            params['_source_excludes'] = '*'
        else:
            params['_source'] = ','.join(set(fields))

        data = await self.request('get', index / '_mget', json=data, params=params)

        result = []

        for d in data['docs']:
            if d['found']:
                source = d.get('_source', {})
                source[key] = d['_id']
                result.append(source)

        self.logger.info('Received %d objects from %s.', len(result), index.name)
        return result

    async def exist(self, index: Index, keys: Collection[str]) -> frozenset:
        """Check that multiple documents exist in index.

        > await es.exist(idx, {'1', '2', '3'})
        frozenset({'1', '2'})

        """
        self.logger.debug('Checking %s objects in %s.', len(keys), index.name)
        data = await self.get(index, keys, fields=[])
        data = frozenset(d[index.primary_key] for d in data)
        self.logger.info('%s object of %s found in %s.', len(data), len(keys), index.name)
        return data

    async def insert(self, index: Index, data: Collection[dict]):
        """Add new documents replacing older ones if required.

        > await es.insert(idx, [{'id': '1', 'name': 'abc'}, {'id': '3', 'name': 'sht'])
        None

        """
        self.logger.debug('Adding %s objects to %s.', len(data), index.name)
        _data = []
        key_name = index.primary_key
        for doc in data:
            _data.append({'index': {'_id': doc[key_name]}})
            del doc[key_name]
            _data.append(doc)
        await self.request('post', index / '_bulk', json=_data)
        self.logger.info('Added %s objects to %s.', len(data), index.name)

    async def update(self, index: Index, data: Collection[dict]):
        """Update document attributes. Documents must exist in the index.

        > await es.update(idx, [{'id': '1', 'name': 'other'}])
        None

        """
        self.logger.debug('Updating %s objects in %s.', len(data), index.name)
        _data = []
        key_name = index.primary_key
        for doc in data:
            _data.append({'update': {'_id': doc[key_name]}})
            del doc[key_name]
            _data.append({'doc': doc})
        await self.request('post', index / '_bulk', json=_data)
        self.logger.info('Updated %s objects in %s.', len(data), index.name)

    async def delete(self, index: Index, keys: Collection):
        """Remove multiple documents from index. Doesn't matter if documents exist or not.

        > await es.delete(idx, {'1', '2', '3'})
        None

        """
        self.logger.debug('Removing %s objects from %s.', len(keys), index.name)
        _data = []
        for key in set(keys):
            _data.append({'delete': {'_id': key}})
        await self.request('post', index / '_bulk', json=_data)
        self.logger.info('Removed %s objects from %s.', len(keys), index.name)

    async def bulk(self, instructions: dict) -> [Union[Exception, None, dict], Union[Exception, None]]:
        """Do a bulk index updates / inserts / removes.

        Данный класс не вызывает ошибку, если она произошла, а возвращает ее
        в результатах. Это сделано для того, чтобы можно было отдельно получить
        и обработать результаты multi-get запроса и bulk-insert/update/delete
        запроса.

        Объекты нужно передать в следующем виде (пример):

        {
            "get": [
                {"index": <Index1>, "doc": {"id": "545"}, "fields": ["id", "name"]}
                ...
            ],
            "delete": [
                {"index": <Index1>, "doc": {"id": "123"}},
                {"index": <Index2>, "doc": {"id": "345"}},
                ...
            ],
            "insert": [
                {"index": <Index3>, "doc": {"id": "123", "name": "fck"}},
                ...
            ],
            "update": [...]
        }

        Ответ для multi_get части будет в виде

        {
            <Index>: [ ... <docs> ... ]
            ...
        }

        либо `Exception` объект, если
        возникли проблемы. Либл None, если запрос не выполнялся.

        Ответ для bulk операций будет либо None, либо `Exception` объект, если
        возникли проблемы.

        Оба ответа выдаются в виде tuple, т.е. (get ответ, bulk ответ).

        """
        self.logger.debug('Making a composite bulk request.')

        _mget, _bulk = [], []
        _indices = {}

        for instruction, data in instructions.items():

            for obj in data:

                idx = obj['index']
                doc = obj['doc']
                _id = doc[idx.primary_key]
                header = {'_index': idx.name, '_id': _id}
                if idx.name not in _indices:
                    _indices[idx.name] = idx

                if instruction == 'get':
                    fields = obj.get('fields')
                    if fields is not None and not fields:
                        header['_source'] = False
                    elif fields:
                        fields.append(idx.primary_key)
                        fields = list(set(fields))
                        header['_source'] = fields
                    _mget.append(header)
                else:
                    if instruction == 'insert':
                        _bulk.append({'index': header})
                        _bulk.append(doc)
                    else:
                        _bulk.append({instruction: header})
                        if instruction == 'update':
                            _bulk.append({'doc': doc})

        _tasks = []

        if _mget:
            _tasks.append(self.request('get', '_mget', json={'docs': _mget}))
        if _bulk:
            _tasks.append(self.request('post', '_bulk', json=_bulk))

        results = await gather(*_tasks, return_exceptions=True)
        get_result = results[0] if _mget else None
        bulk_result = results[-1] if _bulk else None

        if isinstance(get_result, dict):
            result = MultiDict()
            for doc in get_result['docs']:
                idx = _indices[doc['_index']]
                source = doc.get('_source', {})
                source[idx.primary_key] = doc['_id']
                result.add(idx.alias, source)
            get_result = {k: result.getall(k) for k in result}

        self.logger.info('Made a composite bulk request.')

        return get_result, bulk_result
