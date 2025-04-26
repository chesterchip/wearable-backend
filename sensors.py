# sensors.py
import random
from datetime import datetime

def generate_sensor_data():
    return {
        "timestamp": datetime.now().isoformat(),
        "glucose": round(random.uniform(70, 140), 2),
        "lactate": round(random.uniform(0.5, 2.5), 2),
        "ketones": round(random.uniform(0.0, 3.0), 2),
        "proteins": round(random.uniform(6.0, 8.5), 2),
        "alcohol": round(random.uniform(0.0, 0.08), 4),
        "urea": round(random.uniform(15, 45), 2),
        "heart_rate": random.randint(50, 100),
        "skin_temperature": round(random.uniform(30, 36), 2)
    }

historical_data = [generate_sensor_data() for _ in range(1440)]
