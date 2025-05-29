import requests

class WeatherFetcher:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    API_KEY = "80621b22adc11c8bc171962903a64e27"

    def fetch(self, city):
        params = {
            "q": city,
            "appid": self.API_KEY,
            "units": "metric"
        }
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            city_name = data.get("name")
            main = data.get("main", {})
            weather_list = data.get("weather", [])

            if not city_name or "temp" not in main or not weather_list:
                raise ValueError("Incomplete data received from API.")

            return {
                "city": city_name,
                "temperature": main["temp"],
                "description": weather_list[0].get("description", "No description")
            }

        except requests.exceptions.HTTPError as e:
            raise ValueError(f"HTTP error: {e}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Request error: {e}")
        except (KeyError, IndexError, TypeError):
            raise ValueError("Unexpected response format.")
