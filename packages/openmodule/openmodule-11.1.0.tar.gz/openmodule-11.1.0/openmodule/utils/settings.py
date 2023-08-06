import logging
import threading
import time
from typing import Dict, Type, Any, Optional

from pydantic import parse_obj_as

from openmodule.core import core
from openmodule.models.settings import SettingsChangedMessage, SettingsGetRequest, SettingsGetResponse, \
    SettingsGetManyRequest, SettingsGetManyResponse


def split_key(db_key):
    split = db_key.split("/")
    k = "/".join(split[0:-1])
    s = db_key[db_key.rfind("/")+1:]
    return k, s


def join_key(key, scope):
    return f"{key}/{scope}"


class CachedSetting:
    def __init__(self, value: Any, expires_at: float):
        self.expires_at = expires_at
        self.value = value

    def is_expired(self):
        return time.time() > self.expires_at


class SettingsProvider:
    _cached_values: Dict[str, CachedSetting]

    def __init__(self, expire_time=300.0, rpc_timeout=3.0):
        self.log = logging.getLogger(__name__)
        self.expire_time = expire_time
        self.rpc_timeout = rpc_timeout
        self._cached_values = {}
        self._cache_lock = threading.Lock()
        core().messages.register_handler("settings", SettingsChangedMessage, self.settings_changed)

    def settings_changed(self, message: SettingsChangedMessage):
        """
        invalidate cached settings when changed
        """
        with self._cache_lock:
            for key in message.changed_keys:
                self._cached_values.pop(key, None)

    def _get_rpc(self, result_type: Type, key: str, scope: str = "") -> Optional[Any]:
        key_scope = join_key(key, scope)
        with self._cache_lock:
            self._cached_values.pop(key_scope, None)
        response = core().rpc_client.rpc("settings", "get", SettingsGetRequest(key=key, scope=scope),
                                         SettingsGetResponse, self.rpc_timeout)
        if not response.success:
            if response.error != "no such setting":
                self.log.error(f"Settings RPC for key {key_scope} failed because of error {response.error}")
            return None
        result = parse_obj_as(result_type, response.value)
        with self._cache_lock:
            self._cached_values[key_scope] = CachedSetting(response.value, time.time() + self.expire_time)
        return result

    def _get_many_rpc(self, keys_with_types: Dict[str, Type], scope: str = "") -> Dict[str, Any]:
        with self._cache_lock:
            for key in keys_with_types.keys():
                self._cached_values.pop(join_key(key, scope), None)
        response = core().rpc_client.rpc("settings", "get_many",
                                         SettingsGetManyRequest(key=list(keys_with_types.keys()), scope=scope),
                                         SettingsGetManyResponse, self.rpc_timeout)
        results = {}
        for key, setting in response.settings.items():
            key_scope = join_key(key, scope)
            if not setting.success:
                if setting.error != "no such setting":
                    self.log.error(f"Failed to get setting {key_scope} because of error {setting.error}")
                results[key] = None
                continue
            try:
                result = parse_obj_as(keys_with_types[key], setting.value)
            except Exception:
                self.log.error(f"Failed to parse setting {key_scope}")
                results[key] = None
                continue
            results[key] = result
            with self._cache_lock:
                self._cached_values[key_scope] = CachedSetting(setting.value, time.time() + self.expire_time)
        return results

    def get(self, result_type: Type, key: str, scope: str = "") -> Optional[Any]:
        key_scope = join_key(key, scope)
        with self._cache_lock:
            if key_scope in self._cached_values:
                if self._cached_values[key_scope].is_expired():
                    self._cached_values.pop(key_scope, None)
                else:
                    try:
                        return parse_obj_as(result_type, self._cached_values[key_scope].value)
                    except Exception:
                        self.log.error("Tried to get same settings with different incompatible types")
                        self._cached_values.pop(key_scope, None)
        return self._get_rpc(result_type, key, scope)

    def get_no_exception(self, result_type: Type, key: str, scope: str = "", fallback=None) -> Optional[Any]:
        try:
            res = self.get(result_type, key, scope)
            return fallback if res is None else res
        except Exception:
            self.log.exception("Exception in get setting")
            return fallback

    def get_many(self, keys_with_types: Dict[str, Type], scope: str = "") -> Dict[str, Any]:
        all_found_in_cache = True
        results = {}
        with self._cache_lock:
            for key, result_type in keys_with_types.items():
                key_scope = join_key(key, scope)
                if key_scope in self._cached_values:
                    if self._cached_values[key_scope].is_expired():
                        self._cached_values.pop(key_scope, None)
                        all_found_in_cache = False
                    else:
                        try:
                            results[key] = parse_obj_as(result_type, self._cached_values[key_scope].value)
                        except Exception:
                            self.log.error("Tried to get same settings with different incompatible types")
                            self._cached_values.pop(key_scope, None)
                            all_found_in_cache = False
                else:
                    all_found_in_cache = False
        if all_found_in_cache:
            return results
        else:
            return self._get_many_rpc(keys_with_types, scope)

    def get_many_no_exception(self, keys_with_types: Dict[str, Type], scope: str = "",
                                       fallbacks: Dict[str, Any] = {}) -> Dict[str, Any]:
        try:
            res = self.get_many(keys_with_types, scope) or {key: fallbacks.get(key) for key in keys_with_types.keys()}
            for k, v in res.items():
                if v is None:
                    res[k] = fallbacks.get(k)
            return res
        except Exception:
            self.log.exception("Exception in get many settings")
            return {key: fallbacks.get(key) for key in keys_with_types.keys()}
