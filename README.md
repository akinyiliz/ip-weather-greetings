# FastAPI Weather Greeting API

This is a simple FastAPI application that greets visitors with their name and provides weather information based on their IP location.

A challenge from [HNG internship](https://hng.tech/internship) stage 1.

## Endpoint

### `GET /api/hello?visitor_name={visitor_name}`

Returns a personalized greeting message including the visitor's IP, city location, and current temperature.

Response:

```
{
  "client_ip": "127.0.0.1", // The IP address of the requester
  "location": "Nairobi", // The city of the requester
  "greeting": "Hello, Liz!, the temperature is 24 degrees Celcius in Nairobi"
}
```

## Setup

1. **Environment Variables**: Create a `.env` file in the root directory with the following content:

```
WEATHER_API_KEY=your_openweathermap_api_key
```

2. **Installation**: Install dependencies using `pip`:

```bash
pip install -r requirements.txt
```

3. **Running the Server**: Start the FastAPI server:

```bash
fastapi dev app/main.py
```

4. **Usage**: Open your browser or API client and navigate to `http://localhost:8000/api/hello?visitor_name=YourName`.

## Dependencies

- `fastapi`: Web framework for building APIs with Python.
- `requests`: HTTP library for making API requests.
- `geocoder`: Library for retrieving geographical information based on IP addresses.
- `python-dotenv`: Library for loading environment variables from a `.env` file.
