import time
import json
import os
from datetime import datetime

usage_data = {}
current_date = datetime.now().strftime('%Y-%m-%d')  # Current date format

def get_current_app():
    """Fetch the currently active app."""
    try:
        active_app = os.popen('''/usr/bin/osascript -e 'tell application "System Events" to get name of first process whose frontmost is true' ''').read().strip()
        return active_app
    except Exception as e:
        print(f"Error fetching active app: {e}")
        return None

def reset_usage_data():
    """Reset usage data at midnight."""
    global usage_data
    usage_data = {}  # Clear usage data for new day
    with open("usage_stats.json", "w") as f:
        json.dump(usage_data, f)

def collect_usage_data():
    global usage_data, current_date
    midnight_timestamp = time.mktime(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timetuple())

    while True:
        now = time.time()
        app_name = get_current_app()

        # Check if it's a new day
        new_date = datetime.now().strftime('%Y-%m-%d')
        if new_date != current_date:
            reset_usage_data()
            current_date = new_date  # Update current date

        if app_name:
            if app_name not in usage_data:
                usage_data[app_name] = 0
            usage_data[app_name] += 1  # Increment usage by 1 second

        # Write data to JSON every minute (60 seconds)
        if int(now) % 60 == 0:
            with open("usage_stats.json", "w") as f:
                json.dump(usage_data, f)

        time.sleep(1)

if __name__ == "__main__":
    collect_usage_data()
