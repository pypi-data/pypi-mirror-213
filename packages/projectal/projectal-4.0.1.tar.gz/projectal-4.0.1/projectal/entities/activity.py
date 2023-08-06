from projectal.entity import Entity
from projectal.linkers import *


class Activity(Entity, ContactLinker, LocationLinker, RebateLinker,
               ResourceLinker, StaffLinker, StageLinker, TagLinker):
    """
    Implementation of the [Activity](https://projectal.com/docs/latest/#tag/Activity) API.
    """
    _path = 'activity'
    _name = 'activity'
    _links = [ContactLinker, LocationLinker, RebateLinker,
              ResourceLinker, StaffLinker, StageLinker, TagLinker]