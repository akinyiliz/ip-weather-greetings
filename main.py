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

    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        visitor_ip = x_forwarded_for.split(',')[0]
    else:
        visitor_ip = request.client.host

    try:
        # Retrieve visitor's IP address and location info
        response = requests.get(
            f"https://ipinfo.io/json?token={IP_INFO_TOKEN}")
        data = response.json()

        city = data["city"]

        # Fetch weather information from WeatherAPI based on city
        response = requests.get(
            f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}")
        if response.status_code == 200:
            data = response.json()
            temperature = data['current']['temp_c']
        else:
            return "data unavailable"

        # Return response with visitor's IP, location, and greeting message
        return {"client_ip": visitor_ip,
                "location": city,
                "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {city}"
                }

    except requests.exceptions.RequestException as e:
        # Handle errors related to HTTP requests
        raise HTTPException(
            status_code=500, detail="Error fetching data from external API")

    except KeyError as e:
        # Handle errors related to missing data in the API response
        raise HTTPException(
            status_code=500, detail="Missing data in the API response")
