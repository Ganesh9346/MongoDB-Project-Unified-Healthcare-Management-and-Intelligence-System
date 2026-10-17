from config.database import emergency_visits_collection, patients_collection
from pymongo.errors import DuplicateKeyError
from datetime import datetime


def register_emergency_visit():
    print("\n--- Register Emergency Visit ---")

    emergency_id = input("Enter Emergency ID: ").strip()
    patient_id = input("Enter Patient ID: ").strip()
    symptoms = input("Enter Symptoms: ").strip()
    priority = input("Enter Priority (Low/Medium/High/Critical): ").strip().title()

    if not all([emergency_id, patient_id, symptoms, priority]):
        print("All fields are required.")
        return

    if priority not in ["Low", "Medium", "High", "Critical"]:
        print("Invalid priority.")
        return

    patient = patients_collection.find_one({"patient_id": patient_id})

    if not patient:
        print("Patient not found. Register the patient first.")
        return

    emergency = {
        "emergency_id": emergency_id,
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "symptoms": symptoms,
        "priority": priority,
        "status": "Under Treatment",
        "visit_time": datetime.now(),
        "discharge_time": None
    }

    try:
        emergency_visits_collection.insert_one(emergency)
        print("Emergency visit registered successfully!")
    except DuplicateKeyError:
        print("This Emergency ID already exists.")


def view_all_emergency_visits():
    print("\n--- All Emergency Visits ---")

    visits = emergency_visits_collection.find().sort("visit_time", -1)
    count = 0

    for visit in visits:
        count += 1
        print(
            f"Emergency ID: {visit['emergency_id']} | "
            f"Patient: {visit['patient_name']} | "
            f"Priority: {visit['priority']} | "
            f"Status: {visit['status']}"
        )

    if count == 0:
        print("No emergency visits found.")


def search_emergency_visits():
    print("\n--- Search Emergency Visits ---")

    patient_id = input("Enter Patient ID: ").strip()

    visits = emergency_visits_collection.find(
        {"patient_id": patient_id}
    ).sort("visit_time", -1)

    count = 0

    for visit in visits:
        count += 1
        print(
            f"Emergency ID: {visit['emergency_id']} | "
            f"Patient: {visit['patient_name']} | "
            f"Symptoms: {visit['symptoms']} | "
            f"Priority: {visit['priority']} | "
            f"Status: {visit['status']} | "
            f"Visit Time: {visit['visit_time']}"
        )

    if count == 0:
        print("No emergency visits found for this patient.")


def update_emergency_status():
    print("\n--- Update Emergency Status ---")

    emergency_id = input("Enter Emergency ID: ").strip()

    visit = emergency_visits_collection.find_one(
        {"emergency_id": emergency_id}
    )

    if not visit:
        print("Emergency visit not found.")
        return

    print("1. Under Treatment")
    print("2. Discharged")

    choice = input("Choose status: ").strip()

    if choice == "1":
        status = "Under Treatment"
        discharge_time = None
    elif choice == "2":
        status = "Discharged"
        discharge_time = datetime.now()
    else:
        print("Invalid choice.")
        return

    emergency_visits_collection.update_one(
        {"emergency_id": emergency_id},
        {
            "$set": {
                "status": status,
                "discharge_time": discharge_time
            }
        }
    )

    print("Emergency status updated successfully!")