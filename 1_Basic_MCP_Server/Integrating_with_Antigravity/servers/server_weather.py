### Documentation for https://www.weatherapi.com/docs/

from __future__ import annotations
import os
from typing import Any, Optional, Dict, List
from dataclasses import dataclass
from dotenv import load_dotenv
from fastmcp import FastMCP
import httpx
import requests

load_dotenv()

### ---- Weather Current ----###
class WeatherAPIError(RuntimeError):
    """Raised when WeatherAPI returns an error or an unexpected response."""

mcp = FastMCP(name="weather", instructions="This server can provide real-time weather and weather forecast.")

@mcp.tool(name="get_realtime_weather", description="Get real-time weather")
async def get_realtime_weather(
    location: str,
    *,
    api_key: Optional[str] = None,
    aqi: bool = False,
    lang: Optional[str] = None,
    timeout_s: float = 10.0,
) -> Dict[str, Any]:
    """
    Fetch real-time (current) weather for a location using WeatherAPI.com.

    Args:
        location:
            The 'q' parameter. Examples include:
            - "Paris"
            - "48.8567,2.3508"
            - "10001" (US ZIP)
            - "auto:ip"
            - "iata:DXB"
            - "metar:EGLL"
        api_key:
            WeatherAPI key. If not provided, reads WEATHERAPI_KEY from env.
        aqi:
            Include air-quality data where supported by your plan/output settings.
        lang:
            Optional language code for condition text (if supported).
        timeout_s:
            Requests timeout in seconds.

    Returns:
        Parsed JSON response as a dict.

    Raises:
        WeatherAPIError on API-level errors or unexpected responses.
        requests.RequestException on network/transport errors.
    """
    api_key = api_key or os.getenv("WEATHERAPI_KEY")
    if not api_key:
        raise WeatherAPIError("Missing API key. Provide api_key or set WEATHERAPI_KEY env var.")

    base_url = "https://api.weatherapi.com/v1"
    url = f"{base_url}/current.json"  # Current weather endpoint :contentReference[oaicite:1]{index=1}

    params = {
        "key": api_key,               # key=<YOUR API KEY> :contentReference[oaicite:2]{index=2}
        "q": location,                # q=<location query> :contentReference[oaicite:3]{index=3}
        "aqi": "yes" if aqi else "no"  # aqi=yes|no :contentReference[oaicite:4]{index=4}
    }
    if lang:
        params["lang"] = lang

    resp = requests.get(url, params=params, timeout=timeout_s)
    resp.raise_for_status()

    data = resp.json()

    # WeatherAPI returns an "error" object in JSON for API-level errors.
    if isinstance(data, dict) and "error" in data:
        err = data["error"] or {}
        code = err.get("code")
        msg = err.get("message", "Unknown WeatherAPI error")
        raise WeatherAPIError(f"WeatherAPI error (code={code}): {msg}")

    if not isinstance(data, dict) or "current" not in data:
        raise WeatherAPIError("Unexpected response shape from WeatherAPI.")

    return data


### ---- Weather Forecast ----###

class WeatherAPIError(RuntimeError):
    pass


@dataclass(frozen=True)
class ForecastDay:
    date: str
    max_temp_c: float
    min_temp_c: float
    avg_temp_c: float
    condition_text: str
    chance_of_rain: int
    chance_of_snow: int
    max_wind_kph: float
    total_precip_mm: float
    avg_humidity: int
    uv: float


@dataclass(frozen=True)
class WeatherForecast:
    location_name: str
    region: str
    country: str
    localtime: str
    days_requested: int
    days: List[ForecastDay]






