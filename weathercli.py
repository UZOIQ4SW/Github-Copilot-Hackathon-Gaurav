import json
import urllib
import requests
import typer
from datetime import datetime
from decouple import config
from rich import print
from rich.console import Console
from rich.panel import Panel

import logging

API_KEY = config('API_KEY')
# Create and configure logger
logging.basicConfig(filename="weather.log", format='%(asctime)s %(message)s',filemode='a')
 
# Creating an object
logger = logging.getLogger()
    
# Setting the threshold of logger to INFO
logger.setLevel(logging.INFO)
 
    
# app info 
app = typer.Typer(
    name="Weather CLI (Built by @AtharvaShah) with the power of Github Copilot 🎯",
    add_completion=False,
    rich_markup_mode="rich",
    help="📕[bold green] Easy to use weather data fetcher and forecaster right within your terminal [/bold green]",
)

def print_weather(data):
    """
    This function takes in a dictionary of weather data, which is a JSON response from the API request and prints out the current weather information and forecast for the given location.
    The dictionary must contain location, current, and forecast keys. The location key must contain name, region, and country subkeys.
    The current key must contain temp_f, temp_c, condition, wind_mph, wind_dir, and humidity subkeys.
    The forecast key must contain forecastday subkeys, which is a list of dictionaries. Each dictionary must contain date, day, and condition subkeys.
    The function does not return anything.
    """
    
    # get the current location
    location = data['location']['name']
    region = data['location']['region']
    country = data['location']['country']
    address = f"{location}, {region}, {country}"

    current_temp_farenheit = data['current']['temp_f']
    current_temp_celsius = data['current']['temp_c']
    current_condition = data['current']['condition']['text']

    current_wind_mph = data['current']['wind_mph']
    current_wind_direction = data['current']['wind_dir']
    current_humidity = data['current']['humidity']


    print(f"📍     Location: {address}")
    print(f"🌡️      Current Temperature: {current_temp_celsius}°C")
    print(f"🌬️      Current Wind: {current_wind_mph} mph, {current_wind_direction}")
    print(f"💧     Current Humidity: {current_humidity}%")
    print(f"🌤️      Current Condition: {current_condition}")
    
    total_forecast_days = len(data['forecast']['forecastday'])
    for day in range(total_forecast_days):
        day_json = data['forecast']['forecastday'][day]
        date = day_json['date']
        
        # convert date to datetime object and then into human readable format
        date = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B %Y')
        
        
        print(f"📅     Forecast for {date}")
        max_temp_celsius = day_json['day']['maxtemp_c']
        min_temp_celsius = day_json['day']['mintemp_c']
        avg_temp_celsius = day_json['day']['avgtemp_c']
        max_wind_kph = day_json['day']['maxwind_kph']
        total_precip_mm = day_json['day']['totalprecip_mm']
        condition = day_json['day']['condition']['text']
        uv = day_json['day']['uv']
        
        print(f"📈     Max Temperature: {max_temp_celsius}°C")
        print(f"📉     Min Temperature: {min_temp_celsius}°C")
        print(f"🌡️      Avg Temperature: {avg_temp_celsius}°C")
        print(f"🌬️      Max Wind: {max_wind_kph} kph")
        print(f"💧     Total Precipitation: {total_precip_mm} mm")
        print(f"🌤️      Condition: {condition}")
        print(f"🌞      UV: {uv}")
        print()
        


@app.command(rich_help_panel="Weather CLI", help="🎫 Get the weather forecast for a city",)
def forecast(city:str = typer.Argument(..., help="🏙️ City name")):
    """
    This function is a command-line interface that retrieves the 5-day weather forecast for a given city using the WeatherAPI. It first checks if the data.json file exists, and if it does and the city name and date match, it retrieves the data from the file. Otherwise, it makes a GET request to the WeatherAPI to retrieve the data, adds a "fetched_on" field to the JSON data, and saves the data to the data.json file. If there is an error with the request, it prints an error message. The function takes one argument, the city name as a string, and has no return value.
    """
    try:
        data = None
        file_exists = False

        # Check if the data.json file exists
        try:
            with open('data.json') as f:
                data = json.load(f)
            file_exists = True
        except FileNotFoundError:
            pass

        if file_exists:
            # check if city.lower is a substring of data['location']['name'].lower()
            name_exists = city.lower() in data['location']['name'].lower() 
            fetched_today = data['fetched_on'].split(',')[0] == datetime.now().strftime("%d %B %Y")
            no_errors = not data.get('error')

            if name_exists and fetched_today and no_errors:
                logger.info(msg=f"**CACHE HIT!** User requested for ***{city}***.")
                print_weather(data)
                return

        logger.info(msg=f"**CACHE MISS!** Making a request to the WeatherAPI for ***{city}***.")
        # Add parameters to the URL
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=5&aqi=no&alerts=no"

        # Send GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Get JSON response
            data = response.json()

            # Check if the response contains any errors
            if 'error' not in data:
                # Add a field to the JSON data called "fetched_on" and set it to the current date
                data['fetched_on'] = datetime.now().strftime("%d %B %Y, %H:%M:%S")

                # Dump to a JSON file
                with open('data.json', 'w') as f:
                    json.dump(data, f)
                print_weather(data)
            else:
                print(f"Error: {data['error']['message']}")
        else:
            print("Error: Failed to retrieve weather data.")

    except KeyError:
        print("[red b]🚨 The city you entered does not exist.[/red b] Please try again.")
    except requests.exceptions.Timeout:
        print("The server didn't respond. Please try again later.")
    except requests.exceptions.TooManyRedirects:
        print("The URL was bad. Try a different one.")
    except requests.exceptions.RequestException as e:
        raise SystemExit(e) from e
    

if __name__ == "__main__":
    app()