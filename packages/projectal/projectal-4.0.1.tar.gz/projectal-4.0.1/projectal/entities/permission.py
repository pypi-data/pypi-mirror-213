from projectal.entity import Entity
from projectal.linkers import *
from projectal import api

class Permission(Entity, UserLinker, AccessPolicyLinker):
    """
    Implementation of the [Permission](https://projectal.com/docs/latest/#tag/Permission) API.
    """
    _path = 'permission'
    _name = 'permission'
    _links_reverse = [UserLinker, AccessPolicyLinker]


    @classmethod
    def list(cls):
        url = '/api/permission/list?start=0&limit=-1'
        response = api.get(url)
        perms = {}
        for perm in response:
            perms[perm['name']] = Permission(perm)
        return perms
