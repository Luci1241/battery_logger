import csv
import time
import os
from datetime import datetime

try:
    import psutil
except ImportError:
    print("Install psutil first: pip install psutil")
    input("Press Enter to close...")
    exit(1)

LOG_FILE = "battery_log.csv"
INTERVAL_MINUTES = 15

def log_battery():
    # Display full path of log file
    full_path = os.path.abspath(LOG_FILE)
    print(f"Log file location: {full_path}")
    print("-" * 50)
    
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header if file is empty
        if file.tell() == 0:
            writer.writerow(["timestamp", "percentage", "plugged_in", "time_left_mins"])
        
        while True:
            battery = psutil.sensors_battery()
            
            if battery is None:
                print("No battery detected!")
                input("Press Enter to close...")
                break
            
            time_left = battery.secsleft // 60 if battery.secsleft > 0 else "N/A"
            
            row = [
                datetime.now().isoformat(),
                battery.percent,
                battery.power_plugged,
                time_left
            ]
            
            writer.writerow(row)
            file.flush()
            
            print(f"[{row[0]}] Battery: {row[1]}% | Plugged: {row[2]} | Time left: {row[3]} mins")
            
            # Stop if critically low (optional safety)
            if battery.percent <= 5 and not battery.power_plugged:
                print("Battery critically low! Stopping.")
                input("Press Enter to close...")
                break
            
            time.sleep(INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    try:
        log_battery()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to close...")
