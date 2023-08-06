import os
import requests
import json

from .exceptions import *


class VAPI:
    def __init__(
        self,
        addr: str = None,
        cacert: str = None,
        token: str = None,
        namespace: str = None,
        token_file: str = None,
    ):
        self.addr = addr or os.environ.get("VAULT_ADDR", None)
        self.cacert = cacert or os.environ.get("VAULT_CACERT", None)
        self.namespace = namespace or os.environ.get("VAULT_NAMESPACE", "")

        if token and token_file:
            raise ValueError("May not set token and token_file.  Please choose one.")
        elif token:
            self.token = token
        elif token_file:
            with open(token_file, "r") as f:
                self.token = f.read().strip()
        elif os.environ.get("VAULT_TOKEN", None):
            self.token = os.environ["VAULT_TOKEN"]
        elif os.environ.get("VAULT_TOKEN_FILE", None):
            with open(os.environ["VAULT_TOKEN_FILE"], "r") as f:
                self.token = f.read().strip()
        else:
            raise ValueError(
                "Vault Token not set.  Please check Env variables or pass directly."
            )

        if self.addr is None:
            raise ValueError("Vault Address not passed or set as environmetn variable")
        if self.token is None:
            raise ValueError("Vault Token not passed or set as environment variable")

        self.api_version = "v1"
        self.current_path = ""

        token_test = self.token_lookup()

    def _set_headers(self):
        return {
            "Content-type": "application/json",
            "X-Vault-Token": self.token,
            "X-Vault-Namespace": self.namespace,
        }

    def _format_url(self, path):
        url = f"{self.api_version}/{path}".replace("//", "/")
        url = f"{self.addr.rstrip('/')}/{url}"
        return url

    def _format_response(self, response, accepted_status_codes):
        if response.status_code in accepted_status_codes:
            try:
                json_response = response.json()
                if "data" in json_response.keys():
                    return json_response["data"]
                else:
                    return json_response
            except ValueError:
                return {}
        else:
            if response.status_code == 403:
                raise VAPIPermissionDeniedError(str(response.json()["errors"]))
            if response.status_code == 503:
                raise VAPISealedError(str(response.json()["errors"]))
            if response.status_code in [200, 204]:
                raise VAPIAcceptedStatusCodeError(
                    f"Vault Response Status Code {response.status_code} not in Accepted Range {', '.join(item) for item in accepted_status_codes}"
                )

            raise VAPIGenericError(response.text)

        try:
            return response.json()
        except ValueError:
            return {}

    def token_lookup(self, raw=False, accepted_status_codes=[204, 200]):
        headers = self._set_headers()
        url = self._format_url("/auth/token/lookup-self")
        response = requests.get(url, headers=headers, verify=self.cacert)

        if raw:
            return response
        else:
            return self._format_response(response, accepted_status_codes)

    def get(self, path, raw=False, accepted_status_codes=[204, 200]):
        headers = self._set_headers()
        url = self._format_url(path)
        response = requests.get(url, headers=headers, verify=self.cacert)

        if raw:
            return response
        else:
            return self._format_response(response, accepted_status_codes)

    def list(self, path, raw=False, accepted_status_codes=[204, 200]):
        headers = self._set_headers()
        url = f"{self._format_url(path)}?list=true"
        response = requests.get(url, headers=headers, verify=self.cacert)

        if raw:
            return response
        else:
            return self._format_response(response, accepted_status_codes)

    def post(self, path, data={}, raw=False, accepted_status_codes=[204, 200]):
        headers = self._set_headers()
        url = self._format_url(path)
        response = requests.post(url, json=data, headers=headers, verify=self.cacert)

        if raw:
            return response
        else:
            return self._format_response(response, accepted_status_codes)

    def delete(self, path, raw=False, accepted_status_codes=[204, 200]):
        headers = self._set_headers()
        url = self._format_url(path)
        response = requests.delete(url, headers=headers, verify=self.cacert)

        if raw:
            return response
        else:
            return self._format_response(response, accepted_status_codes)
