from projectal.entity import Entity
from projectal.linkers import PermissionLinker, UserLinker


class AccessPolicy(Entity, PermissionLinker, UserLinker):
    """
    Implementation of the [Access Policy](https://projectal.com/docs/latest/#tag/Access-Policy) API.
    """
    _path = 'access-policy'
    _name = 'access_policy'

    _links = [PermissionLinker]
    _links_reverse = [UserLinker]
