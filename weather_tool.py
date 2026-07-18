import requests

def get_weather(city: str) -> str:
    """Fetches current weather for a city using the free Open-Meteo API (no API key required)."""
    try:
        # Step 1: Geocode the city name to lat/lon
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_resp = requests.get(geo_url, params={"name": city, "count": 1, "language": "en"}, timeout=10)
        geo_data = geo_resp.json()

        if "results" not in geo_data or len(geo_data["results"]) == 0:
            return f"Could not find a location named '{city}'. Please try a more specific city name."

        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        resolved_name = location.get("name", city)
        country = location.get("country", "")

        # Step 2: Fetch current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m",
            "timezone": "auto"
        }
        weather_resp = requests.get(weather_url, params=weather_params, timeout=10)
        weather_data = weather_resp.json()

        current = weather_data.get("current", {})
        units = weather_data.get("current_units", {})

        temp = current.get("temperature_2m", "N/A")
        feels_like = current.get("apparent_temperature", "N/A")
        humidity = current.get("relative_humidity_2m", "N/A")
        wind_speed = current.get("wind_speed_10m", "N/A")
        wind_dir = current.get("wind_direction_10m", "N/A")
        weather_code = current.get("weather_code", -1)

        # Map WMO weather codes to human-readable descriptions
        condition = _decode_weather_code(weather_code)

        temp_unit = units.get("temperature_2m", "°C")
        wind_unit = units.get("wind_speed_10m", "km/h")

        summary = (
            f"Weather in {resolved_name}, {country}:\n"
            f"• Condition: {condition}\n"
            f"• Temperature: {temp}{temp_unit} (feels like {feels_like}{temp_unit})\n"
            f"• Humidity: {humidity}%\n"
            f"• Wind: {wind_speed} {wind_unit} from {wind_dir}°"
        )

        return summary

    except requests.exceptions.Timeout:
        return "Weather service timed out. Please try again."
    except Exception as e:
        print(f"WEATHER ERROR: {e}")
        return f"Failed to fetch weather: {str(e)}"


def _decode_weather_code(code: int) -> str:
    """Converts WMO weather interpretation codes to human-readable strings."""
    weather_codes = {
        0: "Clear sky ☀️",
        1: "Mainly clear 🌤️",
        2: "Partly cloudy ⛅",
        3: "Overcast ☁️",
        45: "Foggy 🌫️",
        48: "Depositing rime fog 🌫️",
        51: "Light drizzle 🌦️",
        53: "Moderate drizzle 🌦️",
        55: "Dense drizzle 🌧️",
        56: "Light freezing drizzle 🌧️",
        57: "Dense freezing drizzle 🌧️",
        61: "Slight rain 🌧️",
        63: "Moderate rain 🌧️",
        65: "Heavy rain 🌧️",
        66: "Light freezing rain 🌧️",
        67: "Heavy freezing rain 🌧️",
        71: "Slight snowfall ❄️",
        73: "Moderate snowfall ❄️",
        75: "Heavy snowfall ❄️",
        77: "Snow grains ❄️",
        80: "Slight rain showers 🌦️",
        81: "Moderate rain showers 🌦️",
        82: "Violent rain showers ⛈️",
        85: "Slight snow showers 🌨️",
        86: "Heavy snow showers 🌨️",
        95: "Thunderstorm ⛈️",
        96: "Thunderstorm with slight hail ⛈️",
        99: "Thunderstorm with heavy hail ⛈️",
    }
    return weather_codes.get(code, f"Unknown (code {code})")
