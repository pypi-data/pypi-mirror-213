from projectal.entity import Entity
from projectal.linkers import *


class Resource(Entity, StaffLinker, TaskLinker, TaskTemplateLinker, NoteLinker,
               TagLinker):
    """
    Implementation of the [Resource](https://projectal.com/docs/latest/#tag/Resource) API.
    """
    _path = 'resource'
    _name = 'resource'
    _links = [NoteLinker, TagLinker]
    _links_reverse = [StaffLinker, TaskLinker, TaskTemplateLinker]
