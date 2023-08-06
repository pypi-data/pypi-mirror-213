"""BEMServer API client cleanup service resources

/st_cleanups_by_campaigns/ endpoints
/st_cleanups_by_timeseries/ endpoints
"""
from ..base import BaseResources


class ST_CleanupByCampaignResources(BaseResources):
    endpoint_base_uri = "/st_cleanups_by_campaigns/"
    client_entrypoint = "st_cleanup_by_campaign"

    def get_full(self, *, etag=None, **kwargs):
        endpoint = f"{self.endpoint_base_uri}full"
        return self._req.getall(endpoint, etag=etag, params=kwargs)


class ST_CleanupByTimeseriesResources(BaseResources):
    endpoint_base_uri = "/st_cleanups_by_timeseries/"
    disabled_endpoints = ["create", "update", "delete"]
    client_entrypoint = "st_cleanup_by_timeseries"

    def get_full(self, *, etag=None, **kwargs):
        endpoint = f"{self.endpoint_base_uri}full"
        return self._req.getall(endpoint, etag=etag, params=kwargs)
