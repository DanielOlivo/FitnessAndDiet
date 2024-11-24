from datetime import datetime, timedelta
import requests
import random

def get_weekly_stats(user_id):
    # Simulating data fetch from a database
    sessions = [
        {"date": "2024-11-12", "duration": 60, "weight": 80},
        {"date": "2024-11-14", "duration": 50, "weight": 79.5},
        {"date": "2024-11-16", "duration": 70, "weight": 79},
    ]
    start_of_week = datetime.now() - timedelta(days=7)
    weekly_sessions = [s for s in sessions if datetime.strptime(s["date"], "%Y-%m-%d") >= start_of_week]

    if not weekly_sessions:
        return {"message": "No sessions recorded this week!"}

    # Calculate total weight loss
    start_weight = weekly_sessions[0]["weight"]
    end_weight = weekly_sessions[-1]["weight"]
    weight_loss = start_weight - end_weight

    return {"sessions_completed": len(weekly_sessions), "weight_loss": weight_loss}

def fetch_quote():
    response = random.choices('congratulation','Mazal Tov','Kol Hakavod', 'Molodets', 'Felicitations!')
    if response:
        print(response)
    else:
        return "Keep pushing forward! Every effort counts."

# Example Usage
user_stats = get_weekly_stats(user_id=1)
quote = fetch_quote()

print("Weekly Stats:", user_stats)
print("Motivational Quote:", quote)