"""Generate weather data files with 5-minute interval readings for each day."""
import json
import random
from datetime import datetime, timedelta, timezone

BRISBANE_TZ = timezone(timedelta(hours=10))

LOCATION = {
    "city": "Brisbane",
    "state": "Queensland",
    "country": "Australia",
    "coordinates": {
        "latitude": -27.4698,
        "longitude": 153.0251
    }
}

# Base daily profiles for Brisbane in April (early autumn)
# (hour -> base_temp, base_humidity, base_wind_kph)
HOURLY_PROFILE = {
    7:  (18, 75, 8),
    8:  (19, 72, 9),
    9:  (21, 68, 10),
    10: (23, 62, 12),
    11: (25, 58, 13),
    12: (27, 54, 14),
    13: (28, 52, 14),
    14: (28, 50, 15),
    15: (27, 52, 14),
    16: (26, 55, 12),
    17: (24, 60, 10),
}

WEATHER_CONDITIONS = ["clear", "partly_cloudy", "overcast", "light_rain"]
WEATHER_WEIGHTS_NORMAL = [40, 35, 20, 5]
WIND_DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


def interpolate_base(hour, minute):
    """Interpolate base values between whole hours."""
    h1 = max(7, min(17, hour))
    h2 = min(17, h1 + 1)
    t = minute / 60.0
    t1, hum1, w1 = HOURLY_PROFILE[h1]
    t2, hum2, w2 = HOURLY_PROFILE.get(h2, HOURLY_PROFILE[h1])
    temp = t1 + (t2 - t1) * t
    hum = hum1 + (hum2 - hum1) * t
    wind = w1 + (w2 - w1) * t
    return temp, hum, wind


def light_level(hour):
    if hour < 8:
        return "dawn"
    elif hour < 10:
        return "morning"
    elif hour < 14:
        return "midday"
    elif hour < 17:
        return "afternoon"
    else:
        return "evening"


def generate_weather_day(year, month, day, day_seed):
    """Generate weather readings every 5 minutes from 07:00 to 18:00."""
    random.seed(day_seed)

    # Pick a daily weather tendency
    # Some days are rainy, most are fine
    if random.random() < 0.15:
        day_conditions = ["overcast", "light_rain", "overcast", "partly_cloudy"]
        temp_offset = random.uniform(-3, -1)
        hum_offset = random.uniform(10, 20)
    elif random.random() < 0.3:
        day_conditions = ["partly_cloudy", "overcast", "partly_cloudy"]
        temp_offset = random.uniform(-2, 0)
        hum_offset = random.uniform(5, 10)
    else:
        day_conditions = ["clear", "partly_cloudy", "clear"]
        temp_offset = random.uniform(-1, 2)
        hum_offset = random.uniform(-5, 5)

    # Day-to-day variation
    daily_temp_shift = temp_offset
    daily_hum_shift = hum_offset
    wind_dir = random.choice(WIND_DIRECTIONS)

    readings = []
    current = datetime(year, month, day, 7, 0, 0, tzinfo=BRISBANE_TZ)
    end = datetime(year, month, day, 18, 0, 0, tzinfo=BRISBANE_TZ)

    while current <= end:
        hour = current.hour
        minute = current.minute
        base_temp, base_hum, base_wind = interpolate_base(hour, minute)

        temp = round(base_temp + daily_temp_shift + random.uniform(-0.5, 0.5), 1)
        humidity = max(30, min(95, int(base_hum + daily_hum_shift + random.uniform(-3, 3))))
        wind_speed = round(max(0, base_wind + random.uniform(-3, 3)), 1)
        uv_index = round(max(0, {7: 1, 8: 2, 9: 4, 10: 6, 11: 8, 12: 9, 13: 9, 14: 8, 15: 6, 16: 4, 17: 2}.get(hour, 1) + random.uniform(-0.5, 0.5)), 1)

        # Weather shifts slowly through the day
        condition_idx = int((hour - 7) / 11 * len(day_conditions))
        condition_idx = min(condition_idx, len(day_conditions) - 1)
        weather = day_conditions[condition_idx]
        # Small chance of brief change
        if random.random() < 0.05:
            weather = random.choice(["partly_cloudy", "clear", "overcast"])

        pressure = round(1013 + random.uniform(-5, 5), 1)

        ts_str = current.strftime("%Y-%m-%dT%H:%M:%S") + "+10:00"

        reading = {
            "timestamp": ts_str,
            "location": LOCATION,
            "temperature_celsius": temp,
            "humidity_percent": humidity,
            "pressure_hpa": pressure,
            "wind": {
                "speed_kph": wind_speed,
                "direction": wind_dir
            },
            "uv_index": uv_index,
            "light_level": light_level(hour),
            "weather": weather
        }
        readings.append(reading)
        current += timedelta(minutes=5)

    return readings


def generate_null_weather_day(year, month, day):
    """Generate weather readings with null values to simulate device failure."""
    readings = []
    current = datetime(year, month, day, 7, 0, 0, tzinfo=BRISBANE_TZ)
    end = datetime(year, month, day, 18, 0, 0, tzinfo=BRISBANE_TZ)

    while current <= end:
        ts_str = current.strftime("%Y-%m-%dT%H:%M:%S") + "+10:00"
        reading = {
            "timestamp": ts_str,
            "location": LOCATION,
            "temperature_celsius": None,
            "humidity_percent": None,
            "pressure_hpa": None,
            "wind": {
                "speed_kph": None,
                "direction": None
            },
            "uv_index": None,
            "light_level": None,
            "weather": None
        }
        readings.append(reading)
        current += timedelta(minutes=5)

    return readings


if __name__ == "__main__":
    import os
    os.makedirs("weather", exist_ok=True)

    for day in range(1, 19):
        if day == 17:
            # Simulate device failure on April 17
            readings = generate_null_weather_day(2026, 4, day)
        else:
            readings = generate_weather_day(2026, 4, day, day_seed=1000 + day)

        date_str = f"2026{4:02d}{day:02d}"
        outfile = f"weather/weather_{date_str}.json"
        with open(outfile, "w") as f:
            json.dump(readings, f, indent=2)
        if day == 17:
            print(f"{outfile}: {len(readings)} readings (device failure - all null)")
        else:
            temps = [r["temperature_celsius"] for r in readings]
            print(f"{outfile}: {len(readings)} readings, temp {min(temps)}-{max(temps)}C")
