from location_services import get_geolocation, find_nearby_studios
from reminders import create_event
from statistics import get_weekly_stats, fetch_quote

def main():
    # Step 1: Collect User Data
    address = input("Enter your address: ")
    lat, lng = get_geolocation(address)
    print("Your location:", lat, lng)

    # Step 2: Find Nearby Studios
    studios = find_nearby_studios(lat, lng)
    print("Nearby Studios:")
    for studio in studios:
        print(f"{studio['name']} - {studio['address']}")

    # Step 3: Set Reminders
    print("Setting a training reminder.")
    summary = input("Enter the name of the training session: ")
    start_time = input("Enter start time (YYYY-MM-DDTHH:MM:SS): ")
    end_time = input("Enter end time (YYYY-MM-DDTHH:MM:SS): ")
    create_event(summary, start_time, end_time)
    print("Reminder set!")

    # Step 4: Weekly Statistics
    print("Calculating your weekly stats...")
    stats = get_weekly_stats()
    print(f"Sessions Completed: {stats['sessions_completed']}")
    print(f"Weight Loss: {stats['weight_loss']} kg")

    # Step 5: Motivation
    if stats['weight_loss'] > 0:
        print("Congratulations on your progress!")
        print("Motivational Quote:", fetch_quote())

if __name__ == "__main__":
    main()
