# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0301
# flake8: noqa

import hashlib
import json
import time
import base64
import urllib
import requests
from threading import Timer

TOKEN_REFRESH_INTERVAL_SCALE = 0.9
UNMISTAKABLE_CHARS = "23456789ABCDEFGHJKLMNPQRSTWXYZabcdefghijkmnopqrstuvwxyz"
PRODUCTION_API_HOST = "https://novum-batteries.com"


class novum_api_error(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(f"novum_api_error: {message} (status: {status_code})")


def getSHA256(to_hash: str) -> str:
    return hashlib.sha256(to_hash).hexdigest()


def user_name(user: dict) -> str:
    return user["profile"]["name"]


def full_name(user: dict) -> str:
    if len(user.keys()) > 0:
        return str(user["profile"]["first_name"]) + str(user["profile"]["family_name"])
    else:
        raise novum_api_error("User not found!", 400)


def parse_jwt(token: str) -> dict:
    base64_input = token.split(".")[1]
    base64_bytes = base64_input.encode("utf-8")
    # replace '-' with '+' and '_' with '/' as base64url is different than base64
    base64_bytes += b"=" * (4 - len(base64_bytes) % 4)
    base64_string = base64_bytes.decode("utf-8").replace("-", "+").replace("_", "/")
    if "window" in base64_string:
        json_payload = urllib.parse.unquote(base64.b64decode(base64_string).decode("utf-8"))
    else:
        json_payload = urllib.parse.unquote(base64.b64decode(base64_string.encode("utf-8")).decode("utf-8"))
    return json.loads(json_payload)


class base_api_client:
    def __init__(
        self,
        user=None,
        host=PRODUCTION_API_HOST,
        refresh_token_warning=True,
        refresh_interval_scale=TOKEN_REFRESH_INTERVAL_SCALE,
        _relogin_timer_handle=None,
        _authenticated=False,
    ):
        self.user = user
        self.headers = (
            None
            if user is None
            else dict({"Content-Type": "application/json", "Authorization": "Bearer " + str(self.user.get("jwt"))})
        )
        self.host = host
        self._refresh_token_warning = refresh_token_warning
        self._refresh_interval_scale = refresh_interval_scale
        self._relogin_timer_handle = _relogin_timer_handle
        self._authenticated = _authenticated

    def _set_user(self, user):
        if len(user.keys()) > 0 and user.get("jwt") is not None:
            user["expires_at"] = self._get_expire_time_from_token_in_unix_time_millis(user["jwt"]).isoformat()
            self.user = user
            self._install_token_refresh_procedure(user)

    def _clear_user(self):
        self.user = None
        self._remove_relogin_timer_handle()

    def _remove_relogin_timer_handle(self):
        if self._relogin_timer_handle is not None:
            # clearTimeout(self._reloginTimerHandle)
            self._relogin_timer_handle = None

    def _get_expire_time_from_token_in_unix_time_millis(self, token: str) -> float:
        if token is not None:
            inner_token = parse_jwt(token)
            if inner_token is not None:
                return 1000 * inner_token["exp"]
        return 3600 * 1000

    def _install_token_refresh_procedure(self, user):
        self._remove_relogin_timer_handle()
        expire_time_in_millis = self._get_expire_time_from_token_in_unix_time_millis(self.user["jwt"])
        now = time.time() * 1000

        if expire_time_in_millis is not None and expire_time_in_millis > 1000 + now:
            if user.get("refresh_token") is not None:
                refresh_interval_in_millis = round(self._refresh_interval_scale * (expire_time_in_millis - now), 10)
                self._relogin_timer_handle = Timer(self._refresh_access_token, refresh_interval_in_millis)
            else:
                if self._refresh_token_warning:
                    raise ValueError(
                        "APIClient: There is no refreshToken! Autorefresh of access tokens is not possible."
                    )
                else:
                    raise ValueError("APIClient: Could not get expire_time_In_millis or token has already expired.")

    def _refresh_access_token(self):
        if self.user is not None and self.user.get("refresh_token") is not None:
            print("APIClient._refreshAccessToken - Refreshing the accessToken for userId" + self.user.get("id"))
            new_access_object = self._post_json("/api/batman/v1/refresh", self.user)
            if new_access_object.get("jwt") is not None:
                self._set_user(self.user)
            else:
                print("APIClient._refreshAccessToken - Error no user or refesh token found!")

    def _fetch_by_URL(self, url: str, options: dict):
        response = self._get_json(url, option=options)
        if response.get("ok") is False:
            raise ValueError(f"Failed to load resource {url} -> Status:" + response.get("status"))
        return response

    def _post_by_URL(self, url: str, options: dict):
        response = self._post_json(url, option=options)
        if response.get("ok") is False:
            raise ValueError(f"Failed to load resource {url} -> Status:" + response.get("status"), response)
        return response

    def _fetch_by_path(self, path: str, options: dict):
        return self._fetch_by_URL(self.host + path, options)

    def _post_by_path(self, path: str, options: dict) -> dict:
        return self._post_by_URL(self.host + path, options)

    def _encode_auth_header(self, username: str, password: str):
        return {"Authorization": "Basic " + str(base64.b64encode(username, password).decode("utf-8"))}

    def _headers(self, headers):
        if self.user is not None and self.user.get("jwt") is not None:
            headers["Authorization"] = f"Bearer {self.user['jwt']}"
        return headers

    def _get_json(self, url: str, filter_json=None, option=None, timeout: float = 4.0):
        full_url = str(self.host) + url
        headers = self.headers
        params_json = {"filter": json.dumps(filter_json), "option": json.dumps(option)}
        response = requests.get(
            url=full_url,
            headers=headers,
            params=params_json,
            timeout=timeout,
        )
        if response.status_code == requests.codes.get("ok"):
            return response.json()
        else:
            raise novum_api_error("Unable to get data.", response.status_code)

    def _post_file(self, path: str, file):
        options = {"upload_file": open(file)}
        return self._post_by_path(path, options=options)

    def _post_json(self, url: str, data=None, filter_json=None, option=None, timeout: float = 4):
        full_url = self.host + url
        headers = self.headers
        params_json = {"filter": json.dumps(filter_json), "option": json.dumps(option)}
        data = json.dumps(data)

        response = requests.post(
            url=full_url,
            headers=headers,
            params=params_json,
            data=data,
            timeout=timeout,
        )

        if response.status_code == requests.codes.get("ok"):
            return response.json()

        else:
            raise novum_api_error("The data could not be posted", response.status_code)

    def _put_json(self, url: str, data=None, filter_json=None, option=None, timeout: float = 4):
        full_url = self.host + url
        headers = self.headers
        params_json = {"filter": json.dumps(filter_json), "option": json.dumps(option)}
        data_json = json.dumps(data)

        response = requests.put(
            url=full_url,
            headers=headers,
            params=params_json,
            data=data_json,
            timeout=timeout,
        )

        if response.status_code == requests.codes.get("ok"):
            return response.json()
        else:
            raise novum_api_error("The data was not updated", response.status_code)

    def _delete_json(self, url: str, filter_json=None, option=None, timeout: float = 4.0):
        full_url = self.host + url
        headers = self.headers
        params_json = {"filter": json.dumps(filter_json), "option": json.dumps(option)}

        response = requests.delete(
            url=full_url,
            headers=headers,
            params=params_json,
            timeout=timeout,
        )
        if response.status_code <= 204:
            return response
        else:
            raise novum_api_error("The data was not removed", response.status_code)

    def _get_text(self, path: str, headers=None):
        headers.update({"Content-Type": "application/text"})
        response = self._fetch_by_path(path, options=headers)
        return response.text()

    def _get_array_buffer(self, path: str, headers=None):
        headers.update({"Content-Type": "application/text"})
        response = self._fetch_by_path(path, options=headers)
        return [int(i) for i in response.get("content")]

    def _host(self) -> str:
        return self.host

    def authenticated(self) -> bool:
        return self._authenticated

    def set_new_endpoint(self, new_end_point: str):
        self.host = new_end_point
