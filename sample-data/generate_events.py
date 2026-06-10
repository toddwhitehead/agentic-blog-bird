"""One-off script to generate sample bird detection events across a full day."""
import json
import random
import uuid
from datetime import datetime, timedelta, timezone

BRISBANE_TZ = timezone(timedelta(hours=10))
DATE = "2026-04-18"
START_HOUR = 7
END_HOUR = 18  # 6pm

CAMERAS = ["backyard_cam_01", "backyard_cam_02", "front_yard_cam_01"]

SPECIES = [
    {
        "species": "Sulphur-crested Cockatoo",
        "common_name": "Sulphur-crested Cockatoo",
        "scientific_name": "Cacatua galerita",
        "weight": 45,
    },
    {
        "species": "Noisy Miner",
        "common_name": "Noisy Miner",
        "scientific_name": "Manorina melanocephala",
        "weight": 30,
    },
    {
        "species": "Rainbow Lorikeet",
        "common_name": "Rainbow Lorikeet",
        "scientific_name": "Trichoglossus moluccanus",
        "weight": 15,
    },
    {
        "species": "Australian King-Parrot",
        "common_name": "Australian King-Parrot",
        "scientific_name": "Alisterus scapularis",
        "weight": 7,
    },
    {
        "species": "Pale-headed Rosella",
        "common_name": "Pale-headed Rosella",
        "scientific_name": "Platycercus adscitus",
        "weight": 3,
    },
]

SPECIES_POOL = []
for s in SPECIES:
    SPECIES_POOL.extend([s] * s["weight"])

WEATHER_OPTIONS = ["clear", "partly_cloudy", "overcast"]

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

def temp_for_hour(hour):
    """Rough Brisbane April temperature curve."""
    base = {7: 18, 8: 19, 9: 21, 10: 23, 11: 25, 12: 27, 13: 28, 14: 28, 15: 27, 16: 26, 17: 24}
    base_temp = base.get(hour, 22)
    return round(base_temp + random.uniform(-2, 2), 1)

def random_bbox():
    x_min = random.randint(50, 1600)
    y_min = random.randint(50, 850)
    w = random.randint(70, 220)
    h = random.randint(60, 200)
    return {
        "x_min": x_min,
        "y_min": y_min,
        "x_max": x_min + w,
        "y_max": y_min + h,
        "width": w,
        "height": h,
    }

def generate_events(year=2026, month=4, day=18):
    events = []
    # Generate events with variable gaps (3-20 min apart, clusters during active times)
    current = datetime(year, month, day, 7, 0, 0, tzinfo=BRISBANE_TZ)
    end = datetime(year, month, day, 18, 0, 0, tzinfo=BRISBANE_TZ)

    while current < end:
        hour = current.hour
        # More detections in morning (7-10) and late afternoon (15-18), fewer midday
        if 7 <= hour < 10 or 15 <= hour < 18:
            gap_minutes = random.uniform(2, 10)
            # Sometimes a burst of detections (flock)
            if random.random() < 0.2:
                burst = random.randint(2, 5)
                for i in range(burst):
                    ts = current + timedelta(seconds=random.randint(0, 30))
                    events.append(make_event(ts))
        else:
            gap_minutes = random.uniform(8, 25)

        events.append(make_event(current))
        current += timedelta(minutes=gap_minutes)

    # Sort by timestamp
    events.sort(key=lambda e: e["data"]["timestamp"])
    return events

def make_event(ts):
    bird = random.choice(SPECIES_POOL)
    ts_str = ts.strftime("%Y-%m-%dT%H:%M:%S.") + f"{random.randint(100000,999999):06d}+10:00"
    ts_compact = ts.strftime("%Y%m%d_%H%M%S")
    evt_id = f"evt_{uuid.uuid4().hex[:8]}_{ts_compact}"
    camera = random.choice(CAMERAS)
    hour = ts.hour
    weather = random.choice(WEATHER_OPTIONS)
    utc_ts = (ts - timedelta(hours=10)).strftime("%Y-%m-%dT%H:%M:%S.") + f"{random.randint(100000,999999):06d}+00:00"

    return {
        "topic": "bird/detection",
        "data": {
            "event_id": evt_id,
            "timestamp": ts_str,
            "camera_id": camera,
            "location": {
                "city": "Brisbane",
                "state": "Queensland",
                "country": "Australia",
                "coordinates": {
                    "latitude": -27.4698,
                    "longitude": 153.0251,
                },
                "zone": "front_yard" if "front" in camera else "backyard",
            },
            "detection": {
                "object_type": "bird",
                "species": bird["species"],
                "common_name": bird["common_name"],
                "scientific_name": bird["scientific_name"],
                "confidence": round(random.uniform(0.45, 0.95), 2),
                "bounding_box": random_bbox(),
                "image_dimensions": {"width": 1920, "height": 1080},
            },
            "environmental_data": {
                "temperature_celsius": temp_for_hour(hour),
                "humidity_percent": random.randint(40, 85),
                "light_level": light_level(hour),
                "weather": weather,
            },
            "ai_model": {
                "name": "bird_classifier_v2.1",
                "version": "2.1.0",
                "provider": "acme-ai",
            },
        },
        "received_at": utc_ts,
        "processed_by": "mqtt-proxy",
    }

if __name__ == "__main__":
    from collections import Counter

    for day in range(1, 18):
        random.seed(42 + day)  # different but reproducible seed per day
        events = generate_events(2026, 4, day)
        date_str = f"2026{4:02d}{day:02d}"
        outfile = f"events_{date_str}_070000.json"
        with open(outfile, "w") as f:
            json.dump(events, f, indent=2)
        species_counts = Counter(e["data"]["detection"]["species"] for e in events)
        print(f"{outfile}: {len(events)} events  ", end="")
        print(", ".join(f"{s}: {c}" for s, c in species_counts.most_common()))
