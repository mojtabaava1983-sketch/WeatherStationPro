from weather_api.engine import WeatherApiEngine
from weather_api.models import ApiRequest, NormalizedObservation
class P:
    name="fake"
    def build_request(self,location): return ApiRequest("https://example.test")
    def normalize(self,response): return NormalizedObservation(temperature=response.data["temp"])
class C:
    def request(self,request): return type("R",(),{"status_code":200,"url":request.url,"data":{"temp":22}})(),1
def test_engine():
    r=WeatherApiEngine(P(),C()).fetch({"city":"Baku"})
    assert r.provider=="fake" and r.observation.temperature==22 and r.attempts==1
