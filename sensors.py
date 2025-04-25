import random
from datetime import datetime

def generate_sensor_data(event=None):
    timestamp = datetime.utcnow().isoformat() + 'Z'

    # Baseline ranges for sensors
    data = {
        "timestamp": timestamp,
        "biochemical": {
            "glucose_mg_dL": random.uniform(80, 120),
            "lactate_mmol_L": random.uniform(0.5, 2),
            "ketones_mmol_L": random.uniform(0.1, 0.3),
            "proteins_g_dL": random.uniform(6.5, 7.5),
            "alcohol_BAC_pct": 0.00,
            "urea_mg_dL": random.uniform(10, 18)
        },
        "physiological": {
            "heart_rate_BPM": random.uniform(55, 75),
            "skin_temp_C": random.uniform(33.5, 35.5)
        },
        "environmental": {
            "accelerometer": {
                "x_g": random.uniform(-0.02, 0.02),
                "y_g": random.uniform(-0.02, 0.02),
                "z_g": random.uniform(0.95, 1.02)
            },
            "gyroscope": {
                "x_deg_s": random.uniform(-0.1, 0.1),
                "y_deg_s": random.uniform(-0.1, 0.1),
                "z_deg_s": random.uniform(-0.1, 0.1)
            },
            "ambient_temp_C": random.uniform(20, 24),
            "humidity_pct": random.uniform(30, 50),
            "pressure_hPa": random.uniform(1005, 1020),
            "GSR_uS": random.uniform(1, 5)
        },
        "events": []
    }

    # Adjust sensor data based on simulated event
    if event == "sugary_food":
        data["biochemical"]["glucose_mg_dL"] += random.uniform(50, 100)
        data["physiological"]["heart_rate_BPM"] += random.uniform(5, 10)
        data["events"].append("Sugary food intake")

    elif event == "exercise":
        data["biochemical"]["lactate_mmol_L"] += random.uniform(5, 15)
        data["physiological"]["heart_rate_BPM"] += random.uniform(50, 90)
        data["biochemical"]["glucose_mg_dL"] -= random.uniform(10, 30)
        data["environmental"]["accelerometer"]["x_g"] += random.uniform(-0.3, 0.3)
        data["environmental"]["accelerometer"]["y_g"] += random.uniform(-0.3, 0.3)
        data["environmental"]["accelerometer"]["z_g"] += random.uniform(0.3, 1.5)
        data["events"].append("Exercise")

    elif event == "alcohol":
        data["biochemical"]["alcohol_BAC_pct"] += random.uniform(0.02, 0.08)
        data["physiological"]["heart_rate_BPM"] += random.uniform(5, 10)
        data["environmental"]["GSR_uS"] += random.uniform(0.5, 2)
        data["events"].append("Alcohol intake")

    # Add more events similarly if desired

    return data