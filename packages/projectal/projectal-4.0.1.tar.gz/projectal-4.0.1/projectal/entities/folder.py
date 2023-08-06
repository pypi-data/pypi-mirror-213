from projectal.entity import Entity
from projectal.linkers import *
from projectal import api


class Folder(Entity, FileLinker, FolderLinker, NoteLinker, TagLinker):
    """
    Implementation of the [Folder](https://projectal.com/docs/latest/#tag/Folder) API.
    """
    _path = 'folder'
    _name = 'folder'
    _links = [FileLinker, FolderLinker, NoteLinker, TagLinker]

    def __init__(self, data):
        super().__init__(data)

        # TODO: override linker definition here due to differences in list name vs other file linkers.
        # Remove if/when API is changed to address this.
        class CustomFile(BaseLinker):
            _link_name = 'file'
            _link_key = 'files'
        self._add_link_def(CustomFile)

    @classmethod
    def create(cls, entity):
        payload = entity
        endpoint = '/api/folder/add'
        response = api.post(endpoint, payload)
        entity['uuId'] = response['jobClue']['uuId']
        return cls(entity)

    @classmethod
    def get(cls, uuId, links=None):
        """Get the File entity. No file data is included."""
        link_set = cls._get_linkset(links)
        url = '/api/folder/get?uuId={}'.format(uuId)
        if link_set:
            url += '&links=' + ','.join(link_set)
        return cls(api.get(url))

    @classmethod
    def update(cls, entity):
        payload = entity
        api.put('/api/folder/update', payload)
        return True

    @classmethod
    def delete(cls, uuId):
        api.delete('/api/folder/delete/{}'.format(uuId))
        return True


    @classmethod
    def list(cls, expand=True):
        """Return all folders as a list"""
        folders = api.get('/api/folder/list')
        return [cls(f) for f in folders]
