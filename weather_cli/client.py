from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class WeatherClient:
    api_key: str
    units: str = "metric"
    lang: str = "en"
    timeout: float = 8.0
    base_url: str = "https://api.openweathermap.org/data/2.5"

    def _get(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        merged = {
            **params,
            "appid": self.api_key,
            "units": self.units,
            "lang": self.lang,
        }
        r = requests.get(url, params=merged, timeout=self.timeout)
        # OpenWeather returns JSON errors; still raise on HTTP error:
        try:
            data = r.json()
        except Exception:
            data = {"message": r.text}

        if r.status_code >= 400:
            msg = data.get("message", f"HTTP {r.status_code}")
            raise RuntimeError(f"OpenWeather error: {msg} (HTTP {r.status_code})")
        return data

    def current_by_city(self, city: str, country: Optional[str] = None) -> Dict[str, Any]:
        q = city if not country else f"{city},{country}"
        return self._get("/weather", {"q": q})

    def forecast_3h_by_city(self, city: str, country: Optional[str] = None) -> Dict[str, Any]:
        """
        5 day / 3 hour forecast endpoint.
        We'll summarize it in the CLI.
        """
        q = city if not country else f"{city},{country}"
        return self._get("/forecast", {"q": q})
