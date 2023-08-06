import logging
from functools import wraps

from django.utils.translation import gettext_lazy as _

from apispec.utils import deepupdate

from pfx.pfxcore.exceptions import APIError
from pfx.pfxcore.http import JsonResponse

logger = logging.getLogger(__name__)


def rest_api(
        path, method='get', public=None, priority=0, parameters=None,
        filters=False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            self.request = request
            self.kwargs = kwargs
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("")
                logger.debug("##### REQUEST %s #####", request)
                logger.debug("")
            try:
                self.check_perm(public, func.__name__, *args, **kwargs)
                return func(self, *args, **kwargs)
            except APIError as e:
                return e.response
            except Exception as e:
                logger.exception(e)
                return JsonResponse(dict(message=_(
                    "An internal server error occured.")), status=500)
        wrapper.rest_api_path = path
        wrapper.rest_api_method = method
        wrapper.rest_api_priority = priority
        wrapper.rest_api_params = parameters or []
        wrapper.rest_api_filters = filters
        return wrapper
    return decorator


def rest_property(string=None, type="CharField"):
    def decorator(func):
        func.short_description = string
        func.field_type = type
        return property(func)
    return decorator


def rest_view(path):
    def decorator(cls):
        cls.rest_view_path[cls] = path
        return cls
    return decorator


def rest_doc(path, method, **vals):
    def decorator(cls):
        if cls not in cls.rest_view_path:
            raise Exception(
                "@rest_doc must be used before a @rest_view decorator")
        key = f'{cls.rest_view_path[cls]}{path}', method
        cls.rest_doc[key] = deepupdate(cls.rest_doc.get(key, {}), vals)
        return cls
    return decorator
