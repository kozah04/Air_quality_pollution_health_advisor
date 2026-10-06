import datetime

import requests


def format_time(time_str):
    # open-meteo gives times like "2026-09-26T00:00", this turns
    # that into something readable like "12:00 AM"
    dt = datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M')
    return dt.strftime('%I:%M %p').lstrip('0')


class AirQualityClient:
    GEOCODE_URL = 'https://geocoding-api.open-meteo.com/v1/search'
    AIR_QUALITY_URL = 'https://air-quality-api.open-meteo.com/v1/air-quality'

    def get_coordinates(self, location_name):
        params = {'name': location_name, 'count': 1}

        try:
            res = requests.get(self.GEOCODE_URL, params=params, timeout=10)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f'Could not reach geocoding service: {e}')

        data = res.json()
        results = data.get('results')

        if not results:
            raise ValueError(f"Could not find a place called '{location_name}'")

        place = results[0]
        lat = place['latitude']
        lon = place['longitude']
        name = place.get('name', location_name)

        return lat, lon, name

    def get_current_air_quality(self, latitude, longitude):
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'us_aqi,pm2_5,pm10,ozone,nitrogen_dioxide',
            'timezone': 'auto',
        }

        try:
            res = requests.get(self.AIR_QUALITY_URL, params=params, timeout=10)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f'Could not reach air quality service: {e}')

        data = res.json()
        current = data.get('current')

        if not current:
            raise ValueError('No current air quality data for this location')

        return {
            'aqi': current.get('us_aqi'),
            'pm2_5': current.get('pm2_5'),
            'pm10': current.get('pm10'),
            'ozone': current.get('ozone'),
            'nitrogen_dioxide': current.get('nitrogen_dioxide'),
        }

    def get_forecast_air_quality(self, latitude, longitude):
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'hourly': 'us_aqi,pm2_5',
            'timezone': 'auto',
            'forecast_days': 1,
        }

        try:
            res = requests.get(self.AIR_QUALITY_URL, params=params, timeout=10)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f'Could not reach forecast service: {e}')

        data = res.json()
        hourly = data.get('hourly')

        if not hourly:
            raise ValueError('No forecast data for this location')

        times = hourly.get('time', [])
        aqi_values = hourly.get('us_aqi', [])

        forecast = []
        for i in range(len(times)):
            forecast.append({
                'time': times[i],
                'aqi': aqi_values[i] if i < len(aqi_values) else None,
            })

        return forecast

    def find_cleanest_hour(self, forecast_list):
        cleanest = None
        for entry in forecast_list:
            if entry['aqi'] is None:
                continue
            if cleanest is None or entry['aqi'] < cleanest['aqi']:
                cleanest = entry
        return cleanest

    def find_cleanest_active_hour(self, forecast_list, start_hour=6, end_hour=22):
        # same idea as find_cleanest_hour, but only looks at the hours
        # when people are realistically outside (6am up to 10pm)
        cleanest = None
        for entry in forecast_list:
            if entry['aqi'] is None:
                continue

            hour = datetime.datetime.strptime(entry['time'], '%Y-%m-%dT%H:%M').hour
            if hour < start_hour or hour >= end_hour:
                continue

            if cleanest is None or entry['aqi'] < cleanest['aqi']:
                cleanest = entry
        return cleanest
