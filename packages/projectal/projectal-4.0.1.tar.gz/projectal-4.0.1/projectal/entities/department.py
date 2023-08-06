from projectal.entity import Entity
from projectal import api
from projectal.linkers import *


class Department(Entity, StaffLinker, DepartmentLinker, CompanyLinker, NoteLinker,
                 TagLinker):
    """
    Implementation of the [Department](https://projectal.com/docs/latest/#tag/Department) API.
    """
    _path = 'department'
    _name = 'department'
    _links = [StaffLinker, DepartmentLinker, NoteLinker, TagLinker]
    _links_reverse = [CompanyLinker]

    @staticmethod
    def tree(holder=None, level=None, active_staff=True, inactive_staff=True,
             generic_staff=False):
        """
        Return department list in tree format

        `holder`: Project, Company, or Staff. If None, the full department chart
        is returned (default: `None`)

        `level`: If `True`, only returns the top level of the
        hierarchy (default: `False`)

        `active_staff`: If `True`, includes the list of staff in each
        department who are considered 'active' (i.e, today is within
        their start and end dates) (default: `True`)

        'inactive_staff`: If `True`, includes the list of staff in each
        department who are considered 'inactive' (i.e, today is outside
        their start and end dates) (default: `True`)

        `generic_staff`: Include generic staff in results
        """
        url = '/api/department/tree?'
        params = []
        params.append('uuId={}'.format(holder['uuId'])) if holder else None
        params.append('level=true') if level else None
        params.append('activeStaff={}'.format('true' if active_staff else 'false'))
        params.append('inactiveStaff={}'.format('true' if inactive_staff else 'false'))
        params.append('genericStaff={}'.format('true' if generic_staff else 'false'))
        url += '&'.join(params)

        return api.get(url)

