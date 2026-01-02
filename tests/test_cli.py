import requests
from click.testing import CliRunner

from weather_cli.main import cli


class DummyResp:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self):
        return self._payload

    @property
    def text(self):
        return str(self._payload)


def test_cli_current_json(monkeypatch):
    def mock_get(url, params=None, timeout=None):
        return DummyResp(200, {"name": "Berlin", "main": {"temp": 12}, "weather": [{"description": "cloudy"}]})

    monkeypatch.setattr(requests, "get", mock_get)
    runner = CliRunner()

    result = runner.invoke(cli, ["--json", "current", "Berlin"], env={"OPENWEATHER_API_KEY": "x"})
    assert result.exit_code == 0
    assert '"name": "Berlin"' in result.output


def test_cli_forecast_text(monkeypatch):
    payload = {
        "city": {"name": "Berlin", "country": "DE"},
        "list": [
            {"dt_txt": "2026-01-02 00:00:00", "main": {"temp": 1}, "wind": {"speed": 2}, "weather": [{"description": "snow"}]},
            {"dt_txt": "2026-01-02 03:00:00", "main": {"temp": 0}, "wind": {"speed": 3}, "weather": [{"description": "snow"}]},
            {"dt_txt": "2026-01-03 00:00:00", "main": {"temp": 4}, "wind": {"speed": 5}, "weather": [{"description": "cloudy"}]},
        ],
    }

    def mock_get(url, params=None, timeout=None):
        return DummyResp(200, payload)

    monkeypatch.setattr(requests, "get", mock_get)

    runner = CliRunner()
    result = runner.invoke(cli, ["forecast", "Berlin", "--days", "2"], env={"OPENWEATHER_API_KEY": "x"})
    assert result.exit_code == 0
    assert "Berlin, DE" in result.output
    assert "2026-01-02" in result.output
