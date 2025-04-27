# sensors.py
from datetime import datetime
import random

def generate_sensor_data():
    return {
        "timestamp": datetime.now().isoformat(),
        "galvanic_skin_response": round(random.uniform(1.0, 10.0), 2),
        "air_quality": {"VOC": random.randint(100, 500), "CO2": random.randint(350, 1000)},
        "uv_exposure": random.randint(0, 11),
        "body_impedance": random.randint(300, 700),
        "emg_activity": [round(random.uniform(0.1, 5.0), 1) for _ in range(3)],
        "ecg_waveform": [round(random.uniform(-1.0, 1.0), 1) for _ in range(3)],
        "magnetometer": {"x": round(random.uniform(-50, 50), 1), "y": round(random.uniform(-50, 50), 1), "z": round(random.uniform(-50, 50), 1)},
        "gyroscope": {"x": round(random.uniform(-1, 1), 1), "y": round(random.uniform(-1, 1), 1), "z": round(random.uniform(-1, 1), 1)},
        "accelerometer": {"x": round(random.uniform(-1, 1), 2), "y": round(random.uniform(-1, 1), 2), "z": round(random.uniform(-1, 1), 2)},
        "basal_body_temp": round(random.uniform(35, 38), 1),
        "urea_level": round(random.uniform(15, 45), 1),
        "alcohol_level": round(random.uniform(0, 0.08), 4),
        "total_proteins": round(random.uniform(6.0, 8.5), 1),
        "lactate_level": round(random.uniform(0.5, 2.5), 1),
        "ketone_bodies": round(random.uniform(0.0, 3.0), 1),
        "glucose_level": round(random.uniform(70, 140), 1),
        "electrodermal_activity": round(random.uniform(1.0, 10.0), 2),
        "skin_conductance": round(random.uniform(1.0, 10.0), 2),
        "blood_oxygen_saturation": round(random.uniform(90, 100), 1),
        "blood_pressure": {"systolic": random.randint(110, 130), "diastolic": random.randint(70, 90)},
        "skin_temperature": round(random.uniform(30, 36), 1),
        "heart_rate": random.randint(50, 100)
    }

historical_sensor_data = [generate_sensor_data() for _ in range(1440)]
