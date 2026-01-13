import requests

def test_get_weather_forecast_success():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 49.2497,
        "longitude": -123.1193,
        "hourly": "temperature_2m"
    }

    response = requests.get(url, params=params, timeout=10)

    assert response.status_code == 200

    data = response.json()

    assert "hourly" in data
    assert "temperature_2m" in data["hourly"]