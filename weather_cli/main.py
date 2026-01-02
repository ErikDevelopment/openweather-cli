from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import click

from weather_cli.client import WeatherClient
from weather_cli.config import load_settings
from weather_cli.formatters import format_current, format_forecast_summary, summarize_forecast_daily


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--config", "config_path", type=click.Path(path_type=Path), default=None, help="Path to config.yaml")
@click.option("--units", type=click.Choice(["metric", "imperial", "standard"]), default=None, help="Override units")
@click.option("--lang", default=None, help="Override language (e.g. en, de)")
@click.option("--timeout", type=float, default=None, help="Override request timeout in seconds")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
@click.pass_context
def cli(ctx: click.Context, config_path: Optional[Path], units: Optional[str], lang: Optional[str], timeout: Optional[float], as_json: bool) -> None:
    """weather: OpenWeather CLI (current weather + forecast)."""
    try:
        settings = load_settings(config_path)
    except Exception as e:
        raise click.ClickException(str(e))

    # overrides
    if units:
        settings = settings.__class__(api_key=settings.api_key, units=units, lang=settings.lang, timeout=settings.timeout)
    if lang:
        settings = settings.__class__(api_key=settings.api_key, units=settings.units, lang=lang, timeout=settings.timeout)
    if timeout is not None:
        settings = settings.__class__(api_key=settings.api_key, units=settings.units, lang=settings.lang, timeout=timeout)

    ctx.obj = {
        "client": WeatherClient(
            api_key=settings.api_key,
            units=settings.units,
            lang=settings.lang,
            timeout=settings.timeout,
        ),
        "settings": settings,
        "as_json": as_json,
    }


@cli.command()
@click.argument("city", required=True)
@click.option("--country", default=None, help="Optional country code (e.g. DE, US)")
@click.pass_context
def current(ctx: click.Context, city: str, country: Optional[str]) -> None:
    """Get current weather for CITY."""
    client: WeatherClient = ctx.obj["client"]
    settings = ctx.obj["settings"]
    as_json: bool = ctx.obj["as_json"]

    data = client.current_by_city(city, country=country)

    if as_json:
        click.echo(json.dumps(data, indent=2, ensure_ascii=False))
        return

    click.echo(format_current(data, units=settings.units))


@cli.command()
@click.argument("city", required=True)
@click.option("--country", default=None, help="Optional country code (e.g. DE, US)")
@click.option("--days", type=int, default=3, show_default=True, help="Number of days to summarize (1..5)")
@click.pass_context
def forecast(ctx: click.Context, city: str, country: Optional[str], days: int) -> None:
    """Get forecast summary for CITY (daily min/max)."""
    client: WeatherClient = ctx.obj["client"]
    settings = ctx.obj["settings"]
    as_json: bool = ctx.obj["as_json"]

    days = max(1, min(days, 5))
    data = client.forecast_3h_by_city(city, country=country)

    if as_json:
        click.echo(json.dumps(data, indent=2, ensure_ascii=False))
        return

    city_label = data.get("city", {}) or {}
    name = city_label.get("name", city)
    ctry = city_label.get("country", "")
    label = f"{name}{', ' + ctry if ctry else ''}"

    daily = summarize_forecast_daily(data, units=settings.units, days=days)
    if not daily:
        raise click.ClickException("No forecast data available.")

    click.echo(format_forecast_summary(daily, city_label=label))


if __name__ == "__main__":
    cli()
