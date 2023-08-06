from projectal.entity import Entity


class Tag(Entity):
    """
    Implementation of the [Tag](https://projectal.com/docs/latest/#tag/Tag) API.
    """
    _path = 'tag'
    _name = 'tag'
    _links = []
    _links_reverse = []
