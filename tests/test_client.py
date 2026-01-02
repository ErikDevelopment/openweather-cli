import requests
from weather_cli.client import WeatherClient


class DummyResp:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self):
        return self._payload

    @property
    def text(self):
        return str(self._payload)


def test_current_by_city_success(monkeypatch):
    def mock_get(url, params=None, timeout=None):
        assert "/weather" in url
        assert params["q"] == "Berlin"
        assert "appid" in params
        return DummyResp(200, {"name": "Berlin", "main": {"temp": 10}, "weather": [{"description": "clear sky"}]})

    monkeypatch.setattr(requests, "get", mock_get)

    c = WeatherClient(api_key="x", units="metric", lang="en")
    data = c.current_by_city("Berlin")
    assert data["name"] == "Berlin"


def test_error_raises(monkeypatch):
    def mock_get(url, params=None, timeout=None):
        return DummyResp(401, {"message": "Invalid API key"})

    monkeypatch.setattr(requests, "get", mock_get)

    c = WeatherClient(api_key="bad")
    try:
        c.current_by_city("Berlin")
        assert False, "Expected RuntimeError"
    except RuntimeError as e:
        assert "Invalid API key" in str(e)
