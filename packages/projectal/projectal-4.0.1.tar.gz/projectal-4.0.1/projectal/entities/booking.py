from projectal.entity import Entity
from projectal.linkers import *


class Booking(Entity, StageLinker, TagLinker):
    """
    Implementation of the [Booking](https://projectal.com/docs/latest/#tag/Booking) API.
    """
    _path = 'booking'
    _name = 'booking'
    _links = [StageLinker, TagLinker]