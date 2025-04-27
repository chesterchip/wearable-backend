from datetime import datetime, timedelta

daily_events = [
    {
        "type": "sleep",
        "start_time": "2025-04-26T23:00:00",
        "end_time": "2025-04-27T07:00:00",
        "details": {}
    },
    {
        "type": "meal",
        "start_time": "2025-04-27T07:30:00",
        "end_time": "2025-04-27T07:45:00",
        "details": {
            "description": "Breakfast - eggs, avocado toast, coffee",
            "nutrients": {"protein_g": 20, "carbs_g": 25, "fat_g": 15, "caffeine_mg": 80}
        }
    },
    {
        "type": "exercise",
        "start_time": "2025-04-27T09:00:00",
        "end_time": "2025-04-27T10:00:00",
        "details": {
            "activity": "Running",
            "intensity": "Moderate",
            "calories_burned": 500
        }
    },
    {
        "type": "meal",
        "start_time": "2025-04-27T12:30:00",
        "end_time": "2025-04-27T13:00:00",
        "details": {
            "description": "Lunch - chicken salad, water",
            "nutrients": {"protein_g": 35, "carbs_g": 10, "fat_g": 8, "caffeine_mg": 0}
        }
    },
    {
        "type": "hydration",
        "time": "2025-04-27T15:00:00",
        "details": {"volume_ml": 300}
    },
    {
        "type": "meal",
        "start_time": "2025-04-27T19:00:00",
        "end_time": "2025-04-27T19:30:00",
        "details": {
            "description": "Dinner - salmon, quinoa, vegetables",
            "nutrients": {"protein_g": 40, "carbs_g": 30, "fat_g": 20, "caffeine_mg": 0}
        }
    }
]
