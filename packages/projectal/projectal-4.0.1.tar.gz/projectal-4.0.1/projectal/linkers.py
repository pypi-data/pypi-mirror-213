"""
Linkers provide the interface to add/update/delete links between entities.
Only certain entities can link to certain other entities. When using this
library, your tooling should show you which link methods are available
to the Entity subclass you are using.

Note that some links require additional data in the link. You must ensure
the destination object has this data before adding or updating the link
(example below). See the API documentation for exact link details.
Missing data will raise a `projectal.errors.ProjectalException` with
information about what is missing.


An instance of an entity class that inherits from a linker is able to link
to an instance of the target entity class directly.

```
# Get task and staff
task = projectal.Task.get('1b21e445-f29a...')
staff = projectal.Staff.get('1b21e445-f29a...')

# Task-to-Staff links require a 'resourceLink'
staff['resourceLink'] = {'utilization': 0.6}

# Task inherits from StaffLinker, so staff linking available
task.link_staff(staff)
```

"""

from projectal import api

class BaseLinker:
    # _link_name is the link name (usually the entity name)
    _link_name = None

    # _link_key is the key within the source object that points to the
    # links. E.g., 'skillList'
    _link_key = None

    # _link_data_name is the key within the linked (target) object that points
    # to a store of custom values within that link. E.g, Skill objects,
    # when linked, have a 'skillLink' property that holds data about
    # the link.
    _link_data_name = None

    # _link_type is the data type of the value in entity[link_key]. This is
    # usually a list since most links appear as 'skillList', 'staffList',
    # etc. But some links are single-entity only and appear as dicts like
    # project[stage] = Stage.
    _link_type = list

    # _link_entity is the string name (capitalized, like Stage) of the Entity
    # class within this library that fetched links will be converted to.
    # This is useful when the name of the list differs from the entity
    # name. E.g: stage_list needs to be converted to Stage.
    _link_entity = None

class AccessPolicyLinker(BaseLinker):
    """Subclass can link to Access Policies"""
    _link_name = 'access_policy'
    _link_key = 'accessPolicyList'
    _link_entity = 'AccessPolicy'

    def link_access_policy(self, access_policies):
        self._add_link('access_policy', access_policies)

    def unlink_access_policy(self, access_policies):
        self._delete_link('access_policy', access_policies)


class CompanyLinker(BaseLinker):
    """Subclass can link to Companies"""
    _link_name = 'company'

    def link_company(self, companies):
        self._add_link('company', companies)

    def unlink_company(self, companies):
        self._delete_link('company', companies)


class ContactLinker(BaseLinker):
    """Subclass can link to Contacts"""
    _link_name = 'contact'

    def link_contact(self, contacts):
        self._add_link('contact', contacts)

    def unlink_contact(self, contacts):
        self._delete_link('contact', contacts)


class CustomerLinker(BaseLinker):
    """Subclass can link to Customers"""
    _link_name = 'customer'

    def link_customer(self, customers):
        self._add_link('customer', customers)

    def unlink_customer(self, customers):
        self._delete_link('customer', customers)


class DepartmentLinker(BaseLinker):
    """Subclass can link to Departments"""
    _link_name = 'department'

    def link_department(self, departments):
        self._add_link('department', departments)

    def unlink_department(self, departments):
        self._delete_link('department', departments)


class FileLinker(BaseLinker):
    """Subclass can link to Files"""
    _link_name = 'file'
    _link_key = 'storageFileList'

    def link_file(self, files):
        self._add_link('file', files)

    def unlink_file(self, files):
        self._delete_link('file', files)


class FolderLinker(BaseLinker):
    """Subclass can link to Folders"""
    _link_name = 'folder'
    _link_key = 'folders'

    def link_folder(self, folders):
        self._add_link('folder', folders)

    def unlink_folder(self, folders):
        self._delete_link('folder', folders)


class LocationLinker(BaseLinker):
    """Subclass can link to Locations"""
    _link_name = 'location'

    def link_location(self, locations):
        self._add_link('location', locations)

    def unlink_location(self, locations):
        self._delete_link('location', locations)


