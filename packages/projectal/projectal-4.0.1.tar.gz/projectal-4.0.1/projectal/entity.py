"""
The base Entity class that all entities inherit from.
"""
import copy
import logging
import sys

import projectal
from projectal import api


class Entity(dict):
    """
    The parent class for all our entities, offering requests
    and validation for the fundamental create/read/update/delete
    operations.

    This class (and all our entities) inherit from the builtin
    `dict` class. This means all entity classes can be used
    like standard Python dictionary objects, but we can also
    offer additional utility functions that operate on the
    instance itself (see `linkers` for an example). Any method
    that expects a `dict` can also consume an `Entity` subclass.

    The class methods in this class can operate on one or more
    entities in one request. If the methods are called with
    lists (for batch operation), the output returned will also
    be a list. Otherwise, a single `Entity` subclass is returned.

    Note for batch operations: a `ProjectalException` is raised
    if *any* of the entities fail during the operation. The
    changes will *still be saved to the database for the entities
    that did not fail*.
    """

    #: Child classes must override these with their entity names
    _path = 'entity'  # URL portion to api
    _name = 'entity'

    # And to which entities they link to
    _links = []
    _links_reverse = []

    def __init__(self, data):
        dict.__init__(self, data)
        self._is_new = True
        self._link_def_by_key = {}
        self._link_def_by_name = {}
        self._create_link_defs()
        self._with_links = set()

        self.__fetch = self.get
        self.get = self.__get
        self.update = self.__update
        self.delete = self.__delete
        self.history = self.__history
        self.__old = copy.deepcopy(self)
        self.__type_links()

    # ----- LINKING -----

    def _create_link_defs(self):
        for cls in self._links:
            self._add_link_def(cls)
        for cls in self._links_reverse:
            self._add_link_def(cls, reverse=True)

    def _add_link_def(self, cls, reverse=False):
        """
        Each entity is accompanied by a dict with details about how to
        get access to the data of the link within the object. Subclasses
        can pass in customizations to this dict when their APIs differ.

        reverse denotes a reverse linker, where extra work is done to
        reverse the relationship of the link internally so that it works.
        The backend only offers one side of the relationship.
        """
        d = {
            'name': cls._link_name,
            'link_key': cls._link_key or cls._link_name + 'List',
            'data_name': cls._link_data_name,
            'type': cls._link_type,
            'entity': cls._link_entity or cls._link_name.capitalize(),
            'reverse': reverse
        }
        self._link_def_by_key[d['link_key']] = d
        self._link_def_by_name[d['name']] = d

    def _add_link(self, to_entity_name, to_link):
        self._link(to_entity_name, to_link, 'add', batch_linking=False)

    def _update_link(self,to_entity_name, to_link):
        self._link(to_entity_name, to_link, 'update', batch_linking=False)

    def _delete_link(self, to_entity_name, to_link):
        self._link(to_entity_name, to_link, 'delete', batch_linking=False)

    def _link(self, to_entity_name, to_link, operation, update_cache=True, batch_linking=True):
        """
        `to_entity_name`: Destination entity name (e.g. 'staff')

        `to_link`: List of Entities of the same type (and optional data) to link to

        `operation`: `add`, `update`, `delete`

        'update_cache': also modify the entity's internal representation of the links
        to match the operation that was done. Set this to False when replacing the
        list with a new one (i.e., when calling save() instead of a linker method).

        'batch_linking': Enabled by default, batches any link
        updates required into composite API requests. If disabled
        a request will be executed for each link update.
        Recommended to leave enabled to increase performance.
        """

        link_def = self._link_def_by_name[to_entity_name]
        to_key = link_def['link_key']

        if isinstance(to_link, dict) and link_def['type'] == list:
            # Convert input dict to list when link type is a list (we allow linking to single entity for convenience)
            to_link = [to_link]

            # For cases where user passed in dict instead of Entity, we turn them into
            # Entity on their behalf.
            typed_list = []
            target_cls = getattr(sys.modules['projectal.entities'], link_def['entity'])
            for link in to_link:
                if not isinstance(link, target_cls):
                    typed_list.append(target_cls(link))
                else:
                    typed_list.append(link)
            to_link = typed_list
        else:
            # For everything else, we expect types to match.
            if not isinstance(to_link, link_def['type']):
                raise api.UsageException('Expected link type to be {}. Got {}.'.format(link_def['type'], type(to_link)))

        if not to_link:
            return

        url = ''
        payload = {}
        request_list = []
        # Is it a reverse linker? If so, invert the relationship
        if link_def['reverse']:
            for link in to_link:
                request_list.extend(link._link(self._name, self, operation, update_cache, batch_linking=batch_linking))
        else:
            # Only keep UUID and the data attribute, if it has one
            def strip_payload(link):
                single = {'uuId': link['uuId']}
                data_name = link_def.get('data_name')
                if data_name and data_name in link:
                    single[data_name] = copy.deepcopy(link[data_name])
                return single

            # If batch linking is enabled and the entity to link is a list of entities,
            # a separate request must be constructed for each one because the final composite
            # request permits only one input per call
            url = '/api/{}/link/{}/{}'.format(self._path, to_entity_name, operation)
            to_link_payload = None
            if isinstance(to_link, list):
                to_link_payload = []
                for link in to_link:
                    if batch_linking:
                        request_list.append({
                            'method': "POST",
                            'invoke': url,
                            'body': {
                                'uuId': self['uuId'],
                                to_key: [strip_payload(link)],
                            }
                        })
                    else:
                        to_link_payload.append(strip_payload(link))
            if isinstance(to_link, dict):
                if batch_linking:
                    request_list.append({
                        'method': "POST",
                        'invoke': url,
                        'body': {
                            'uuId': self['uuId'],
                            to_key: strip_payload(to_link),
                        }
                    })
                else:
                    to_link_payload = strip_payload(to_link)

            if not batch_linking:
                payload = {
                    'uuId': self['uuId'],
                    to_key: to_link_payload
                }
                api.post(url, payload=payload)

        if not update_cache:
            return request_list

        # Set the initial state if first add. We need the type to be set to correctly update the cache
        if operation == 'add' and self.get(to_key, None) is None:
            if link_def.get('type') == dict:
                self[to_key] = {}
            elif link_def.get('type') == list:
                self[to_key] = []

        # Modify the entity object's cache of links to match the changes we pushed to the server.
        if isinstance(self.get(to_key, []), list):
            if operation == 'add':
                # Sometimes the backend doesn't return a list when it has none. Create it.
                if to_key not in self:
                    self[to_key] = []

                for to_entity in to_link:
                    self[to_key].append(to_entity)
            else:
                for to_entity in to_link:
                    # Find it in original list
                    for i, old in enumerate(self.get(to_key, [])):
                        if old['uuId'] == to_entity['uuId']:
                            if operation == 'update':
                                self[to_key][i] = to_entity
                            elif operation == 'delete':
                                del self[to_key][i]
        if isinstance(self.get(to_key, None), dict):
            if operation in ['add', 'update']:
                self[to_key] = to_link
            elif operation == 'delete':
                self[to_key] = None

        # Update the "old" record of the link on the entity to avoid
        # flagging it for changes (link lists are not meant to be user editable).
        if to_key in self:
            self.__old[to_key] = self[to_key]

        return request_list

    # -----

    @classmethod
    def create(cls, entities, params=None, batch_linking=True):
        """
        Create one or more entities of the same type. The entity
        type is determined by the subclass calling this method.

        `entities`: Can be a `dict` to create a single entity,
        or a list of `dict`s to create many entities in bulk.

        `params`: Optional URL parameters that may apply to the
        entity's API (e.g: `?holder=1234`).

        'batch_linking': Enabled by default, batches any link
        updates required into composite API requests. If disabled
        a request will be executed for each link update.
        Recommended to leave enabled to increase performance.

        If input was a `dict`, returns an entity subclass. If input was
        a list of `dict`s, returns a list of entity subclasses.

        ```
        # Example usage:
        projectal.Customer.create({'name': 'NewCustomer'})
        # returns Customer object
        ```
        """

        if isinstance(entities, dict):
            # Dict input needs to be a list
            e_list = [entities]
        else:
            # We have a list of dicts already, the expected format
            e_list = entities

        # Apply type
        typed_list = []
        for e in e_list:
            if not isinstance(e, Entity):
                # Start empty to correctly populate history
                new = cls({})
                new.update(e)
                typed_list.append(new)
            else:
                typed_list.append(e)
        e_list = typed_list

        endpoint = '/api/{}/add'.format(cls._path)
        if params:
            endpoint += params
        if not e_list:
            return []

        # Strip links from payload
        payload = []
        keys = e_list[0]._link_def_by_key.keys()
        for e in e_list:
            cleancopy = copy.deepcopy(e)
            # Remove any fields that match a link key
            for key in keys:
                cleancopy.pop(key, None)
            payload.append(cleancopy)

        objects = []
        for i in range(0, len(payload), projectal.chunk_size_write):
            chunk = payload[i:i + projectal.chunk_size_write]
            orig_chunk = e_list[i:i + projectal.chunk_size_write]
            response = api.post(endpoint, chunk)
            # Put uuId from response into each input dict
            for e, o, orig in zip(chunk, response, orig_chunk):
                orig['uuId'] = o['uuId']
                orig.__old = copy.deepcopy(orig)
                # Delete links from the history in order to trigger a change on them after
                for key in orig._link_def_by_key:
                    orig.__old.pop(key, None)
                objects.append(orig)

        # Detect and apply any link additions
        # if batch_linking is enabled, builds a list of link requests
        # needed for each entity, then executes them with composite
        # API requests
        link_request_batch = []
        for e in e_list:
            requests = e.__apply_link_changes(batch_linking=batch_linking)
            link_request_batch.extend(requests)

        if len(link_request_batch) > 0 and batch_linking:
            for i in range(0, len(link_request_batch), 1000):
                chunk = link_request_batch[i:i + 1000]
                api.post('/api/composite', chunk)

        if not isinstance(entities, list):
            return objects[0]
        return objects

    @classmethod
    def _get_linkset(cls, links):
        """Get a set of link names we have been asked to fetch with. Raise an
        error if the requested link is not valid for this Entity type."""
        link_set = set()
        if links is not None:
            if isinstance(links, str) or not hasattr(links, '__iter__'):
                raise projectal.UsageException("Parameter 'links' must be a list or None.")

            defs = cls({})._link_def_by_name
            for link in links:
                name = link.lower()
                if name not in defs:
                    raise projectal.UsageException(
                        "Link '{}' is invalid for {}".format(name, cls._name))
                link_set.add(name)
        return link_set

    @classmethod
    def get(cls, entities, links=None, deleted_at=None):
        """
        Get one or more entities of the same type. The entity
        type is determined by the subclass calling this method.

        `entities`: One of several formats containing the `uuId`s
        of the entities you want to get (see bottom for examples):

        - `str` or list of `str`
        - `dict` or list of `dict` (with `uuId` key)

        `links`: A case-insensitive list of entity names to fetch with
        this entity. For performance reasons, links are only returned
        on demand.

        Links follow a common naming convention in the output with
        a *_List* suffix. E.g.:
        `links=['company', 'location']` will appear as `companyList` and
        `locationList` in the response.
        ```
        # Example usage:
        # str
        projectal.Project.get('1b21e445-f29a-4a9f-95ff-fe253a3e1b11')

        # list of str
        ids = ['1b21e445-f29a...', '1b21e445-f29a...', '1b21e445-f29a...']
        projectal.Project.get(ids)

        # dict
        project = project.Project.create({'name': 'MyProject'})
        # project = {'uuId': '1b21e445-f29a...', 'name': 'MyProject', ...}
        projectal.Project.get(project)

        # list of dicts (e.g. from a query)
        # projects = [{'uuId': '1b21e445-f29a...'}, {'uuId': '1b21e445-f29a...'}, ...]
        project.Project.get(projects)

        # str with links
        projectal.Project.get('1b21e445-f29a...', 'links=['company', 'location']')
        ```

        `deleted_at`: Include this parameter to get a deleted entity.
        This value should be a UTC timestamp from a webhook delete event.
        """
        link_set = cls._get_linkset(links)

        if isinstance(entities, str):
            # String input is a uuId
            payload = [{'uuId': entities}]
        elif isinstance(entities, dict):
            # Dict input needs to be a list
            payload = [entities]
        elif isinstance(entities, list):
            # List input can be a list of uuIds or list of dicts
            # If uuIds (strings), convert to list of dicts
            if len(entities) > 0 and isinstance(entities[0], str):
                payload = [{'uuId': uuId} for uuId in entities]
            else:
                # Already expected format
                payload = entities
        else:
            # We have a list of dicts already, the expected format
            payload = entities

        if deleted_at:
            if not isinstance(deleted_at, int):
                raise projectal.UsageException("deleted_at must be a number")

        url = '/api/{}/get'.format(cls._path)
        params = []
        params.append('links={}'.format(','.join(links))) if links else None
        params.append('epoch={}'.format(deleted_at - 1)) if deleted_at else None
        if len(params) > 0:
            url += '?' + '&'.join(params)

        # We only need to send over the uuIds
        payload = [{'uuId': e['uuId']} for e in payload]
        if not payload:
            return []
        objects = []
        for i in range(0, len(payload), projectal.chunk_size_read):
            chunk = payload[i:i + projectal.chunk_size_read]
            dicts = api.post(url, chunk)
            for d in dicts:
                obj = cls(d)
                obj._with_links.update(link_set)
                obj._is_new = False
                # Create default fields for links we ask for. Workaround for backend
                # sometimes omitting links if no links exist.
                for link_name in link_set:
                    link_def = obj._link_def_by_name[link_name]
                    if link_def['link_key'] not in obj:
                        if link_def['type'] == dict:
                            obj.set_readonly(link_def['link_key'], None)
                        else:
                            obj.set_readonly(link_def['link_key'], link_def['type']())
                objects.append(obj)

        if not isinstance(entities, list):
            return objects[0]
        return objects

    def __get(self, *args, **kwargs):
        """Use the dict get for instances."""
        return super(Entity, self).get(*args, **kwargs)

    @classmethod
    def update(cls, entities, batch_linking=True):
        """
        Save one or more entities of the same type. The entity
        type is determined by the subclass calling this method.
        Only the fields that have been modifier will be sent
        to the server as part of the request.

        `entities`: Can be a `dict` to update a single entity,
        or a list of `dict`s to update many entities in bulk.

        'batch_linking': Enabled by default, batches any link
        updates required into composite API requests. If disabled
        a request will be executed for each link update.
        Recommended to leave enabled to increase performance.

        Returns `True` if all entities update successfully.

        ```
        # Example usage:
        rebate = projectal.Rebate.create({'name': 'Rebate2022', 'rebate': 0.2})
        rebate['name'] = 'Rebate2024'
        projectal.Rebate.update(rebate)
        # Returns True. New rebate name has been saved.
        ```
        """
        if isinstance(entities, dict):
            e_list = [entities]
        else:
            e_list = entities

        # Reduce the list to only modified entities and their modified fields.
        # Only do this to an Entity subclass - the consumer may have passed
        # in a dict of changes on their own.
        payload = []

        for e in e_list:
            if isinstance(e, Entity):
                changes = e._changes_internal()
                if changes:
                    changes['uuId'] = e['uuId']
                    payload.append(changes)
            else:
                payload.append(e)
        if payload:
            for i in range(0, len(payload), projectal.chunk_size_write):
                chunk = payload[i:i + projectal.chunk_size_write]
                api.put('/api/{}/update'.format(cls._path), chunk)

        # Detect and apply any link changes
        # if batch_linking is enabled, builds a list of link requests
        # from the changes of each entity, then executes
        # composite API requests with those changes
        link_request_batch = []
        for e in e_list:
            if isinstance(e, Entity):
                requests = e.__apply_link_changes(batch_linking=batch_linking)
                link_request_batch.extend(requests)

        if len(link_request_batch) > 0 and batch_linking:
            for i in range(0, len(link_request_batch), 1000):
                chunk = link_request_batch[i:i + 1000]
                api.post('/api/composite', chunk)

        return True

    def __update(self, *args, **kwargs):
        """Use the dict update for instances."""
        return super(Entity, self).update(*args, **kwargs)

    def save(self):
        """Calls `update()` on this instance of the entity, saving
        it to the database."""
        return self.__class__.update(self)

    @classmethod
    def delete(cls, entities):
        """
        Delete one or more entities of the same type. The entity
        type is determined by the subclass calling this method.

        `entities`: See `Entity.get()` for expected formats.

        ```
        # Example usage:
        ids = ['1b21e445-f29a...', '1b21e445-f29a...', '1b21e445-f29a...']
        projectal.Customer.delete(ids)
        ```
        """
        if isinstance(entities, str):
            # String input is a uuId
            payload = [{'uuId': entities}]
        elif isinstance(entities, dict):
            # Dict input needs to be a list
            payload = [entities]
        elif isinstance(entities, list):
            # List input can be a list of uuIds or list of dicts
            # If uuIds (strings), convert to list of dicts
            if len(entities) > 0 and isinstance(entities[0], str):
                payload = [{'uuId': uuId} for uuId in entities]
            else:
                # Already expected format
                payload = entities
        else:
            # We have a list of dicts already, the expected format
            payload = entities

        # We only need to send over the uuIds
        payload = [{'uuId': e['uuId']} for e in payload]
        if not payload:
            return True
        for i in range(0, len(payload), projectal.chunk_size_write):
            chunk = payload[i:i + projectal.chunk_size_write]
            api.delete('/api/{}/delete'.format(cls._path), chunk)
        return True

    def __delete(self):
        """Let an instance delete itself."""
        return self.__class__.delete(self)

    def clone(self, entity):
        """
        Clones an entity and returns its `uuId`.

        Each entity has its own set of required values when cloning.
        Check the API documentation of that entity for details.
        """
        url = '/api/{}/clone?reference={}'.format(self._path, self['uuId'])
        response = api.post(url, entity)
        return response['jobClue']['uuId']

    @classmethod
    def history(cls, UUID, start=0, limit=-1, order='desc', epoch=None, event=None):
        """
        Returns an ordered list of all changes made to the entity.

        `UUID`: the UUID of the entity.

        `start`: Start index for pagination (default: `0`).

        `limit`: Number of results to include for pagination. Use
        `-1` to return the entire history (default: `-1`).

        `order`: `asc` or `desc` (default: `desc` (index 0 is newest))

        `epoch`: only return the history UP TO epoch date

        `event`:
        """
        url = '/api/{}/history?holder={}&'.format(cls._path, UUID)
        params = []
        params.append('start={}'.format(start))
        params.append('limit={}'.format(limit))
        params.append('order={}'.format(order))
        params.append('epoch={}'.format(epoch)) if epoch else None
        params.append('event={}'.format(event)) if event else None
        url += '&'.join(params)
        return api.get(url)

    def __history(self, **kwargs):
        """Get history of instance."""
        return self.__class__.history(self['uuId'], **kwargs)

    @classmethod
    def list(cls, expand=False, links=None):
        """Return a list of all entity UUIDs of this type.

        You may pass in `expand=True` to get full Entity objects
        instead, but be aware this may be very slow if you have
        thousands of objects.

        If you are expanding the objects, you may further expand
        the results with `links`.
        """

        payload = {
            "name": "List all entities of type {}".format(cls._name.upper()),
            "type": "msql", "start": 0, "limit": -1,
            "select": [
                ["{}.uuId".format(cls._name.upper())]
            ],
        }
        ids = api.query(payload)
        ids = [id[0] for id in ids]
        if ids:
            return cls.get(ids, links=links) if expand else ids
        return []

    @classmethod
    def match(cls, field, term, links=None):
        """Find entities where `field`=`term` (exact match), optionally
        expanding the results with `links`.

        Relies on `Entity.query()` with a pre-built set of rules.
        ```
        projects = projectal.Project.match('identifier', 'zmb-005')
        ```
        """
        filter = [["{}.{}".format(cls._name.upper(), field), "eq", term]]
        return cls.query(filter, links)

    @classmethod
    def match_startswith(cls, field, term, links=None):
        """Find entities where `field` starts with the text `term`,
        optionally expanding the results with `links`.

        Relies on `Entity.query()` with a pre-built set of rules.
        ```
        projects = projectal.Project.match_startswith('name', 'Zomb')
        ```
        """
        filter = [["{}.{}".format(cls._name.upper(), field), "prefix", term]]
        return cls.query(filter, links)

    @classmethod
    def match_endswith(cls, field, term, links=None):
        """Find entities where `field` ends with the text `term`,
        optionally expanding the results with `links`.

        Relies on `Entity.query()` with a pre-built set of rules.
        ```
        projects = projectal.Project.match_endswith('identifier', '-2023')
        ```
        """
        term = "(?i).*{}$".format(term)
        filter = [["{}.{}".format(cls._name.upper(), field), "regex", term]]
        return cls.query(filter, links)

    @classmethod
    def match_one(cls, field, term, links=None):
        """Convenience function for match(). Returns the first match or None."""
        matches = cls.match(field, term, links)
        if matches:
            return matches[0]

    @classmethod
    def match_startswith_one(cls, field, term, links=None):
        """Convenience function for match_startswith(). Returns the first match or None."""
        matches = cls.match_startswith(field, term, links)
        if matches:
            return matches[0]

    @classmethod
    def match_endswith_one(cls, field, term, links=None):
        """Convenience function for match_endswith(). Returns the first match or None."""
        matches = cls.match_endswith(field, term, links)
        if matches:
            return matches[0]

    @classmethod
    def search(cls, fields=None, term='', case_sensitive=True, links=None):
        """Find entities that contain the text `term` within `fields`.
        `fields` is a list of field names to target in the search.

        `case_sensitive`: Optionally turn off case sensitivity in the search.

        Relies on `Entity.query()` with a pre-built set of rules.
        ```
        projects = projectal.Project.search(['name', 'description'], 'zombie')
        ```
        """
        filter = []
        term = '(?{}).*{}.*'.format('' if case_sensitive else '?', term)
        for field in fields:
            filter.append(["{}.{}".format(cls._name.upper(), field), "regex", term])
        filter = ['_or_', filter]
        return cls.query(filter, links)

    @classmethod
    def query(cls, filter, links=None):
        """Run a query on this entity with the supplied filter.

        The query is already set up to target this entity type, and the
        results will be converted into full objects when found, optionally
        expanded with the `links` provided. You only need to supply a
        filter to reduce the result set.

        See [the filter documentation](https://projectal.com/docs/v1.1.1#section/Filter-section)
        for a detailed overview of the kinds of filters you can construct.
        """
        payload = {
            "name": "Python library entity query ({})".format(cls._name.upper()),
            "type": "msql", "start": 0, "limit": -1,
            "select": [
                ["{}.uuId".format(cls._name.upper())]
            ],
            "filter": filter
        }
        ids = api.query(payload)
        ids = [id[0] for id in ids]
        if ids:
            return cls.get(ids, links=links)
        return []

    def profile_get(self, key):
        """Get the profile (metadata) stored for this entity at `key`."""
        return projectal.profile.get(key, self.__class__._name.lower(), self['uuId'])

    def profile_set(self, key, data):
        """Set the profile (metadata) stored for this entity at `key`. The contents
        of `data` will completely overwrite the existing data dictionary."""
        return projectal.profile.set(key, self.__class__._name.lower(), self['uuId'], data)

    def __type_links(self):
        """Find links and turn their dicts into typed objects matching their Entity type."""

        for key, _def in self._link_def_by_key.items():
            if key in self:
                cls = getattr(projectal, _def['entity'])
                if _def['type'] == list:
                    as_obj = []
                    for link in self[key]:
                        as_obj.append(cls(link))
                elif _def['type'] == dict:
                    as_obj = cls(self[key])
                else:
                    raise projectal.UsageException("Unexpected link type")
                self[key] = as_obj

    def changes(self):
        """Return a dict containing the fields that have changed since fetching the object.
        Dict values contain both the old and new values. E.g.: {'old': 'original', 'new': 'current'}.

        In the case of link lists, there are three values: added, removed, updated. Only links with
        a data attribute can end up in the updated list, and the old/new dictionary is placed within
        that data attribute. E.g. for a staff-resource link:
        'updated': [{
            'uuId': '24eb4c31-0f92-49d1-8b4d-507ab939003e',
            'resourceLink': {'quantity': {'old': 2, 'new': 5}}
        }]
        """
        changed = {}
        for key in self.keys():
            link_def = self._link_def_by_key.get(key)
            if link_def:
                changes = self._changes_for_link_list(link_def, key)
                # Only add it if something in it changed
                for action in changes.values():
                    if len(action):
                        changed[key] = changes
                        break
            elif key not in self.__old and self[key] is not None:
                changed[key] = {'old': None, 'new': self[key]}
            elif self.__old.get(key) != self[key]:
                changed[key] = {'old': self.__old.get(key), 'new': self[key]}
        return changed

    def _changes_for_link_list(self, link_def, key):
        changes = self.__apply_list(link_def, report_only=True)
        data_key = link_def['data_name']

        # For linked entities, we will only report their UUID, name (if it has one),
        # and the content of their data attribute (if it has one).
        def get_slim_list(entities):
            slim = []
            if isinstance(entities, dict):
                entities = [entities]
            for e in entities:
                fields = {'uuId': e['uuId']}
                name = e.get('name')
                if name:
                    fields['name'] = e['name']
                if data_key and e[data_key]:
                    fields[data_key] = e[data_key]
                slim.append(fields)
            return slim

        out = {
            'added': get_slim_list(changes.get('add', [])),
            'updated': [],
            'removed': get_slim_list(changes.get('remove', [])),
        }

        updated = changes.get('update', [])
        if updated:
            before_map = {}
            for entity in self.__old.get(key):
                before_map[entity['uuId']] = entity

            for entity in updated:
                old_data = before_map[entity['uuId']][data_key]
                new_data = entity[data_key]
                diff = {}
                for key in new_data.keys():
                    if key not in old_data and new_data[key] is not None:
                        diff[key] = {'old': None, 'new': new_data[key]}
                    elif old_data.get(key) != new_data[key]:
                        diff[key] = {'old': old_data.get(key), 'new': new_data[key]}
                out['updated'].append({'uuId': entity['uuId'], data_key: diff})
        return out

    def _changes_internal(self):
        """Return a dict containing only the fields that have changed and their current value,
        without any link data.

        This method is used internally to strip payloads down to only the fields that have changed.
        """
        changed = {}
        for key in self.keys():
            # We don't deal with link or link data changes here. We only want standard fields.
            if key in self._link_def_by_key:
                continue
            if key not in self.__old and self[key] is not None:
                changed[key] = self[key]
            elif self.__old.get(key) != self[key]:
                changed[key] = self[key]
        return changed

    def set_readonly(self, key, value):
        """Set a field on this Entity that will not be sent over to the
        server on update unless modified."""
        self[key] = value
        self.__old[key] = value

    # --- Link management ---

    @staticmethod
    def __link_data_differs(have_link, want_link, data_key):

        if data_key:
            if 'uuId' in have_link[data_key]:
                del have_link[data_key]['uuId']
            if 'uuId' in want_link[data_key]:
                del want_link[data_key]['uuId']
            return have_link[data_key] != want_link[data_key]

        # Links without data never differ
        return False

    def __apply_link_changes(self, batch_linking=True):
        """Send each link list to the conflict resolver. If we detect
        that the entity was not fetched with that link, we do the fetch
        first and use the result as the basis for comparison."""

        # Find which lists belong to links but were not fetched so we can fetch them
        need = []
        find_list = []
        if not self._is_new:
            for link in self._link_def_by_key.values():
                if link['link_key'] in self and link['name'] not in self._with_links:
                    need.append(link['name'])
                    find_list.append(link['link_key'])

        if len(need):
            logging.warning("Entity links were modified but entity not fetched with links. "
                            "For better performance, include the links when getting the entity.")
            logging.warning("Fetching {} again with missing links: {}".format(self._name.upper(), ','.join(need)))
            new = self.__fetch(self, links=need)
            for _list in find_list:
                self.__old[_list] = copy.deepcopy(new.get(_list, []))

        # if batch_linking is enabled, builds a list of link requests
        # for each link definition of the calling entity then returns the list
        request_list = []
        for link_def in self._link_def_by_key.values():
            link_def_requests = self.__apply_list(link_def, batch_linking=batch_linking)
            if batch_linking:
                request_list.extend(link_def_requests)
        return request_list

    def __apply_list(self, link_def, report_only=False, batch_linking=True):
        """Automatically resolve differences and issue the correct sequence of
        link/unlink/relink for the link list to result in the supplied list
        of entities.

        report_only will not make any changes to the data or issue network requests.
        Instead, it returns the three lists of changes (add, update, delete).
        """
        to_add = []
        to_remove = []
        to_update = []
        should_only_have = set()
        link_key = link_def['link_key']

        if link_def['type'] == list:
            want_entities = self.get(link_key, [])
            have_entities = self.__old.get(link_key, [])

            if not isinstance(want_entities, list):
                raise api.UsageException("Expecting '{}' to be {}. Found {} instead.".format(
                    link_key, link_def['type'].__name__, type(want_entities).__name__))

            for want_entity in want_entities:
                if want_entity['uuId'] in should_only_have:
                    raise api.UsageException("Duplicate {} in {}".format(link_def['name'], link_key))
                should_only_have.add(want_entity['uuId'])
                have = False
                for have_entity in have_entities:
                    if have_entity['uuId'] == want_entity['uuId']:
                        have = True
                        data_name = link_def.get('data_name')
                        if data_name and self.__link_data_differs(have_entity, want_entity, data_name):
                            to_update.append(want_entity)
                if not have:
                    to_add.append(want_entity)
            for have_entity in have_entities:
                if have_entity['uuId'] not in should_only_have:
                    to_remove.append(have_entity)
        elif link_def['type'] == dict:
            # Note: dict type does not implement updates as we have no dict links
            # that support update (yet?).
            want_entity = self.get(link_key, None)
            have_entity = self.__old.get(link_key, None)

            if want_entity is not None and not isinstance(want_entity, dict):
                raise api.UsageException("Expecting '{}' to be {}. Found {} instead.".format(
                    link_key, link_def['type'].__name__, type(have_entity).__name__))

            if want_entity:
                if have_entity:
                    if want_entity['uuId'] != have_entity['uuId']:
                        to_remove = have_entity
                        to_add = want_entity
                else:
                    to_add = want_entity
            if not want_entity:
                if have_entity:
                    to_remove = have_entity

            want_entities = want_entity
        else:
            # Would be an error in this library if we reach here
            raise projectal.UnsupportedException("This type does not support linking")

        # if batch_linking is enabled, builds a list of requests
        # from each link method
        if not report_only:
            request_list = []
            if to_remove:
                delete_requests = self._link(
                        link_def['name'], to_remove, 'delete',
                        update_cache=False, batch_linking=batch_linking
                )
                request_list.extend(delete_requests)
            if to_update:
                update_requests = self._link(
                    link_def['name'], to_update, 'update',
                    update_cache=False, batch_linking=batch_linking
                )
                request_list.extend(update_requests)
            if to_add:
                add_requests = self._link(
                    link_def['name'], to_add, 'add',
                    update_cache=False, batch_linking=batch_linking
                )
                request_list.extend(add_requests)
            self.__old[link_key] = copy.deepcopy(want_entities)
            return request_list
        else:
            changes = {}
            if to_remove:
                changes['remove'] = to_remove
            if to_update:
                changes['update'] = to_update
            if to_add:
                changes['add'] = to_add
            return changes

    @classmethod
    def get_link_definitions(cls):
        return cls({})._link_def_by_name
    # --- ---

    def entity_name(self):
        return self._name.capitalize()
