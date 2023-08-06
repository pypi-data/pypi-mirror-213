import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

import jwt
from jwt import DecodeError

from pfx.pfxcore.models import CacheableMixin
from pfx.pfxcore.shortcuts import delete_token_cookie

logger = logging.getLogger(__name__)


class JWTTokenDecodeMixin:

    @classmethod
    def get_cached_user(cls, pk):
        UserModel = get_user_model()
        has_cache = issubclass(UserModel, CacheableMixin)
        if (has_cache):
            user = UserModel.cache_get(pk)
            if user:
                return user
        user = UserModel._default_manager.get(pk=pk)
        if (has_cache):
            user.cache()
        return user

    @classmethod
    def decode_jwt(cls, token):
        try:
            decoded = jwt.decode(
                token, settings.PFX_SECRET_KEY,
                options=dict(require=["exp"]),
                algorithms="HS256")
            return cls.get_cached_user(decoded['pfx_user_pk'])
        except get_user_model().DoesNotExist:
            raise
        except DecodeError as e:
            logger.exception(e)
            raise
        except jwt.ExpiredSignatureError:
            raise
        except Exception as e:  # pragma: no cover
            logger.exception(e)
            raise


class AuthenticationMiddleware(JWTTokenDecodeMixin, MiddlewareMixin):

    def process_request(self, request):
        authorization = request.headers.get('Authorization')
        if authorization:
            try:
                _, key = authorization.split("Bearer ")
            except ValueError:
                key = None
            try:
                request.user = self.decode_jwt(key)
            except Exception:
                request.user = AnonymousUser()
        else:
            if not hasattr(request, 'user'):
                request.user = AnonymousUser()

    def process_response(self, request, response):
        return response


class CookieAuthenticationMiddleware(JWTTokenDecodeMixin, MiddlewareMixin):

    def process_request(self, request):
        key = request.COOKIES.get('token')
        if key:
            try:
                request.user = self.decode_jwt(key)
            except Exception:
                request.user = AnonymousUser()
                request.delete_cookie = True
        else:
            if not hasattr(request, 'user'):
                request.user = AnonymousUser()

    def process_response(self, request, response):
        if getattr(request, 'delete_cookie', False):
            return delete_token_cookie(response)
        return response
