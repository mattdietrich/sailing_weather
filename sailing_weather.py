import requests             # Need to install this HTTP Python library: http://requests.readthedocs.org/en/latest/
import datetime

API_KEY = "" # Request an API key from http://openweathermap.org/appid#get

# My minimum Laser sailing weather conditions
MAX_RAIN = 0            # millimetres
MAX_SNOW = 0            # millimetres
MIN_DAY_TEMP = 10       # Celsius
MIN_WIND_SPEED = 15/3.6 # metres/second
MAX_WIND_SPEED = 30/3.6 # metres/second (I don't want to die!)

def main():
    """Requests the weather forecast data and identifies the days with suitable sailing weather
    """
    
    url = "http://api.openweathermap.org/data/2.5/forecast/daily"   # Base URL 
    url += "?q=Toronto,ca"                                          # City and country
    url += "&units=metric"                                          # Unit type
    url += "&appid=" + API_KEY                                      # API key

    # print(url)

    r = requests.get(url)               # Make the API request
    r.raise_for_status()                # Raise the error response, if any
    json_resp = r.json()                # Convert response to JSON
    raw_forecasts = json_resp["list"]   # List of day forecasts (raw)

    sailing_weather = True   # Set to false if weather condition checks fail
    sailing_days = []        # Result set of good sailing days
    
    for day in raw_forecasts:
        # print (date_from_timestamp(day["dt"]))
        
        # Rain Condition Check        
        if "rain" in day and day["rain"] > MAX_RAIN:
            # print ("Too much rain")
            continue

        # Snow Condition Check 
        if "snow" in day and day["snow"] > MAX_SNOW:
            # print ("Too much snow")
            continue

        # Temperature Condition Check
        if day["temp"]["day"] < MIN_DAY_TEMP:
            # print ("Too cold")
            continue

        # Wind Speed Checks
        if day["speed"] < MIN_WIND_SPEED:
            # print ("Wind too light")
            continue
        if day["speed"] > MAX_WIND_SPEED:
            # print ("Wind too heavy")
            continue

        # Building the result set
        sailing_day = Forecast(date_from_timestamp(day["dt"]))
        sailing_day.set_main(day["weather"][0]["main"])
        sailing_day.set_temp_high(day["temp"]["max"])   # Celsius
        sailing_day.set_temp_low(day["temp"]["min"])    # Celsius
        sailing_day.set_temp_day(day["temp"]["day"])    # Celsius
        sailing_day.set_wind_speed(day["speed"]*3.6)    # Convert to km/h
        sailing_day.set_wind_deg(day["deg"])        
        sailing_day.set_wind_direction(deg_to_direction(sailing_day.get_wind_deg()))
        if "rain" in day:
            sailing_day.set_rain(day["rain"]) # millimetres
        if "snow" in day:
            sailing_day.set_snow(day["snow"]) # millimetres
        sailing_days.append(sailing_day)

    # Printing a result message
    if len(sailing_days) is 0:
        print ("There are no good sailing days coming up.\nBummer!")
    elif len(sailing_days) is 1:
        print ("There's 1 good sailing day coming up!\nHere's the forecast:\n")
    else:
        print ("There are " + str(len(sailing_days)) + " good sailing days coming up!\nHere are the forecasts:\n")
    # Printing the results
    for sd in sailing_days:
        sd.print()
        print()

class Forecast:
    """Represents the weather forecast for a particular day
    """
    def __init__(self, date):
        self.date = date
        self.main = None
        self.temp_high = None
        self.temp_low = None
        self.temp_day = None
        self.wind_speed = None
        self.wind_direction = None
        self.wind_deg = None
        self.rain = None
        self.snow = None

    def print(self):
        """Print the forecast in a readable way
        """
        print (self.date.strftime("%A %B %d, %Y"))
        print (self.main)
        print ("Temperature: High = " + str(round(self.temp_high)) + " C, Low = " + str(round(self.temp_low)) + " C")
        print ("Wind: " + str(round(self.wind_speed)) + " km/h " + self.wind_direction)
        if self.rain:
            print ("Rain: " + str(round(self.rain)) + " mm")
        if self.snow:
            print ("Snow: " + str(round(self.snow)) + " mm")

    # Setters
    def set_date(self, main):
        self.date = date
    def set_main(self, main):
        self.main = main
    def set_temp_high(self, temp_high):
        self.temp_high = temp_high
    def set_temp_low(self, temp_low):
        self.temp_low = temp_low
    def set_temp_day(self, temp_day):
        self.temp_day = temp_day
    def set_wind_speed(self, wind_speed):
        self.wind_speed = wind_speed
    def set_wind_direction(self, wind_direction):
        self.wind_direction = wind_direction
    def set_wind_deg(self, wind_deg):
        self.wind_deg = wind_deg
    def set_rain(self, rain):
        self.rain = rain
    def set_snow(self, snow):
        self.snow = snow

    # Getters
    def get_date(self):
        return self.date
    def get_main(self):
        return self.main
    def get_temp_high(self):
        return self.temp_high
    def get_temp_low(self):
        return self.temp_low
    def get_temp_day(self):
        return self.temp_day
    def get_wind_speed(self):
        return self.wind_speed
    def get_wind_direction(self):
        return self.wind_direction
    def get_wind_deg(self):
        return self.wind_deg
    def get_rain(self):
        return self.rain
    def get_snow(self):
        return self.snow

def deg_to_direction(deg):
    """Convert degrees to cardinal direction
    """
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW", "N"]
    return directions[round(deg%360/22.5)]
    

def date_from_timestamp(tstamp):
    """Convert the integer timestamp to datetime
    """
    return datetime.datetime.utcfromtimestamp(tstamp)

if __name__ == "__main__": main()
