from __future__ import annotations

import os
from typing import Any, Optional, Dict
from dotenv import load_dotenv

load_dotenv()

import requests


class WeatherAPIError(RuntimeError):
    """Raised when WeatherAPI returns an error or an unexpected response."""


def get_realtime_weather(
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



weather = get_realtime_weather("Pune", aqi=True)
print(weather["location"]["name"], weather["current"]["temp_c"], weather["current"]["condition"]["text"])


# Example usage:
# weather = get_realtime_weather("Pune", aqi=True)
# print(weather["location"]["name"], weather["current"]["temp_c"], weather["current"]["condition"]["text"])