import requests
import pandas as pd

# Define a class to store weather data for a city
class WeatherData:
    def __init__(self, city, description, temperature, humidity, wind_speed):
        self.city = city
        self.description = description
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed

# Function to retrieve weather data for a given city
def get_weather(city_name, api_key):
    # Construct the API request URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    # Send the request to the OpenWeatherMap API
    response = requests.get(url)
    data = response.json()
    
    # Check if the request was successful (status code 200)
    if data.get("cod") == 200:
        # Extract weather description, temperature, humidity, and wind speed from the response
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        # Create a WeatherData object to store the weather data
        return WeatherData(city_name, description, temperature, humidity, wind_speed)
    else:
        # If the request was unsuccessful, print an error message
        print(f"Weather data for {city_name} not found.")
        return None

# Function to save weather data to a CSV file
def save_weather_data(weather_data_list, filename):
    try:
        # Convert the list of WeatherData objects to a pandas DataFrame
        df = pd.DataFrame(weather_data_list)
        # Save the DataFrame to a CSV file
        df.to_csv(filename, index=False)
        # Print a message indicating that the data has been saved
        print(f"Weather data saved to {filename}")
    except Exception as e:
        # If an error occurs while saving the data, print an error message
        print(f"Error saving weather data: {e}")

# Function to display weather details for a given city
def display_weather_details(weather_data):
    if not weather_data:
        print("No weather data available.")
        return
    
    # Print weather details for the city
    print(f"Weather details for {weather_data.city}:")
    print(f"Weather Description: {weather_data.description}")
    print(f"Temperature: {weather_data.temperature}°C")
    print(f"Humidity: {weather_data.humidity}%")
    print(f"Wind Speed: {weather_data.wind_speed} m/s")
    print()
    
    # Check for warnings based on weather description
    if "storm" in weather_data.description.lower():
        print("Warning: Possible storm in the area!")
    elif "hurricane" in weather_data.description.lower():
        print("Warning: Hurricane expected!")
    elif "tornado" in weather_data.description.lower():
        print("Warning: Tornado alert!")
    elif "flood" in weather_data.description.lower():
        print("Warning: Risk of flooding!")
    elif "wildfire" in weather_data.description.lower():
        print("Warning: Wildfire alert!")
    elif "blizzard" in weather_data.description.lower():
        print("Warning: Blizzard conditions possible!")
    else:
        print("No specific warnings for this area.")
    
    # Provide suggestions based on weather description and temperature
    if "clear" in weather_data.description.lower() and weather_data.temperature > 25:
        print("It's a sunny day! Don't forget to put on sunscreen.")
    elif "rain" in weather_data.description.lower():
        print("It's a rainy day! Don't forget your umbrella.")
    elif "cloud" in weather_data.description.lower():
        print("It's a cloudy day. Bring an umbrella just in case!")
    elif "snow" in weather_data.description.lower():
        print("It's a snowy day! Bundle up and drive safely.")
    else:
        print("Enjoy the weather!")

if __name__ == "__main__":
    # OpenWeatherMap API key
    api_key = "7a42cf2fdc0aa8edf6285e3267f1389f"
    # List to store cities
    cities = []

    # Loop to input city names
    while True:
        city = input("Enter city name (or type 'done' to finish): ").strip()
        if city.lower() == 'done':
            break
        cities.append(city)

    # List to store weather data for each city
    weather_data_list = []
    # Retrieve weather data for each city
    for city in cities:
        weather_data = get_weather(city, api_key)
        if weather_data:
            weather_data_list.append(weather_data)
            display_weather_details(weather_data)
            print()

    # Save weather data to a CSV file
    if weather_data_list:
        filename = "weather_data.csv"
        save_weather_data(weather_data_list, filename)
