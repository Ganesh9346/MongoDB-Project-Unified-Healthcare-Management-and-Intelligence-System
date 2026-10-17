from config.database import follow_ups_collection, patients_collection
from pymongo.errors import DuplicateKeyError
from datetime import datetime


def schedule_follow_up():
    print("\n--- Schedule Patient Follow-Up ---")

    follow_up_id = input("Enter Follow-Up ID: ").strip()
    patient_id = input("Enter Patient ID: ").strip()
    follow_up_date = input("Enter Follow-Up Date (YYYY-MM-DD): ").strip()
    reason = input("Enter Follow-Up Reason: ").strip()

    if not all([follow_up_id, patient_id, follow_up_date, reason]):
        print("All fields are required.")
        return

    try:
        follow_up_date = datetime.strptime(
            follow_up_date, "%Y-%m-%d"
        )

        if follow_up_date.date() < datetime.now().date():
            print("Follow-up date cannot be in the past.")
            return

    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    patient = patients_collection.find_one(
        {"patient_id": patient_id}
    )

    if not patient:
        print("Patient not found. Register the patient first.")
        return

    follow_up = {
        "follow_up_id": follow_up_id,
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "follow_up_date": follow_up_date,
        "reason": reason,
        "status": "Scheduled",
        "created_at": datetime.now()
    }

    try:
        follow_ups_collection.insert_one(follow_up)
        print("Follow-up scheduled successfully!")

    except DuplicateKeyError:
        print("This Follow-Up ID already exists.")


def view_all_follow_ups():
    print("\n--- All Patient Follow-Ups ---")

    follow_ups = follow_ups_collection.find().sort(
        "follow_up_date", 1
    )

    count = 0

    for item in follow_ups:
        count += 1
        print(
            f"Follow-Up ID: {item['follow_up_id']} | "
            f"Patient: {item['patient_name']} | "
            f"Patient ID: {item['patient_id']} | "
            f"Date: {item['follow_up_date'].strftime('%Y-%m-%d')} | "
            f"Reason: {item['reason']} | "
            f"Status: {item['status']}"
        )

    if count == 0:
        print("No follow-ups found.")


def search_follow_ups_by_patient():
    print("\n--- Search Follow-Ups by Patient ---")

    patient_id = input("Enter Patient ID: ").strip()

    follow_ups = follow_ups_collection.find(
        {"patient_id": patient_id}
    ).sort("follow_up_date", 1)

    count = 0

    for item in follow_ups:
        count += 1
        print(
            f"Follow-Up ID: {item['follow_up_id']} | "
            f"Date: {item['follow_up_date'].strftime('%Y-%m-%d')} | "
            f"Reason: {item['reason']} | "
            f"Status: {item['status']}"
        )

    if count == 0:
        print("No follow-ups found for this patient.")


def update_follow_up_status():
    print("\n--- Update Follow-Up Status ---")

    follow_up_id = input("Enter Follow-Up ID: ").strip()

    follow_up = follow_ups_collection.find_one(
        {"follow_up_id": follow_up_id}
    )

    if not follow_up:
        print("Follow-up not found.")
        return

    print("1. Scheduled")
    print("2. Completed")
    print("3. Cancelled")
    print("4. Missed")

    choice = input("Select new status: ").strip()

    statuses = {
        "1": "Scheduled",
        "2": "Completed",
        "3": "Cancelled",
        "4": "Missed"
    }

    if choice not in statuses:
        print("Invalid choice.")
        return

    follow_ups_collection.update_one(
        {"follow_up_id": follow_up_id},
        {"$set": {"status": statuses[choice]}}
    )

    print("Follow-up status updated successfully!")