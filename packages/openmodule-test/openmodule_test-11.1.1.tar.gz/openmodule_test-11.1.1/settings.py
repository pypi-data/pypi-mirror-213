import time
from enum import Enum
from typing import Dict, Any, Optional, Type

from pydantic import parse_obj_as

from openmodule.models.settings import SettingsGetRequest, SettingsGetResponse, SettingsGetManyRequest, \
    SettingsGetManyResponse
from openmodule.rpc import RPCServer
from openmodule.utils.settings import join_key


def _valid_key(k):
    # just a catch-developer-pitfall utility function
    if k.startswith("common/"):
        return k.count("/") >= 2
    else:
        return "/" in k


class SettingsMocker:
    """
    easy settings mock: replace SettingsProvider with SettingsMocker
    put your settings into mocker as <key>/<scope>: <setting>
    """

    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings
        assert all(_valid_key(k) for k in settings.keys()), (
            "please ensure that all your settings have scopes. A key MUST consist of '<key>/<scope>'\n"
            "for empty string scopes ('') please use '<key>/'"
        )
        self.exception = None

    def get(self, result_type: Type, key: str, scope: str = "") -> Optional[Any]:
        if self.exception:
            raise self.exception
        return parse_obj_as(result_type, self.settings.get(join_key(key, scope)))

    def get_no_exception(self, result_type: Type, key: str, scope: str = "", fallback=None) -> Optional[Any]:
        if self.exception:
            return fallback
        else:
            res = self.settings.get(join_key(key, scope))
            if res is None:
                return fallback
            else:
                try:
                    return parse_obj_as(result_type, res)
                except Exception:
                    return fallback

    def get_many(self, keys_with_types: Dict[str, Type], scope: str = "") -> Dict[str, Any]:
        if self.exception:
            raise self.exception
        else:
            return {key: self.settings.get(join_key(key, scope)) for key in keys_with_types.keys()}

    def get_many_no_exception(self, keys_with_types: Dict[str, Type], scope: str = "",
                              fallbacks: Dict[str, Any] = {}) -> Dict[str, Any]:
        if self.exception:
            return {key: fallbacks.get(key) for key in keys_with_types.keys()}
        else:
            res = {key: self.settings.get(join_key(key, scope)) for key in keys_with_types.keys()}
            for k, v in res.items():
                if v is None:
                    res[k] = fallbacks.get(k)
                else:
                    try:
                        res[k] = parse_obj_as(keys_with_types[k], v)
                    except Exception:
                        res[k] = fallbacks.get(k)
            return res

    def add_setting(self, value: Any, key: str, scope: str = ""):
        self.change_setting(value, key, scope)

    def change_setting(self, value: Any, key: str, scope: str = ""):
        self.settings[join_key(key, scope)] = value

    def remove_setting(self, key: str, scope: str = ""):
        self.settings.pop(join_key(key, scope), None)


class SettingsRPCMocker:
    """
    settings mocker which answers RPCs: Useful when replacing SettingsProvider is not possible
    (e.g. when testing a subclass of SettingsProvider)
    put your settings into mocker as <key>/<scope>: <setting>
    use result_mode to simulate errors
    """

    class ResultMode(str, Enum):
        ok = "ok"  # successful
        error = "error"  # raise error in callback
        timeout = "timeout"  # sleep in callback for 1 second
        fail = "fail"  # return success false
        first_fail = "first_fail"  # return success false for first in get_many

    def __init__(self, rpc_server: RPCServer, settings: Dict[str, Any]):
        rpc_server.register_handler("settings", "get", SettingsGetRequest, SettingsGetResponse, self._get_handler,
                                    register_schema=False)
        rpc_server.register_handler("settings", "get_many", SettingsGetManyRequest, SettingsGetManyResponse,
                                    self._get_many_handler, register_schema=False)
        self.settings = settings
        self.result_mode = SettingsRPCMocker.ResultMode.ok

    def _get_setting(self, key, scope, idx=0) -> SettingsGetResponse:
        setting = self.settings.get(join_key(key, scope))
        if setting is None or self.result_mode == SettingsRPCMocker.ResultMode.fail or \
                (idx == 0 and self.result_mode == SettingsRPCMocker.ResultMode.first_fail):
            return SettingsGetResponse(success=False, error="no such setting")
        else:
            return SettingsGetResponse(value=setting, success=True)

    def _do_errors(self):
        if self.result_mode == SettingsRPCMocker.ResultMode.error:
            raise RuntimeError()
        elif self.result_mode == SettingsRPCMocker.ResultMode.timeout:
            time.sleep(1)
            raise RuntimeError()

    def _get_handler(self, request: SettingsGetRequest, _) -> SettingsGetResponse:
        self._do_errors()
        return self._get_setting(request.key, request.scope)

    def _get_many_handler(self, request: SettingsGetManyRequest, _) -> SettingsGetManyResponse:
        self._do_errors()
        return SettingsGetManyResponse(settings={key: self._get_setting(key, request.scope, i)
                                                 for i, key in enumerate(request.key)})
