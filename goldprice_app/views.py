from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from .forms import UserRegisterForm
from django.http import JsonResponse
import pandas as pd
from django.conf import settings

# Load city names
file_path = settings.BASE_DIR / 'list_of_cities_and_towns_in_india.csv'
cities_df = pd.read_csv(file_path)
cities = cities_df['Name of City'].str.lower().tolist()

def home(request):
    return render(request, 'goldprice_app/home.html', {'title': 'Home Page'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('home')  # Redirect to home page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'goldprice_app/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'goldprice_app/profile.html', {'user': request.user})

@login_required
def get_gold_prices(request):
    city = request.GET.get('city')
    if city and city.lower() not in cities:
        suggestions = [c for c in cities if c.startswith(city.lower()[:3])]
        suggestion = suggestions[0] if suggestions else 'Lucknow'
        return JsonResponse({"error": f"City '{city}' not found. Did you mean '{suggestion.capitalize()}'?"})

    api_url = "https://gold-rates-india.p.rapidapi.com/api/gold-rates"
    headers = {
        "x-rapidapi-key": '220f62a1cfmsh847f14d13070cd7p1fd5ffjsn9651c928c715',  # Use the key from settings for security
        "x-rapidapi-host": "gold-rates-india.p.rapidapi.com"
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        gold_rates = data.get("GoldRate", [])
        if not gold_rates:
            return JsonResponse({"error": "Could not fetch gold rates."})
        if city:
            city_rate = next((rate for rate in gold_rates if rate["city"].lower() == city.lower()), None)
            if not city_rate:
                return JsonResponse({"error": "City not found."})
            return JsonResponse({
                "city": city_rate["city"],
                "TenGram22K": city_rate["TenGram22K"],
                "TenGram24K": city_rate["TenGram24K"]
            })
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Error occurred: {e}"})
