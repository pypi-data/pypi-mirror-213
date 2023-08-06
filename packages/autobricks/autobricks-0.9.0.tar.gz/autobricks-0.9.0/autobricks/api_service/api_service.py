from ._auth_factory import auth_factory, AuthenticationType
from ._auth import Auth
from ._base_api import (
    base_api_get as _base_api_get,
    base_api_post as _base_api_post,
    base_api_delete as _base_api_delete,
    base_api_put as _base_api_put,
)
from . import autobricks_logging
from ._exceptions import AutobricksConfigurationInvalid, AutobricksResponseJsonError
from ._configuration import configuration
import json

_logger = autobricks_logging.get_logger(__name__)


_API_VERSION = "2.0"
_PREVIEW = "preview"


class ApiService:
    def __init__(self, config: dict = None):
        _logger.info("Initialising ApiService")

        if config:
            _logger.debug("Configuring ApiService from constructor")
            _config = config
        else:
            _logger.debug("Configuring ApiService from default configuration")
            _config = configuration

        config_json = json.dumps(_config, indent=4)
        _logger.debug(config_json)

        try:
            auth_type_str = _config["auth_type"]
        except KeyError:
            e = AutobricksConfigurationInvalid(
                "auth_type", valid_values=AuthenticationType
            )
            _logger.error(e.message)
            raise e

        try:
            self.host: str = _config["databricks_api_host"]
            if self.host.endswith("/"):
                self.host = self.host[:-1]

            _logger.debug(f"Databricks REST endpoint set as {self.host}")
        except KeyError:
            e = AutobricksConfigurationInvalid("databricks_api_host")
            _logger.error(e.message)
            raise e

        try:
            _logger.debug(f"Setting AuthorisationType as {auth_type_str}")
            self.auth_type: AuthenticationType = AuthenticationType[auth_type_str]
        except Exception:
            e = AutobricksConfigurationInvalid(
                "auth_type", value=auth_type_str, valid_values=AuthenticationType
            )
            _logger.error(e.message)
            raise e

        auth: Auth = auth_factory.get_auth(self.auth_type, _config)

        _logger.debug("Setting Authorisation Headers")
        self._headers = auth.get_headers()
        _header_json = json.dumps(self._headers, indent=4)
        _logger.debug(_header_json)

    def api_put(
        self,
        api: str,
        function: str,
        data: dict = None,
        params=None,
        preview: bool = False,
        api_version=_API_VERSION,
    ):
        if preview:
            url = f"{self.host}/api/{api_version}/{_PREVIEW}/{api}/{function}"
        else:
            url = f"{self.host}/api/{api_version}/{api}/{function}"

        response = _base_api_put(
            url=url, headers=self._headers, json=data, params=params
        )

        try:
            json = response.json()
        except Exception:
            ex = AutobricksResponseJsonError(url, "PUT", data, response.text)
            _logger.error(ex.message)
            raise ex

        return json

    def api_get(
        self,
        api: str,
        function: str,
        data: dict = None,
        params=None,
        preview: bool = False,
        api_version=_API_VERSION,
    ):
        if preview:
            url = f"{self.host}/api/{api_version}/{_PREVIEW}/{api}"
        else:
            url = f"{self.host}/api/{api_version}/{api}"

        if function:
            url = f"{url}/{function}"

        response = _base_api_get(
            url=url, headers=self._headers, json=data, params=params
        )

        try:
            json = response.json()
        except Exception:
            ex = AutobricksResponseJsonError(url, "GET", data, response.text)
            _logger.error(ex.message)
            raise ex

        return json

    def api_delete(
        self,
        api: str,
        function: str,
        data: dict = None,
        params=None,
        preview: bool = False,
        api_version=_API_VERSION,
    ):
        if preview:
            url = f"{self.host}/api/{api_version}/{_PREVIEW}/{api}/{function}"
        else:
            url = f"{self.host}/api/{api_version}/{api}/{function}"

        response = _base_api_delete(
            url=url, headers=self._headers, json=data, params=params
        )

        try:
            json = response.json()
        except Exception:
            ex = AutobricksResponseJsonError(url, "DELETE", data, response.text)
            _logger.error(ex.message)
            raise ex

        return json

    def api_post(
        self,
        api: str,
        function: str,
        data: dict,
        preview: bool = False,
        api_version=_API_VERSION,
    ):
        if preview:
            url = f"{self.host}/api/{api_version}/{_PREVIEW}/{api}"
        else:
            url = f"{self.host}/api/{api_version}/{api}"

        if function:
            url = f"{url}/{function}"

        response = _base_api_post(url=url, headers=self._headers, json=data)

        try:
            json = response.json()
        except Exception:
            ex = AutobricksResponseJsonError(url, "POST", data, response.text)
            _logger.error(ex.message)
            raise ex

        return json
