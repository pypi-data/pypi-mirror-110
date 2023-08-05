import json
from typing import Dict, Optional

from django.db.backends import utils

from . import settings
from .errors import IdentityNotSet

USER_IDENTITY: Dict[str, str] = {}
SERVICE_NAME: Optional[str] = None


class Mixin(object):
    def _annotate_query(self, sql: str) -> str:
        if USER_IDENTITY:
            email = USER_IDENTITY["email"]
            group = USER_IDENTITY["group"]
            identity = {
                "user": email,
                "userGroup": group,
            }
            if SERVICE_NAME is not None:
                identity["serviceName"] = SERVICE_NAME
            comment_data = json.dumps(identity)
        else:
            if settings.REQUIRE_IDENTITY:
                # if REQUIRE_IDENTITY is true, block the query and raise this exception
                raise IdentityNotSet()
            else:
                # otherwise, let the query pass
                comment_data = "USER_IDENTITY_NOT_SET"
        return f"/*CyralContext {comment_data}*/ {sql}"

    def execute(self, sql: str, params=None):
        sql = self._annotate_query(sql)
        return super().execute(sql, params)  # type: ignore

    def executemany(self, sql: str, param_list):
        sql = self._annotate_query(sql)
        return super().executemany(sql, param_list)  # type: ignore


class CustomWrapper(Mixin, utils.CursorWrapper):
    pass


class CustomDebugWrapper(Mixin, utils.CursorDebugWrapper):
    pass


def install_wrapper():
    utils.CursorWrapper = CustomWrapper
    utils.CursorDebugWrapper = CustomDebugWrapper


def set_user_identity(email: str, group: str) -> None:
    USER_IDENTITY["email"] = email
    USER_IDENTITY["group"] = group


def set_service_name(name: str) -> None:
    global SERVICE_NAME
    SERVICE_NAME = name


__all__ = ["set_user_identity", "set_service_name"]

default_app_config = "cyral_django_wrapper.apps.CyralDjangoWrapperConfig"
