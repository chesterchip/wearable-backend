import random
from datetime import datetime, timedelta

initial_drink_time = datetime.utcnow() - timedelta(hours=7)
initial_BAC = 0.16  # initial heavy drinking BAC peak

sensor_state = {
    "glucose_mg_dL": 92,
    "lactate_mmol_L": 1.1,
    "ketones_mmol_L": 0.2,
    "proteins_g_dL": 7.1,
    "urea_mg_dL": 15,
    "heart_rate_BPM": 72,
    "skin_temp_C": 34.7,
    "ambient_temp_C": 22.0,
    "humidity_pct": 40,
    "pressure_hPa": 1013,
    "GSR_uS": 3.5,
}

historical_data = []

def random_walk(value, min_val, max_val, step):
    return max(min_val, min(max_val, value + random.uniform(-step, step)))

def current_BAC():
    elapsed_hours = (datetime.utcnow() - initial_drink_time).total_seconds() / 3600
    metabolized_BAC = elapsed_hours * 0.015  # standard metabolism rate
    return max(0, initial_BAC - metabolized_BAC)

def generate_sensor_data(timestamp=None):
    if not timestamp:
        timestamp = datetime.utcnow().isoformat() + "Z"

    bac_now = current_BAC()

    # Simulate realistic glucose recovery from alcohol-induced low
    glucose_base = 95 if bac_now < 0.05 else 85  # glucose recovery post-alcohol
    sensor_state["glucose_mg_dL"] = random_walk(glucose_base, 80, 110, 1.0)

    sensor_state["lactate_mmol_L"] = random_walk(sensor_state["lactate_mmol_L"], 0.7, 1.5, 0.05)
    sensor_state["ketones_mmol_L"] = random_walk(sensor_state["ketones_mmol_L"], 0.1, 0.3, 0.01)
    sensor_state["proteins_g_dL"] = random_walk(sensor_state["proteins_g_dL"], 6.8, 7.3, 0.01)
    sensor_state["urea_mg_dL"] = random_walk(sensor_state["urea_mg_dL"], 13, 17, 0.1)

    # Heart rate gradually returns to normal after elevated drinking period
    heart_rate_base = 68 if bac_now < 0.05 else 75
    sensor_state["heart_rate_BPM"] = random_walk(heart_rate_base, 60, 80, 1.0)

    sensor_state["skin_temp_C"] = random_walk(sensor_state["skin_temp_C"], 33.8, 35.0, 0.05)

    # Environmental stable minor variations
    sensor_state["ambient_temp_C"] = random_walk(sensor_state["ambient_temp_C"], 20, 24, 0.05)
    sensor_state["humidity_pct"] = random_walk(sensor_state["humidity_pct"], 35, 45, 0.2)
    sensor_state["pressure_hPa"] = random_walk(sensor_state["pressure_hPa"], 1008, 1018, 0.1)
    
    # GSR slowly normalizing
    gsr_base = 3.0 if bac_now < 0.05 else 4.0
    sensor_state["GSR_uS"] = random_walk(gsr_base, 2.5, 4.5, 0.05)

    data = {
        "timestamp": timestamp,
        "biochemical": {
            "glucose_mg_dL": round(sensor_state["glucose_mg_dL"], 1),
            "lactate_mmol_L": round(sensor_state["lactate_mmol_L"], 2),
            "ketones_mmol_L": round(sensor_state["ketones_mmol_L"], 2),
            "proteins_g_dL": round(sensor_state["proteins_g_dL"], 2),
            "alcohol_BAC_pct": round(bac_now, 4),
            "urea_mg_dL": round(sensor_state["urea_mg_dL"], 1),
        },
        "physiological": {
            "heart_rate_BPM": round(sensor_state["heart_rate_BPM"], 1),
            "skin_temp_C": round(sensor_state["skin_temp_C"], 2),
        },
        "environmental": {
            "ambient_temp_C": round(sensor_state["ambient_temp_C"], 2),
            "humidity_pct": round(sensor_state["humidity_pct"], 1),
            "pressure_hPa": round(sensor_state["pressure_hPa"], 1),
            "GSR_uS": round(sensor_state["GSR_uS"], 2),
        }
    }

    return data

def generate_historical_data():
    historical_data.clear()
    time_point = datetime.utcnow() - timedelta(hours=24)
    for _ in range(17280):  # 24 hours data, every 5 seconds
        historical_data.append(generate_sensor_data(time_point.isoformat() + "Z"))
        time_point += timedelta(seconds=5)

generate_historical_data()
