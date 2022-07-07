import logging
import traceback
from http import HTTPStatus

from .api import ResponseData

logger = logging.getLogger('default')


def _print_stack_trace():
    try:
        logger.error(traceback.format_exc())
    except Exception:
        logger.exception('Cannot format traceback')


def handle_generic_error(e):
    logger.error(e, exc_info=True)
    res = ResponseData(error=e.name, msg=str(e))
    return res.to_json(), e.status_code


def handle_validation_error(e):
    _print_stack_trace()
    logger.error(e.messages)
    res = ResponseData(error='ValidationError', msg=e.messages)
    return res.to_json(), HTTPStatus.BAD_REQUEST


def handle_unknow_exception(e):
    logger.error(e, exc_info=True)
    res = ResponseData(error="InternalServerError")
    return res.to_json(), HTTPStatus.INTERNAL_SERVER_ERROR


def handle_not_found(e):
    res = ResponseData(error="NotFound")
    return res.to_json(), HTTPStatus.NOT_FOUND


def handle_app_exception(e):
    res = ResponseData(error=e.name, msg=repr(e))
    return res.to_json(), e.status_code


def handle_unauthorized(e):
    res = ResponseData(error='Unauthorized')
    return res.to_json(), HTTPStatus.UNAUTHORIZED
