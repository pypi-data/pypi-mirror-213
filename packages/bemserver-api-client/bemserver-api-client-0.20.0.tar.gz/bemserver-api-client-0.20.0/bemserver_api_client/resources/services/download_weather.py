"""BEMServer API client download weather data by sites service resources

/st_download_weather_data_by_sites/ endpoints
/st_download_weather_forecast_data_by_sites/ endpoints
"""
from ..base import BaseResources


class ST_DownloadWeatherDataBySiteResources(BaseResources):
    endpoint_base_uri = "/st_download_weather_data_by_sites/"
    client_entrypoint = "st_download_weather_by_site"

    def get_full(self, *, etag=None, **kwargs):
        endpoint = f"{self.endpoint_base_uri}full"
        return self._req.getall(endpoint, etag=etag, params=kwargs)


class ST_DownloadWeatherForecastDataBySiteResources(BaseResources):
    endpoint_base_uri = "/st_download_weather_forecast_data_by_sites/"
    client_entrypoint = "st_download_weather_forecast_by_site"

    def get_full(self, *, etag=None, **kwargs):
        endpoint = f"{self.endpoint_base_uri}full"
        return self._req.getall(endpoint, etag=etag, params=kwargs)
