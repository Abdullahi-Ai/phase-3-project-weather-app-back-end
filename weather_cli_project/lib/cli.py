from db.models import get_engine, get_session, City, WeatherReport
from config import OPENWEATHER_API_KEY
import requests
from tabulate import tabulate


def fetch_weather_from_api(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": OPENWEATHER_API_KEY, "units": "metric"}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code != 200 or "main" not in data:
            print(f"City not found or API error: {data.get('message', 'Unknown error')}", flush=True)
            return None

        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        actual_name = data["name"]
        return actual_name, temperature, description

    except Exception as e:
        print(f"Error fetching data: {e}", flush=True)
        return None


def city_menu(session):
    while True:
        print("\n--- Cities Menu ---")
        print("1. Create City")
        print("2. Delete City")
        print("3. List All Cities")
        print("4. Find City by Name")
        print("5. View Weather Reports for a City")
        print("6. Back to Main Menu")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            name = input("Enter city name to create: ").strip()
            if not name:
                print("City name cannot be empty.")
                continue
            existing = City.find_by_name(session, name)
            if existing:
                print(f"City '{name}' already exists.")
                continue
            city = City.create(session, name)
            session.commit()
            print(f"City '{city.name}' created.")

        elif choice == "2":
            city_id = input("Enter city ID to delete: ").strip()
            if not city_id.isdigit():
                print("Invalid ID. Must be a number.")
                continue
            city = City.find_by_id(session, int(city_id))
            if not city:
                print("City not found.")
                continue
            
            reports = WeatherReport.find_by_city_id(session, city.id)
            for r in reports:
                r.delete(session)
            city.delete(session)
            session.commit()
            print(f"City and related weather reports deleted.")

        elif choice == "3":
            cities = City.get_all(session)
            if not cities:
                print("No cities found.")
            else:
                table = [(c.id, c.name) for c in cities]
                print(tabulate(table, headers=["ID", "Name"], tablefmt="pretty"))

        elif choice == "4":
            name = input("Enter city name to search the weather: ").strip()
            results = City.find_by_name(session, name)
            if not results:
                print("No city found with that name.")
            else:
                table = [(c.id, c.name) for c in results]
                print(tabulate(table, headers=["ID", "Name"], tablefmt="pretty"))

        elif choice == "5":
            city_id = input("Enter city ID to view weather reports: ").strip()
            if not city_id.isdigit():
                print("The invalid id must be the number.")
                continue
            city = City.find_by_id(session, int(city_id))
            if not city:
                print("City not found.")
                continue
            reports = WeatherReport.find_by_city_id(session, city.id)
            if not reports:
                print(f"No weather reports found for {city.name}.")
            else:
                table = [(r.id, r.temperature_c, r.description) for r in reports]
                print(f"Weather Reports for {city.name}:")
                print(tabulate(table, headers=["ID", "Temperature (°C)", "Description"], tablefmt="pretty"))

        elif choice == "6":
            break

        else:
            print("Invalid option. Try again.")


def weather_menu(session):
    while True:
        print("\n--- Weather Reports Menu ---")
        print("1. List All Weather Reports")
        print("2. Find Weather Report by ID")
        print("3. Delete Weather Report by ID")
        print("4. Back to Main Menu")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            reports = WeatherReport.get_all(session)
            if not reports:
                print("No weather reports found.")
            else:
                table = [(r.id, r.city_id, r.temperature_c, r.description) for r in reports]
                print(tabulate(table, headers=["ID", "City ID", "Temperature (°C)", "Description"], tablefmt="pretty"))

        elif choice == "2":
            report_id = input("Enter weather report ID: ").strip()
            if not report_id.isdigit():
                print("Invalid ID. Must be a number.")
                continue
            report = WeatherReport.find_by_id(session, int(report_id))
            if not report:
                print("Sorry, weather report has not been found.")
            else:
                table = [(report.id, report.city_id, report.temperature_c, report.description)]
                print(tabulate(table, headers=["ID", "City ID", "Temperature (°C)", "Description"], tablefmt="pretty"))

        elif choice == "3":
            report_id = input("Enter weather report ID to delete: ").strip()
            if not report_id.isdigit():
                print("Invalid ID. Must be a number.")
                continue
            report = WeatherReport.find_by_id(session, int(report_id))
            if not report:
                print("Weather report not found.")
                continue
            report.delete(session)
            session.commit()
            print("Weather report deleted.")

        elif choice == "4":
            break

        else:
            print("Invalid option! Please try again later.")


def main():
    engine = get_engine()
    session = get_session(engine)

    print("Welcome to Osman Weather CLI App")

    while True:
        print("\n--- Main Menu ---")
        print("1. Fetch Weather and Save")
        print("2. Manage Cities")
        print("3. Manage Weather Reports")
        print("4. Exit")

        choice = input("Please choose an option: ").strip()

        if choice == "1":
            city_input = input("Please enter the city name to fetch the weather: ").strip()
            if not city_input:
                print("Sorry, city name can't be empty.")
                continue

            result = fetch_weather_from_api(city_input)
            if not result:
                continue

            actual_name, temperature, description = result

            city = City.find_by_name(session, actual_name)
            city = city[0] if city else City.create(session, actual_name)

            report = WeatherReport.create(session, city, temperature, description)
            session.commit()

            print(f"\nWeather for {actual_name}: {temperature}°C, {description}")

        elif choice == "2":
            city_menu(session)

        elif choice == "3":
            weather_menu(session)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Oops! Sorry, invalid option. Please try again.")

    session.close()


if __name__ == "__main__":
    main()
