from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Tuple


def unit_symbols(units: str) -> tuple[str, str]:
    # temperature, wind speed
    if units == "imperial":
        return "°F", "mph"
    if units == "standard":
        return "K", "m/s"
    return "°C", "m/s"


def format_current(data: Dict[str, Any], units: str) -> str:
    t_sym, w_sym = unit_symbols(units)
    name = data.get("name", "Unknown")
    sys = data.get("sys", {}) or {}
    country = sys.get("country", "")
    weather = (data.get("weather") or [{}])[0] or {}
    main = data.get("main", {}) or {}
    wind = data.get("wind", {}) or {}

    desc = weather.get("description", "n/a")
    temp = main.get("temp", "n/a")
    feels = main.get("feels_like", "n/a")
    hum = main.get("humidity", "n/a")
    spd = wind.get("speed", "n/a")

    loc = f"{name}{', ' + country if country else ''}"
    return (
        f"{loc}\n"
        f"- Condition: {desc}\n"
        f"- Temperature: {temp}{t_sym} (feels like {feels}{t_sym})\n"
        f"- Humidity: {hum}%\n"
        f"- Wind: {spd} {w_sym}"
    )


def summarize_forecast_daily(data: Dict[str, Any], units: str, days: int = 3) -> List[Dict[str, Any]]:
    """
    Take 3-hour forecast list and summarize into daily min/max + most common description.
    """
    t_sym, w_sym = unit_symbols(units)
    items = data.get("list") or []
    if not isinstance(items, list):
        return []

    by_day: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for it in items:
        dt_txt = it.get("dt_txt")
        if not dt_txt:
            continue
        day = dt_txt.split(" ")[0]
        by_day[day].append(it)

    days_sorted = sorted(by_day.keys())[: max(1, days)]
    out: List[Dict[str, Any]] = []

    for day in days_sorted:
        entries = by_day[day]
        temps = []
        descs = []
        winds = []
        for e in entries:
            main = e.get("main", {}) or {}
            wind = e.get("wind", {}) or {}
            w = (e.get("weather") or [{}])[0] or {}
            if "temp" in main:
                temps.append(main["temp"])
            if "speed" in wind:
                winds.append(wind["speed"])
            if "description" in w:
                descs.append(w["description"])

        if not temps:
            continue

        # most common description
        desc = max(set(descs), key=descs.count) if descs else "n/a"
        avg_wind = round(sum(winds) / len(winds), 2) if winds else "n/a"

        out.append(
            {
                "date": day,
                "temp_min": min(temps),
                "temp_max": max(temps),
                "condition": desc,
                "wind_avg": avg_wind,
                "temp_unit": t_sym,
                "wind_unit": w_sym,
            }
        )

    return out


def format_forecast_summary(daily: List[Dict[str, Any]], city_label: str) -> str:
    lines = [city_label]
    for d in daily:
        lines.append(
            f"- {d['date']}: {d['condition']}, "
            f"{d['temp_min']}{d['temp_unit']}..{d['temp_max']}{d['temp_unit']}, "
            f"wind avg {d['wind_avg']} {d['wind_unit']}"
        )
    return "\n".join(lines)
