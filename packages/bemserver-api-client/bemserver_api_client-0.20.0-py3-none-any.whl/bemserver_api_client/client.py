"""BEMServer API client"""
import logging
from packaging.version import Version, InvalidVersion
from requests.auth import HTTPBasicAuth

from .exceptions import BEMServerAPIVersionError
from .request import BEMServerApiClientRequest
from .resources import RESOURCES_MAP


APICLI_LOGGER = logging.getLogger(__name__)

REQUIRED_API_VERSION = {
    "min": Version("0.21.0"),
    "max": Version("0.22.0"),
}


class BEMServerApiClient:
    """API client"""

    def __init__(
        self,
        host,
        use_ssl=True,
        authentication_method=None,
        uri_prefix="http",
        auto_check=False,
        request_manager=None,
    ):
        self.base_uri_prefix = uri_prefix or "http"
        self.host = host
        self.use_ssl = use_ssl

        self._request_manager = request_manager or BEMServerApiClientRequest(
            self.base_uri,
            authentication_method,
            logger=APICLI_LOGGER,
        )

        if auto_check:
            api_version = self.about.getall().data["versions"]["bemserver_api"]
            self.check_api_version(api_version)

    def __getattr__(self, name):
        try:
            # Here name value is expected to be a resource client_entrypoint value.
            return RESOURCES_MAP[name](self._request_manager)
        except KeyError:
            raise AttributeError

    @property
    def uri_prefix(self):
        uri_prefix = self.base_uri_prefix
        if self.use_ssl:
            uri_prefix = self.base_uri_prefix.replace("http", "https")
        return f"{uri_prefix}://"

    @property
    def base_uri(self):
        return f"{self.uri_prefix}{self.host}"

    @staticmethod
    def make_http_basic_auth(email, password):
        return HTTPBasicAuth(
            email.encode(encoding="utf-8"),
            password.encode(encoding="utf-8"),
        )

    @classmethod
    def check_api_version(cls, api_version):
        try:
            version_api = Version(str(api_version))
        except InvalidVersion as exc:
            raise BEMServerAPIVersionError(f"Invalid API version: {str(exc)}")
        version_min = REQUIRED_API_VERSION["min"]
        version_max = REQUIRED_API_VERSION["max"]
        if not (version_min <= version_api < version_max):
            raise BEMServerAPIVersionError(
                f"API version ({str(version_api)}) not supported!"
                f" (expected: >={str(version_min)},<{str(version_max)})"
            )
