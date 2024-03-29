from functools import wraps
from app import logger
from app.tools.log_message_halper import log_msg, log_request_msg
from flask import request, Response


def default_exception_handler(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logger.error(log_msg(
                type_msg=ex.__class__.__name__,
                msg=str(ex),
                source=func.__name__)
            )
            raise ex
    return _wrapper


# декоратор запросов
def decorator_request(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logger.error(
                log_request_msg(
                    type_msg=ex.__class__.__name__,
                    msg=f"Couldn't get json: {str(ex)}",
                    source=request
                )
            )
            return '', 500
    return _wrapper


def system_response(result='{"result": "The request was processed successfully"}', res_status=200,
                    res_mimetype="application/json;  charset=utf-8"):
    return Response(response=result, status=res_status, mimetype=res_mimetype)