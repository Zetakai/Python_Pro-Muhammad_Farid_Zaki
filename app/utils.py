import requests
from datetime import datetime, timedelta
import random
import os

def get_user_location_from_ip():
    """
    Coba dapatkan lokasi user dari IP address
    Kalau gagal atau ditolak, return 'Jakarta' sebagai fallback
    """
    try:
        # Pakai ipapi.co untuk geolocation (gratis, no API key needed)
        response = requests.get('https://ipapi.co/json/', timeout=3)
        if response.status_code == 200:
            data = response.json()
            city = data.get('city', 'Jakarta')
            # Kalau city kosong atau error, pakai Jakarta
            if not city or city == 'None':
                return 'Jakarta'
            return city
    except:
        pass
    
    # Fallback ke Jakarta
    return 'Jakarta'

def get_weather_data(city_name):
    """
    Ambil data cuaca dari OpenWeatherMap API
    Return None kalau ada error atau kota tidak ditemukan
    """
    # Load API key dari environment variable (dari .env)
    api_key = os.environ.get('WEATHER_API_KEY')
    
    # Kalau API key belum di-set, return None
    if not api_key:
        return None
    
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    
    try:
        params = {
            'q': city_name,
            'appid': api_key,
            'units': 'metric',
            'lang': 'id'  # Bahasa Indonesia
        }
        
        response = requests.get(base_url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Ambil data untuk 3 hari ke depan
            forecasts = []
            today = datetime.now().date()
            
            # Group by date
            daily_data = {}
            for item in data['list']:
                date = datetime.fromtimestamp(item['dt']).date()
                if date >= today and date <= today + timedelta(days=2):
                    if date not in daily_data:
                        daily_data[date] = []
                    daily_data[date].append(item)
            
            # Ambil data siang dan malam untuk setiap hari
            for i in range(3):
                target_date = today + timedelta(days=i)
                
                if target_date in daily_data:
                    day_data = daily_data[target_date]
                    
                    # Cari data siang (12:00-15:00) dan malam (18:00-21:00)
                    day_temp = None
                    night_temp = None
                    description = None
                    icon = None
                    
                    for item in day_data:
                        hour = datetime.fromtimestamp(item['dt']).hour
                        if 12 <= hour <= 15 and day_temp is None:
                            day_temp = item['main']['temp']
                            description = item['weather'][0]['description']
                            icon = item['weather'][0]['icon']
                        elif 18 <= hour <= 21 and night_temp is None:
                            night_temp = item['main']['temp']
                    
                    # Kalau tidak ketemu, ambil yang terdekat
                    if day_temp is None and day_data:
                        day_temp = day_data[0]['main']['temp']
                        description = day_data[0]['weather'][0]['description']
                        icon = day_data[0]['weather'][0]['icon']
                    if night_temp is None and day_data:
                        night_temp = day_data[-1]['main']['temp']
                    
                    # Nama hari dalam bahasa Indonesia
                    days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
                    day_name = days[target_date.weekday()]
                    
                    forecasts.append({
                        'date': target_date.strftime('%Y-%m-%d'),
                        'day_name': day_name,
                        'day_temp': round(day_temp) if day_temp else None,
                        'night_temp': round(night_temp) if night_temp else None,
                        'description': description or 'Tidak tersedia',
                        'icon': icon or '01d'
                    })
                else:
                    # Kalau data tidak ada, kasih placeholder
                    days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
                    day_name = days[target_date.weekday()]
                    forecasts.append({
                        'date': target_date.strftime('%Y-%m-%d'),
                        'day_name': day_name,
                        'day_temp': None,
                        'night_temp': None,
                        'description': 'Data tidak tersedia',
                        'icon': '01d'
                    })
            
            return forecasts
        else:
            return None
            
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None


def get_random_question():
    """Ambil pertanyaan random dari pool pertanyaan"""
    from app.quiz_data import QUIZ_QUESTIONS
    return random.choice(QUIZ_QUESTIONS)

