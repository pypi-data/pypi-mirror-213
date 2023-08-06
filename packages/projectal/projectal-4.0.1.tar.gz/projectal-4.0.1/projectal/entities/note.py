import copy

import projectal
from projectal.entity import Entity
from projectal.linkers import *

class Note(Entity, TagLinker):
    """
    Implementation of the [Note](https://projectal.com/docs/latest/#tag/Note) API.
    """
    _path = 'note'
    _name = 'note'
    _links = [TagLinker]  # TODO: user?

    @classmethod
    def create(cls, holder, entity):
        """Create a Note

        `holder`: `uuId` of the owner

        `entity`: The fields of the entity to be created
        """
        holder_id = holder['uuId'] if isinstance(holder, dict) else holder
        params = "?holder=" + holder_id
        out = super().create(entity, params)
        # Notes use "empty linkers" during creation which don't go through our
        # usual linker pipeline where the internal list is updated. Do it here
        # manually.
        if isinstance(holder, Entity):
            nl = holder.get('noteList', [])
            nl.append(out)
            holder.set_readonly('noteList', copy.deepcopy(nl))

        # Notes contain references to the objects that made and hold them. We don't get this
        # information from the creation api method, but we can insert them ourselves because
        # we know what they are.
        time = projectal.response_timestamp
        def add_fields(obj):
            obj.set_readonly('created', time)
            obj.set_readonly('modified', time)
            obj.set_readonly('author', projectal.api_auth_details.get('name'))
            obj.set_readonly('authorRef', projectal.api_auth_details.get('uuId'))
            obj.set_readonly('holderRef', holder_id)
            tag = None
            if isinstance(holder, Entity):
                tag = holder._name.upper()
            obj.set_readonly('holderTag', tag)

        if isinstance(out, dict):
            add_fields(out)
        if isinstance(out, list):
            for obj in out:
                add_fields(obj)
        return out
