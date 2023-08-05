from approw.v2.exceptions import ApprowWrongArgumentException


class CheckType(object):

    def __init__(self):
        pass

    def is_list(self, _list, message):
        if not isinstance(_list, list):
            raise ApprowWrongArgumentException(message)

    def target_type(self, target_type):
        if target_type not in ['USER', 'ROLE', 'GROUP', 'ORG']:
            raise ApprowWrongArgumentException('unsupported target_type: %s' % target_type)

    def resource_type(self, resource_type):
        if resource_type not in ['DATA', 'API', 'MENU', 'UI', 'BUTTON']:
            raise ApprowWrongArgumentException('unsupported resource_type: %s' % resource_type)

    def page_options(self, page, limit):
        if page:
            if not isinstance(page, int):
                raise ApprowWrongArgumentException('page must be a int bigger than 0')
            if page < 1:
                raise ApprowWrongArgumentException('page must be a int bigger than 0')

        if limit:
            if not isinstance(limit, int):
                raise ApprowWrongArgumentException('limit must be a int bigger than 0')
            if limit < 1:
                raise ApprowWrongArgumentException('limit must be a int bigger than 0')
