import os
import requests
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox


# Function to fetch weather data
def fetch_weather():
    user_api = os.environ.get('current_weather_data')
    if not user_api:
        messagebox.showerror("Error", "API key is missing. Set the 'current_weather_data' environment variable.")
        return
    
    location = city_input.get().strip()
    if not location:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    
    complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={user_api}"
    response = requests.get(complete_api_link)
    
    if response.status_code != 200:
        messagebox.showerror("Error", "Could not retrieve weather data. Please check the city name.")
        return
    
    api_data = response.json()
    if api_data.get("cod") != 200:
        messagebox.showerror("Error", api_data.get('message', 'Invalid request.'))
        return
    
    # Extract weather data
    temp_city = api_data['main']['temp'] - 273.15
    feels_like = api_data['main']['feels_like'] - 273.15
    weather_desc = api_data['weather'][0]['description']
    hmdt = api_data['main']['humidity']
    pressure = api_data['main']['pressure']
    transparency = api_data.get('visibility', 'N/A')
    wind_spd = api_data['wind']['speed']
    sunrise = datetime.utcfromtimestamp(api_data['sys']['sunrise']).strftime('%I:%M:%S %p')
    sunset = datetime.utcfromtimestamp(api_data['sys']['sunset']).strftime('%I:%M:%S %p')
    date_time = datetime.now().strftime('%d %b %Y || %I:%M:%S %p')
    
    # Update output box
    output_text = (
        f"Weather Stats for - {location.upper()} || {date_time}\n"
        f"-------------------------------------------------------------\n"
        f"Current temperature : {temp_city:.2f}°C\n"
        f"Feels like temperature : {feels_like:.2f}°C\n"
        f"Current weather : {weather_desc}\n"
        f"Humidity : {hmdt}%\n"
        f"Pressure : {pressure} hPa\n"
        f"Visibility : {transparency} meters\n"
        f"Wind speed : {wind_spd} km/h\n"
        f"Sunrise at : {sunrise}\n"
        f"Sunset at : {sunset}\n"
    )
    output_box.delete("1.0", ctk.END)
    output_box.insert(ctk.END, output_text)


# Initialize the GUI
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Weather App")

# Input and button
city_input = ctk.CTkEntry(root, placeholder_text="Enter city name")
city_input.pack(pady=10, padx=10, fill="x")

fetch_button = ctk.CTkButton(root, text="Get Weather", command=fetch_weather)
fetch_button.pack(pady=5)

# Output box
output_box = ctk.CTkTextbox(root, height=200)
output_box.pack(pady=10, padx=10, fill="both", expand=True)

# Dark mode toggle
def toggle_mode():
    mode = ctk.get_appearance_mode()
    ctk.set_appearance_mode("light" if mode == "dark" else "dark")

dark_mode_toggle = ctk.CTkSwitch(root, text="Dark Mode", command=toggle_mode)
dark_mode_toggle.pack(pady=5)

# Run the app
root.geometry("600x400")
root.mainloop()
