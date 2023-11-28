from http import HTTPStatus

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import exception_handler

from gabgabgurus.common.utils.exceptions import extract_exception_details
from gabgabgurus.config import exceptions

exception_and_status_code_mapping = {
    exceptions.HTTPException: None,
    exceptions.EntityAlreadyExists: HTTPStatus.CONFLICT,
    exceptions.EntityDoesntExist: HTTPStatus.NOT_FOUND,
    exceptions.Forbidden: HTTPStatus.FORBIDDEN,
    exceptions.OldPasswordIsIncorrect: HTTPStatus.UNAUTHORIZED,
    exceptions.DBError: HTTPStatus.CONFLICT,
}


def make_error_response(exception, status_code: int | None = None):
    code = status_code
    if not code and hasattr(exception, "code"):
        code = exception.code
    if not code:
        code = exception_and_status_code_mapping.get(type(exception), HTTPStatus.INTERNAL_SERVER_ERROR)

    details = extract_exception_details(exception)

    return Response(details, status=code)


def http_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        if type(exc) in exception_and_status_code_mapping or not settings.DEBUG:
            return make_error_response(exc)

    return response
