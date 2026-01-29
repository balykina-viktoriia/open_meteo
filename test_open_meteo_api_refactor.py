import requests
import pytest

class TestWeatherForecast:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    def get_forecast(self, latitude, longitude, hourly="temperature_2m"):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": hourly
        }
        return requests.get(self.BASE_URL, params=params, timeout=10)
    @pytest.mark.parametrize(
        "latitude, longitude, city_name",
        [
            (49.2497, -123.1193, "Vancouver"),
            (41.8781, -87.6298, "Chicago"),
            (35.6762, 139.6503, "Tokyo"),
            (55.7558, 37.6173, "Moscow"),
        ],
        )
    def test_get_weather_forecast_success(self, latitude, longitude, city_name):
        response = self.get_forecast(latitude, longitude)
        assert response.status_code == 200, "Failed for {city_name}"

        data = response.json()

        assert "hourly" in data
        assert "temperature_2m" in data["hourly"]
        assert "time" in data["hourly"]

        times = data["hourly"]["time"]
        temps = data["hourly"]["temperature_2m"]

        assert len(times) == len(temps)
        assert len(times) > 0

    @pytest.mark.parametrize("invalid_lat", [91, -100, 999])
    def test_invalid_latitude_is_handled(self, invalid_lat):
        response = self.get_forecast(invalid_lat, 0)
        assert response.status_code == 400, "Failed for {invalid_lat}"