@mcp.tool(name="get_weather_forecast", description="Get weather forecast")
async def get_weather_forecast(
    location: str,
    *,
    days: int = 3,
    api_key: Optional[str] = None,
    aqi: bool = False,
    alerts: bool = False,
    lang: Optional[str] = None,
    dt: Optional[str] = None,
    timeout_s: float = 10.0,
) -> WeatherForecast:
    """
    WeatherAPI forecast (daily) for a location using /forecast.json.

    WeatherAPI docs notes:
      - 'days' range: 1..14
      - If 'days' is omitted, only today's weather is returned
      - 'dt' can restrict date output for Forecast between today and next 14 days

    Args:
        location: WeatherAPI 'q' (e.g., "Pune", "48.8567,2.3508", "auto:ip", "iata:DXB")
        days: number of forecast days (1..14)
        api_key: WeatherAPI key, else reads WEATHERAPI_KEY from environment
        aqi: include air quality data (aqi=yes|no)
        alerts: include weather alerts (alerts=yes|no)
        lang: optional language code for condition text
        dt: optional date (YYYY-MM-DD) to restrict forecast output
        timeout_s: requests timeout

    Returns:
        WeatherForecast with normalized daily summaries.
    """
    if not (1 <= days <= 14):
        raise ValueError("days must be between 1 and 14 per WeatherAPI forecast limits.")

    api_key = api_key or os.getenv("WEATHERAPI_KEY")
    if not api_key:
        raise WeatherAPIError("Missing API key. Provide api_key or set WEATHERAPI_KEY env var.")

    url = "https://api.weatherapi.com/v1/forecast.json"
    params: Dict[str, Any] = {
        "key": api_key,
        "q": location,
        "days": days,                       # 1..14
        "aqi": "yes" if aqi else "no",
        "alerts": "yes" if alerts else "no",
    }
    if lang:
        params["lang"] = lang
    if dt:
        params["dt"] = dt

    resp = requests.get(url, params=params, timeout=timeout_s)
    resp.raise_for_status()
    data = resp.json()

    if isinstance(data, dict) and "error" in data:
        err = data["error"] or {}
        raise WeatherAPIError(f"WeatherAPI error (code={err.get('code')}): {err.get('message')}")

    loc = data["location"]
    forecast_days = data.get("forecast", {}).get("forecastday", []) or []

    out_days: List[ForecastDay] = []
    for d in forecast_days:
        day = d.get("day", {}) or {}
        cond = day.get("condition", {}) or {}

        out_days.append(
            ForecastDay(
                date=str(d.get("date", "")),
                max_temp_c=float(day.get("maxtemp_c", 0.0)),
                min_temp_c=float(day.get("mintemp_c", 0.0)),
                avg_temp_c=float(day.get("avgtemp_c", 0.0)),
                condition_text=str(cond.get("text", "")),
                chance_of_rain=int(day.get("daily_chance_of_rain", 0) or 0),
                chance_of_snow=int(day.get("daily_chance_of_snow", 0) or 0),
                max_wind_kph=float(day.get("maxwind_kph", 0.0)),
                total_precip_mm=float(day.get("totalprecip_mm", 0.0)),
                avg_humidity=int(day.get("avghumidity", 0) or 0),
                uv=float(day.get("uv", 0.0)),
            )
        )

    return WeatherForecast(
        location_name=str(loc.get("name", "")),
        region=str(loc.get("region", "")),
        country=str(loc.get("country", "")),
        localtime=str(loc.get("localtime", "")),
        days_requested=days,
        days=out_days,
    )


    # Example:
    # os.environ["WEATHERAPI_KEY"] = "<your_key>"
    # fc = get_weather_forecast("Pune", days=5, alerts=True)
    # for d in fc.days:
    #     print(d.date, d.max_temp_c, d.condition_text)

### ----------------------###

## Run MCP server with streamable-http transport
# if __name__ == "__main__":
#     mcp.run(transport="streamable-http", host="127.0.0.1", port=8002)    # with streamable-http transport
    # mcp.run()                             # with stdio transport


## Run MCP server with stdio transport
if __name__ == "__main__":
    mcp.run(transport="stdio")
