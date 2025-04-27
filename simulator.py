from datetime import datetime, timedelta
from events import daily_events

class HumanSimulator:
    def __init__(self, events):
        self.events = sorted(events, key=lambda x: x.get("start_time", x.get("time")))
    
    def get_current_event(self, current_time):
        for event in self.events:
            start = datetime.fromisoformat(event.get("start_time", event.get("time")))
            end = datetime.fromisoformat(event.get("end_time", event.get("time")))
            if start <= current_time <= end:
                return event
        return None

    def simulate_sensor_data(self, current_time):
        event = self.get_current_event(current_time)

        # Base resting values
        heart_rate = 65
        glucose_level = 85

        # Adjustments based on event type
        if event:
            if event["type"] == "sleep":
                heart_rate -= 10
            elif event["type"] == "exercise":
                heart_rate += 40
                glucose_level -= 20
            elif event["type"] == "meal":
                glucose_level += event["details"]["nutrients"]["carbs_g"] * 0.5  # simplified glucose impact

        data = {
            "timestamp": current_time.isoformat(),
            "heart_rate": heart_rate,
            "glucose_level": glucose_level,
            # additional sensor simulations here...
        }

        return data
