import datetime


class AirReading:
    # holds the data for one air quality check

    def __init__(self, location, latitude, longitude, aqi, pm2_5, pm10,
                 ozone, nitrogen_dioxide, timestamp=None):
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.aqi = aqi
        self.pm2_5 = pm2_5
        self.pm10 = pm10
        self.ozone = ozone
        self.nitrogen_dioxide = nitrogen_dioxide

        if timestamp is None:
            self.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.timestamp = timestamp

    def to_dict(self):
        # convert to a dict so we can dump it into json
        return {
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'aqi': self.aqi,
            'pm2_5': self.pm2_5,
            'pm10': self.pm10,
            'ozone': self.ozone,
            'nitrogen_dioxide': self.nitrogen_dioxide,
            'timestamp': self.timestamp,
        }

    @staticmethod
    def from_dict(data):
        return AirReading(
            location=data.get('location'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            aqi=data.get('aqi'),
            pm2_5=data.get('pm2_5'),
            pm10=data.get('pm10'),
            ozone=data.get('ozone'),
            nitrogen_dioxide=data.get('nitrogen_dioxide'),
            timestamp=data.get('timestamp'),
        )

    def __str__(self):
        return f"{self.location} at {self.timestamp} - AQI: {self.aqi}"
