import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Header, HTTPException

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Fetch the OpenWeatherMap API key and IPInfo token from environment variables
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
IP_INFO_TOKEN = os.getenv("IP_INFO_TOKEN")


@app.get("/api/hello")
async def get_visitor(visitor_name: str,  request: Request):
    """
    Endpoint to greet a visitor with their name and weather information based on their IP location.
    """

    try:
        # Retrieve visitor's IP address and location info
        response = requests.get(
            f"https://ipinfo.io/json?token={IP_INFO_TOKEN}")
        data = response.json()

        visitor_ip = data["ip"]
        location = data["loc"].split(",")

        lat = location[0]
        lon = location[1]

        # Fetch weather information from OpenWeatherMap based on latitude and longitude
        weather_response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={WEATHER_API_KEY}")

        # Check if the request was successful
        weather_response.raise_for_status()

        weather_data = weather_response.json()

        city = weather_data["name"]
        temp = int(weather_data["main"]["feels_like"])

        # Return response with visitor's IP, location, and greeting message
        return {"client_ip": visitor_ip,
                "location": city,
                "greeting": f"Hello, {visitor_name}!, the temperature is {temp} degrees Celcius in {city}"
                }

    except requests.exceptions.RequestException as e:
        # Handle errors related to HTTP requests
        raise HTTPException(
            status_code=500, detail="Error fetching data from external API")

    except KeyError as e:
        # Handle errors related to missing data in the API response
        raise HTTPException(
            status_code=500, detail="Missing data in the API response")
