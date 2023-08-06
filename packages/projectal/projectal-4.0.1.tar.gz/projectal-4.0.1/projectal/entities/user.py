from projectal import api
from projectal.entity import Entity
from projectal.linkers import *


class User(Entity, AccessPolicyLinker, PermissionLinker, NoteLinker, TagLinker):
    """
    Implementation of the [User](https://projectal.com/docs/latest/#tag/User) API.
    """
    _path = 'user'
    _name = 'user'
    _links = [AccessPolicyLinker, PermissionLinker, NoteLinker, TagLinker]

    def register(self):
        url = '/api/user/registration/{}'.format(self['uuId'])
        return api.post(url)

    def set_password(self, password, token_id):
        url = '/auth/register/password'
        payload = {
            'password': password,
            'confirm': password,
            'tokenId': token_id
        }
        api.post(url, payload=payload)
        return True

    @classmethod
    def current_user_permissions(cls):
        """
        Get the authenticated user's permissions as a list.
        """
        return api.get('/api/user/permissions')['permissions']

    def link_permission(self, permissions):
        self.__permission(self, permissions, 'add')

    def unlink_permission(self, permissions):
        self.__permission(self, permissions, 'delete')

    @classmethod
    def __permission(cls, from_user, to_permissions, operation):
        if isinstance(to_permissions, dict):
            to_permissions = [to_permissions]

        url = '/api/user/permission/{}'.format(operation)
        payload = [{
            'uuId': from_user['uuId'],
            'permissionList': to_permissions
        }]
        api.post(url, payload=payload)
        return True

    @classmethod
    def current_user_details(cls):
        """Get some details about the authenticated user."""
        return api.get('/api/user/details')

    @classmethod
    def get_permissions(cls, user):
        """Get the permissions assigned to a specific User entity."""
        url = '/api/user/get/{}/permissions'.format(user['uuId'])
        return api.get(url)['data']
