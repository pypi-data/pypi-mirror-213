from projectal.entity import Entity
from projectal.linkers import *


class Stage(Entity, ProjectLinker, TaskLinker, TagLinker):
    """
    Implementation of the [Stage](https://projectal.com/docs/latest/#tag/Stage) API.
    """
    _path = 'stage'
    _name = 'stage'
    _links = [TagLinker]
    _links_reverse = [ProjectLinker, TaskLinker]
