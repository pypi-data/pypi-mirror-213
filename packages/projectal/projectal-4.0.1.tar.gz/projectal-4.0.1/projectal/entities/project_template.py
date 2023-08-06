from projectal import api
from projectal.entity import Entity
from projectal.linkers import *

class ProjectTemplate(Entity, NoteLinker, TagLinker):
    """
    Implementation of the
    [Project Template](https://projectal.com/docs/latest/#tag/Project-Template) API.
    """
    _path = 'template/project'
    _name = 'project_template'
    _links = [NoteLinker, TagLinker]

    @classmethod
    def autoschedule(cls, project, mode='ASAP'):
        """
        Autoschedule the project template.

        `project`: A ProjectTemplate entity

        `mode`: `ASAP` or `ALAP`
        """
        url = '/api/template/project/schedule?mode={}'.format(mode)
        api.post(url, [project])
        return True
