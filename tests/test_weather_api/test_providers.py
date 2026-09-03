from weather_api.providers.base import WeatherProvider
from weather_api.models import ApiRequest, NormalizedObservation, ProviderResponse
class P(WeatherProvider):
    name="demo"
    def build_request(self,location): return ApiRequest("https://example.test")
    def normalize(self,response): return NormalizedObservation(temperature=response.data["temperature"])
def test_contract():
    p=P()
    assert p.build_request({}).method=="GET"
    assert p.normalize(ProviderResponse("demo",200,{"temperature":20},"x")).temperature==20
