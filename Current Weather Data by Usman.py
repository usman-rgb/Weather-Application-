import requests
import os
from datetime import datetime


# Use the environment variable to load the API key.
user_api = os.environ.get('current_weather_data') 
if not user_api:
    print("Incorrect API key set. The environment variable 'current_weather_data' needs to be set.")
    exit()

# Get location input
location = input("Enter the city name:") 

# Use to retrieve weather data from the OpenWeatherMap API.
complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={user_api}" 
api_link = requests.get(complete_api_link)


if api_link.status_code!= 200:
    print("Error: Data cannot be retrieved. Please double-check the name of the city or try again later.")
    exit()

api_data = api_link.json() 

if api_data.get("cod") != 200:
    print(f" Error : {api_data.get('message', 'Invalid request.')}")
    exit()

# Retrieve meteorological information

temp_city = api_data ['main'] ['temp'] - 273.15
Feels_like = api_data['main'] ['feels_like'] - 273.15 
Weather_desc = api_data['weather'] [0]['description']
hmdt= api_data['main'] ['humidity']
pressure = api_data ['main'] ['pressure']
transparency = api_data.get('visibility', 'N/A')
wind_spd= api_data ['wind'] ['speed']
sunrise = datetime.utcfromtimestamp(api_data['sys']['sunrise']).strftime('%I:%M:%S %p')
sunset = datetime.utcfromtimestamp(api_data['sys']['sunset']).strftime('%I:%M:%S %p')
date_time = datetime.now().strftime('%d %b %Y || %I:%M:%S %p')


# Show the weather information

print( "-------------------------------------------------------------" )

print(f"Weather Stats for - {location.upper()} || {date_time} ")

print( "-------------------------------------------------------------" )

print(f"Current temperature : {temp_city:.2f}°C" )
print(f"Feels like temperature : {Feels_like:.2f}°C" )
print(f"Current weather : {Weather_desc}" )
print(f"Humidity : {hmdt}%" )
print(f"Pressure : {pressure} hPa" )
print(f"Visibility : {transparency} meters" )
print(f"Wind speed : {wind_spd} km/h" )
print(f"Sunrise at : {sunrise}" )
print(f"Sunset at : {sunset}" )

# Store in a file

save_data = input("Would you like to write down the weather data? (yes/no): ").strip().lower()

if save_data == 'yes':
    with open(f"{location}_weather.txt", "w") as file:
        file.write("-------------------------------------------------------------\n")
        file.write(f"Weather Stats for - {location.upper()}  || {date_time}\n")
        file.write("-------------------------------------------------------------\n")
        file.write(f"Current temperature     : {temp_city:.2f}°C\n")
        file.write(f" Feels like temperature  : {Feels_like:.2f}°C\n")
        file.write(f"Current weather         : {Weather_desc}\n")
        file.write(f"Humidity                : {hmdt}%\n")
        file.write(f"Pressure                : {pressure} hPa\n")
        file.write(f"Visibility              : {transparency} meters\n")
        file.write(f"Wind speed              : {wind_spd} km/h\n")
        file.write(f"Sunrise at              : {sunrise}\n")
        file.write(f"Sunset at               : {sunset}\n")
    print(f"Weather data saved to {location}_weather.txt.")