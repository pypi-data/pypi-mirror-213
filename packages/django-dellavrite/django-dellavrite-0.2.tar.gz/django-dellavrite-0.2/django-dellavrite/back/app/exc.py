from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied, AuthenticationFailed
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'error': {
            }
        }
    else:
        return response

    if isinstance(exc, Http404):
        response.data['error']['code'] = "404"
        response.data['error']['message'] = "Not Found"
    elif exc.status_code == status.HTTP_403_FORBIDDEN and exc.detail == 'anonymous':
        response.data['error']['code'] = exc.status_code
        response.data['error']['message'] = "Login failed"
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        response.data['error']['code'] = exc.status_code
        response.data['error']['message'] = "Forbidden for you"
    elif exc.status_code == status.HTTP_401_UNAUTHORIZED:
        response.data['error']['code'] = exc.status_code
        response.data['error']['message'] = "Authentication failed"

    if isinstance(exc, ValidationError):
        response.data['error']['message'] = 'validation errors'
        response.data['error']['code'] = 422
        response.data['error']['errors'] = exc.detail

    return response
