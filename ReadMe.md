# Weather Forecasting Tool

This is a command-line tool that fetches and displays the current weather forecast for a specific city. It leverages the OpenWeatherMap API to retrieve weather data and utilizes Python for data parsing and manipulation. The purpose of this tool is to provide an easy and efficient way to access accurate and up-to-date weather information, allowing users to plan their outdoor activities, travel, and day-to-day decision making.

## Features

- Fetches weather data using the [WeatherAPI.com API](https://www.weatherapi.com/)
- Retrieves current weather forecast for a specific city
- Command-line interface for quick and convenient access
- Efficient and simple tool, eliminating the need for complex graphical interfaces or websites

## Technologies Used

- Python: A versatile and popular programming language that enables efficient data manipulation and parsing.
- GitHub Copilot: An AI-powered coding assistant that aids in API usage, data parsing, and error handling.
- WeatherAPI.com API: A comprehensive weather data API offering a wide range of weather information for locations worldwide.

## GitHub Copilot Integration

GitHub Copilot plays a significant role in the development of this tool. It assists in various aspects, including:

- API Usage: GitHub Copilot generates API requests, including the endpoint, parameters, and authentication, simplifying integration with the WeatherAPI.com API.
- Data Parsing: Copilot provides suggestions and code snippets for parsing the JSON or XML responses from the WeatherAPI.com API, making it easier to extract the relevant weather data.
- Error Handling: GitHub Copilot offers guidance on implementing error handling mechanisms, such as exception handling and error status code checks, ensuring a robust and reliable tool.

## Usage

To use the Weather Forecasting Tool, follow these steps:

1. Clone the repository from GitHub.
2. Install the required dependencies.

```
pip install -r requirements.txt
```

3. Create a free account on [WeatherAPI.com](https://www.weatherapi.com/) and obtain an API key. Paste the API Key in the .env file.

```py
# .env file
API_KEY=<your-api-key>
```

4. Run the command-line tool and provide the name of the city for which you want to retrieve the weather forecast.

```py
# cd into the weathercli folder
cd weathercli
python -m weathercli forecast <city-name>

# Example
python -m weathercli forecast London

# wrap city name in quotes if it contains spaces
python -m weathercli forecast "New York"
```

5. The tool will fetch the weather data from the WeatherAPI.com API and display the current forecast for the specified city.

## Run Tests 👇🏻

```
# Move to source folder
cd weathercli

# Run all tests
python -m pytest ../tests
```

## Contribution

This project was developed as part of the TechGig Microsoft Github Co-Pilot Hackathon. Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please submit a pull request or open an issue on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to modify and distribute it according to the terms of the license.
