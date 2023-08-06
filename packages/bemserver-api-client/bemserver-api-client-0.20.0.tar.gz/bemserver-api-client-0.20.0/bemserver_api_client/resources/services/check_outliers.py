"""BEMServer API client outliers data service resources

/st_check_outliers_by_campaigns/ endpoints
"""
from ..base import BaseResources


class ST_CheckOutlierByCampaignResources(BaseResources):
    endpoint_base_uri = "/st_check_outliers_by_campaigns/"
    client_entrypoint = "st_check_outlier_by_campaign"

    def get_full(self, *, etag=None, **kwargs):
        endpoint = f"{self.endpoint_base_uri}full"
        return self._req.getall(endpoint, etag=etag, params=kwargs)
