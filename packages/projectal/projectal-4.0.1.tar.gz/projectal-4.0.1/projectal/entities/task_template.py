from projectal import api
from projectal.entity import Entity
from projectal.linkers import *


class TaskTemplate(Entity, ResourceLinker, SkillLinker, FileLinker, StaffLinker, RebateLinker,
                   NoteLinker, TagLinker):
    """
    Implementation of the
    [Task Template](https://projectal.com/docs/latest/#tag/Task-Template) API.
    """
    _path = 'template/task'
    _name = 'task_template'
    _links = [ResourceLinker, SkillLinker, FileLinker, StaffLinker, RebateLinker,
              NoteLinker, TagLinker]

    def clone(self, holder, entity):
        url = '/api/template/task/clone?holder={}&reference={}'\
            .format(holder['uuId'], self['uuId'])
        response = api.post(url, entity)
        return response['jobClue']['uuId']

    @classmethod
    def create(cls, holder, entity):
        """Create a Task Template

        `holder`: `uuId` of the owner

        `entity`: The fields of the entity to be created
        """
        holder = holder['uuId'] if isinstance(holder, dict) else holder
        params = "?holder=" + holder
        return super().create(entity, params)

    @classmethod
    def link_predecessor_task(cls, task, predecessor_task):
        return cls.__plan(task, predecessor_task, 'add')

    @classmethod
    def relink_predecessor_task(cls, task, predecessor_task):
        return cls.__plan(task, predecessor_task, 'update')

    @classmethod
    def unlink_predecessor_task(cls, task, predecessor_task):
        return cls.__plan(task, predecessor_task, 'delete')

    @classmethod
    def __plan(cls, from_task, to_task, operation):
        url = '/api/template/task/plan/task/{}'.format(operation)
        payload = {
            'uuId': from_task['uuId'],
            'taskList': [to_task]
        }
        api.post(url, payload=payload)
        return True
