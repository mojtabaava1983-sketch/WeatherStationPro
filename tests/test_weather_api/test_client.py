import json
from unittest.mock import patch
from weather_api.client import HttpClient
from weather_api.models import ApiRequest
from weather_api.retry import RetryPolicy
def test_client_json():
    class R:
        status=200
        def geturl(self): return "https://example.test"
        def read(self): return json.dumps({"temp":21}).encode()
        def __enter__(self): return self
        def __exit__(self,*a): pass
    with patch("weather_api.client.urlopen", return_value=R()):
        r,n=HttpClient(RetryPolicy(1,0)).request(ApiRequest("https://example.test"))
    assert r.data=={"temp":21} and n==1
