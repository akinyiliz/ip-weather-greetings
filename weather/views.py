import os
import requests
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ImproperlyConfigured


load_dotenv()


class HelloView(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get(self, request):
        visitor_name = request.GET.get('visitor_name', 'Guest')
        ip_info_token = os.getenv("IP_INFO_TOKEN")
        weather_api_key = os.getenv("WEATHER_API_KEY")

        if not ip_info_token or not weather_api_key:
            raise ImproperlyConfigured(
                "API keys not set in environment variables.")

        # Get visitor's IP address
        visitor_ip = self.get_client_ip(request)

        response = requests.get(
            f"https://ipinfo.io/{visitor_ip}json?token={ip_info_token}")
        data = response.json()
        print(data)

        city = data.city

        try:
            # Fetch weather information from OpenWeatherMap based on latitude and longitude
            api_url = "https://api.weatherapi.com/v1/current.json?key="+weather_api_key+"&q="+city
            weather_response = requests.get(api_url)
            weather_response.raise_for_status()

            weather_data = weather_response.json()

            temp = weather_data['current']['temp_c']

            # Return response with visitor's IP, location, and greeting message
            return JsonResponse({
                "client_ip": visitor_ip,
                "location": city,
                "greeting": f"Hello, {visitor_name}!, the temperature is {temp} degrees Celsius in {city}"
            })

        except requests.exceptions.RequestException as e:
            # Handle errors related to HTTP requests
            return JsonResponse({"error": "Error fetching data from external API"}, status=500)

        except KeyError as e:
            # Handle errors related to missing data in the API response
            return JsonResponse({"error": "Missing data in the API response"}, status=500)
