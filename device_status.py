import random
from datetime import datetime

def generate_device_status():
    return {
        "timestamp": datetime.now().isoformat(),
        "on_wrist": True,
        "battery_level": 85,
        "charging": False,
        "signal_strength": -70,
        "device_health": "OK",
        "last_sync_time": datetime.now().isoformat()
    }

historical_device_status = [generate_device_status() for _ in range(1440)]