class PermissionLinker(BaseLinker):
    """Subclass can link to Permissions"""
    _link_name = 'permission'

    def link_permission(self, permissions):
        return self._add_link('permission', permissions)

    def unlink_permission(self, permissions):
        return self._delete_link('permission', permissions)


class ProjectLinker(BaseLinker):
    """Subclass can link to Projects"""
    _link_name = 'project'

    def link_project(self, projects):
        self._add_link('project', projects)

    def unlink_project(self, projects):
        self._delete_link('project', projects)


class RebateLinker(BaseLinker):
    """Subclass can link to Rebates"""
    _link_name = 'rebate'

    def link_rebate(self, rebates):
        self._add_link('rebate', rebates)

    def unlink_rebate(self, rebates):
        self._delete_link('rebate', rebates)


class ResourceLinker(BaseLinker):
    """Subclass can link to Resources"""
    _link_name = 'resource'
    _link_data_name = 'resourceLink'

    def link_resource(self, resources):
        self._add_link('resource', resources)

    def relink_resource(self, resources):
        self._update_link('resource', resources)

    def unlink_resource(self, resources):
        self._delete_link('resource', resources)


class SkillLinker(BaseLinker):
    """Subclass can link to Skills"""
    _link_name = 'skill'
    _link_data_name = 'skillLink'

    def link_skill(self, skills):
        self._add_link('skill', skills)

    def relink_skill(self, skills):
        self._update_link('skill', skills)

    def unlink_skill(self, skills):
        self._delete_link('skill', skills)


class StaffLinker(BaseLinker):
    """Subclass can link to Staff"""
    _link_name = 'staff'
    _link_data_name = 'resourceLink'

    def link_staff(self, staffs):
        self._add_link('staff', staffs)

    def relink_staff(self, staffs):
        self._update_link('staff', staffs)

    def unlink_staff(self, staffs):
        self._delete_link('staff', staffs)


class StageLinker(BaseLinker):
    """Subclass can link to Stages"""
    _link_name = 'stage'
    _link_key = 'stage'
    _link_type = dict

    def link_stage(self, stages):
        self._add_link('stage', stages)

    def unlink_stage(self, stages):
        self._delete_link('stage', stages)


class StageListLinker(BaseLinker):
    """Subclass can link to Stage List"""
    _link_name = 'stage_list'
    _link_key = 'stageList'
    _link_entity = 'Stage'

    def link_stage_list(self, stages):
        if not isinstance(stages, list):
            raise api.UsageException('Stage list link must be a list')
        self._add_link('stage_list', stages)

    def unlink_stage_list(self, stages):
        if not isinstance(stages, list):
            raise api.UsageException('Stage list unlink must be a list')
        stages = [{'uuId': s['uuId']} for s in stages]
        self._delete_link('stage_list', stages)


class UserLinker(BaseLinker):
    _link_name = 'user'

    def link_user(self, users):
        self._add_link('user', users)

    def unlink_user(self, users):
        self._delete_link('user', users)


class TaskLinker(BaseLinker):
    _link_name = 'task'

    def link_task(self, tasks):
        self._add_link('task', tasks)

    def unlink_task(self, tasks):
        self._delete_link('task', tasks)


class TaskTemplateLinker(BaseLinker):
    _link_name = 'task_template'
    _link_entity = 'TaskTemplate'

    def link_task_template(self, task_templates):
        self._add_link('task_template', task_templates)

    def unlink_task_template(self, task_templates):
        self._delete_link('task_template', task_templates)

class TagLinker(BaseLinker):
    _link_name = 'tag'

    def link_tag(self, tags):
        self._add_link('tag', tags)

    def unlink_tag(self, tags):
        self._delete_link('tag', tags)

class NoteLinker(BaseLinker):
    _link_name = 'note'

class CalendarLinker(BaseLinker):
    _link_name = 'calendar'

# Projects have a list of tasks that we can fetch using the links=
# method, but they have no linker methods available.
class TaskInProjectLinker(BaseLinker):
    _link_name = "task"
