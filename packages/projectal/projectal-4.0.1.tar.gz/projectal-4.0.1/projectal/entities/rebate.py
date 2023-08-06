from projectal.entity import Entity
from projectal.linkers import *


class Rebate(Entity, ProjectLinker, TaskLinker, TaskTemplateLinker, NoteLinker,
             TagLinker):
    """
    Implementation of the [Rebate](https://projectal.com/docs/latest/#tag/Rebate) API.
    """
    _path = 'rebate'
    _name = 'rebate'
    _links = [NoteLinker, TagLinker]
    _links_reverse = [ProjectLinker, TaskLinker, TaskTemplateLinker]
