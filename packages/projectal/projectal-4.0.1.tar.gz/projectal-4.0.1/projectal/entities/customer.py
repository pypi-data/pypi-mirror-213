from projectal.entity import Entity
from projectal.linkers import *


class Customer(Entity, LocationLinker, ContactLinker, FileLinker, ProjectLinker, NoteLinker,
               TagLinker):
    """
    Implementation of the [Customer](https://projectal.com/docs/latest/#tag/Customer) API.
    """
    _path = 'customer'
    _name = 'customer'
    _links = [LocationLinker, ContactLinker, FileLinker, NoteLinker, TagLinker]
    _links_reverse = [ProjectLinker]
