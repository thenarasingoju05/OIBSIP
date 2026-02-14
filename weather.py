import os
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# -----------------------------------
# CONFIGURATION
# -----------------------------------
# Prefer environment variable for API key; fall back to hardcoded if set.
API_KEY = os.getenv("OPENWEATHER_API_KEY", "API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Optional proxy support via environment variables `HTTP_PROXY` / `HTTPS_PROXY`


def _session_with_retries(retries=3, backoff_factor=0.5, status_forcelist=(500, 502, 503, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_weather(city):
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        print("❌ Please set your OpenWeatherMap API key in the OPENWEATHER_API_KEY env var.")
        return

    params = {"q": city, "appid": API_KEY, "units": "metric"}

    session = _session_with_retries()

    # Apply explicit proxy configuration if provided via environment variables.
    # Supports HTTP_PROXY, HTTPS_PROXY, lower-case variants, or a generic PROXY_URL.
    http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
    generic_proxy = os.getenv("PROXY_URL") or os.getenv("proxy_url")
    if generic_proxy and not (http_proxy or https_proxy):
        http_proxy = http_proxy or generic_proxy
        https_proxy = https_proxy or generic_proxy

    if http_proxy or https_proxy:
        proxies = {}
        if http_proxy:
            proxies["http"] = http_proxy
        if https_proxy:
            proxies["https"] = https_proxy
        session.proxies.update(proxies)
        print("Using proxy:", proxies)

    try:
        response = session.get(BASE_URL, params=params, timeout=10)
    except requests.RequestException as e:
        print("❌ Network error:", e)
        return

    if not response.ok:
        print(f"❌ API returned status {response.status_code}")
        print("Response body:", response.text)
        return

    try:
        data = response.json()
    except ValueError:
        print("❌ Failed to parse JSON from API response.")
        print("Status:", response.status_code)
        print("Body:", response.text)
        return

    # Safely extract fields
    temperature = data.get("main", {}).get("temp")
    humidity = data.get("main", {}).get("humidity")
    weather = None
    if isinstance(data.get("weather"), list) and data["weather"]:
        weather = data["weather"][0].get("description")

    # Display output
    print("\n🌍 Weather Report")
    print("---------------------")
    print(f"City        : {city}")
    print(f"Temperature : {temperature} °C")
    print(f"Humidity    : {humidity} %")
    print(f"Condition   : {weather.capitalize() if weather else 'N/A'}")

# -----------------------------------
# MAIN PROGRAM
# -----------------------------------
if __name__ == "__main__":
    city_name = input("Enter city name: ")
    get_weather(city_name)
