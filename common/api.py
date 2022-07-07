import logging
import flask
import uuid

logger = logging.getLogger('default')


class ResponseData():
    def __init__(self, data={}, total=None, error=None, msg=None):
        self.data = data
        self.error = error
        self.msg = msg
        self.total = total

    def to_json(self):
        messages = None
        if self.error and self.msg:
            messages = []
            if type(self.msg) is list:
                messages += self.msg
            else:
                messages.append(self.msg)
        return {
            'data': self.data,
            'total': self.total,
            'error_code': self.error,
            'error_message': messages
        }


def add_request_id():
    if flask.request.headers.get('X-Request-Id'):
        flask.g.request_id = flask.request.headers.get('X-Request-Id')
    elif not getattr(flask.g, 'request_id', None):
        new_uuid = _generate_request_id()
        flask.g.request_id = new_uuid
    else:
        return None


def _generate_request_id():
    return uuid.uuid4()
