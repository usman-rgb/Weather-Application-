import requests
import os
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")

# Retrieve API key from environment variables
user_api = os.environ.get('current_weather_data')
if not user_api:
    print("API key is missing. Please set the 'current_weather_data' environment variable.")
    exit()

# Get location input
location = input("Enter the city name: ").strip()

# Base URL for OpenWeatherMap
weather_url = "https://api.openweathermap.org/data/2.5/"

# Retrieve current weather data
complete_api_link = f"{weather_url}weather?q={location}&appid={user_api}"
api_link = requests.get(complete_api_link)
if api_link.status_code != 200:
    print("Error: Unable to retrieve data. Check the city name or try again later.")
    exit()
api_data = api_link.json()
if api_data.get("cod") != 200:
    print(f"Error: {api_data.get('message', 'Invalid request.')}")
    exit()

# Extract weather information
temp_city = api_data['main']['temp'] - 273.15
feels_like = api_data['main']['feels_like'] - 273.15
weather_desc = api_data['weather'][0]['description']
hmdt = api_data['main']['humidity']
pressure = api_data['main']['pressure']
transparency = api_data.get('visibility', 'N/A')
wind_spd = api_data['wind']['speed']
sunrise = datetime.fromtimestamp(api_data['sys']['sunrise'], tz=timezone.utc).strftime('%I:%M:%S %p')
sunset = datetime.fromtimestamp(api_data['sys']['sunset'], tz=timezone.utc).strftime('%I:%M:%S %p')
date_time = datetime.now().strftime('%d %b %Y || %I:%M:%S %p')

# Retrieve weather forecast
def get_forecast():
    forecast_url = f"{weather_url}forecast?q={location}&appid={user_api}&units=metric"
    response = requests.get(forecast_url).json()
    if response.get("cod") != "200":
        print("Error retrieving forecast data.")
        return []
    forecasts = []
    for item in response['list']:
        forecast_time = item['dt_txt']
        temp = item['main']['temp']
        desc = item['weather'][0]['description']
        forecasts.append((forecast_time, temp, desc))
    return forecasts

forecast_data = get_forecast()

# Retrieve historical weather data
def get_historical():
    one_day_ago = int((datetime.now() - timedelta(days=1)).timestamp())
    history_url = f"{weather_url}onecall/timemachine?lat={api_data['coord']['lat']}&lon={api_data['coord']['lon']}&dt={one_day_ago}&appid={user_api}&units=metric"
    response = requests.get(history_url).json()
    if 'current' not in response:
        print("Error retrieving historical weather data.")
        return None
    return response['current']

historical_data = get_historical()

# Display weather information
print("-------------------------------------------------------------")
print(f"Weather Stats for - {location.upper()} || {date_time}")
print("-------------------------------------------------------------")
print(f"Current temperature : {temp_city:.2f}°C")
print(f"Feels like temperature : {feels_like:.2f}°C")
print(f"Current weather : {weather_desc}")
print(f"Humidity : {hmdt}%")
print(f"Pressure : {pressure} hPa")
print(f"Visibility : {transparency} meters")
print(f"Wind speed : {wind_spd} km/h")
print(f"Sunrise at : {sunrise}")
print(f"Sunset at : {sunset}")

if forecast_data:
    print("\nWeather Forecast (Next 5 Days):")
    for time, temp, desc in forecast_data[:5]:
        print(f"{time}: {temp:.2f}°C, {desc}")

if historical_data:
    print("\nHistorical Weather Data (Yesterday):")
    print(f"Temperature: {historical_data['temp']:.2f}°C")
    print(f"Weather: {historical_data['weather'][0]['description']}")

# Plot the forecast data with temperature, wind speed, and humidity
def plot_weather_data(data, location):
    times = [datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S') for item in data]
    temps = [item[1] for item in data]
    wind_speeds = [wind_spd] * len(data)  # Assuming wind speed stays constant for simplicity
    humidities = [hmdt] * len(data)  # Assuming humidity stays constant for simplicity

    plt.figure(figsize=(12, 6))

    # Plot temperature
    plt.plot(times, temps, marker='o', color='royalblue', label='Temperature (°C)', linestyle='-', linewidth=2)

    # Plot wind speed
    plt.plot(times, wind_speeds, marker='x', color='orange', label='Wind Speed (km/h)', linestyle='--', linewidth=2)

    # Plot humidity
    plt.plot(times, humidities, marker='^', color='green', label='Humidity (%)', linestyle=':', linewidth=2)

    # Formatting and labels
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %d %I:%M %p'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.HourLocator(interval=6))
    plt.gcf().autofmt_xdate()

    plt.title(f"5-Day Weather Forecast for {location.capitalize()}", fontsize=16, fontweight='bold')
    plt.xlabel("Date & Time", fontsize=12)
    plt.ylabel("Values", fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(f"{location}_weather_trends.png", dpi=300, bbox_inches='tight')
    plt.show()

# Example usage with forecast data
if forecast_data:
    # Assuming each item contains a tuple (forecast_time, temp, desc)
    plot_weather_data(forecast_data[:10], location)

# Save weather data to a file
save_data = input("Would you like to save the weather data? (yes/no): ").strip().lower()
if save_data == 'yes':
    with open(f"{location}_weather.txt", "w") as file:
        file.write("-------------------------------------------------------------\n")
        file.write(f"Weather Stats for - {location.upper()}  || {date_time}\n")
        file.write("-------------------------------------------------------------\n")
        file.write(f"Current temperature     : {temp_city:.2f}°C\n")
        file.write(f"Feels like temperature  : {feels_like:.2f}°C\n")
        file.write(f"Current weather         : {weather_desc}\n")
        file.write(f"Humidity                : {hmdt}%\n")
        file.write(f"Pressure                : {pressure} hPa\n")
        file.write(f"Visibility              : {transparency} meters\n")
        file.write(f"Wind speed              : {wind_spd} km/h\n")
        file.write(f"Sunrise at              : {sunrise}\n")
        file.write(f"Sunset at               : {sunset}\n")
        if forecast_data:
            file.write("\nWeather Forecast (Next 5 Days):\n")
            for time, temp, desc in forecast_data:
                file.write(f"{time}: {temp:.2f}°C, {desc}\n")
        if historical_data:
            file.write("\nHistorical Weather Data (Yesterday):\n")
            file.write(f"Temperature: {historical_data['temp']:.2f}°C\n")
            file.write(f"Weather: {historical_data['weather'][0]['description']}\n")
    print(f"Weather data saved to {location}_weather.txt.")