from config.database import (
    medical_history_collection,
    patients_collection
)
from pymongo.errors import DuplicateKeyError
from datetime import datetime


def add_medical_history():
    print("\n--- Add Medical History ---")

    history_id = input("Enter History ID: ").strip()
    patient_id = input("Enter Patient ID: ").strip()
    diagnosis = input("Enter Diagnosis: ").strip()
    allergies = input("Enter Allergies (or None): ").strip()
    medications = input("Enter Current Medications (or None): ").strip()
    notes = input("Enter Additional Notes: ").strip()

    if not all([
        history_id,
        patient_id,
        diagnosis,
        allergies,
        medications,
        notes
    ]):
        print("All fields are required. Enter None if not applicable.")
        return

    patient = patients_collection.find_one({
        "patient_id": patient_id
    })

    if not patient:
        print("Patient not found. Register the patient first.")
        return

    history = {
        "history_id": history_id,
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "diagnosis": diagnosis,
        "allergies": allergies,
        "medications": medications,
        "notes": notes,
        "recorded_at": datetime.now()
    }

    try:
        medical_history_collection.insert_one(history)
        print("Medical history recorded successfully!")

    except DuplicateKeyError:
        print("This History ID already exists.")


def view_all_medical_history():
    print("\n--- All Medical History Records ---")

    records = medical_history_collection.find()
    count = 0

    for record in records:
        count += 1

        print("\nHistory ID:", record["history_id"])
        print("Patient ID:", record["patient_id"])
        print("Patient Name:", record["patient_name"])
        print("Diagnosis:", record["diagnosis"])
        print("Allergies:", record["allergies"])
        print("Medications:", record["medications"])
        print("Notes:", record["notes"])
        print("Recorded At:", record["recorded_at"])

    if count == 0:
        print("No medical history records found.")


def view_patient_history():
    print("\n--- Search Patient Medical History ---")

    patient_id = input("Enter Patient ID: ").strip()

    records = medical_history_collection.find({
        "patient_id": patient_id
    })

    count = 0

    for record in records:
        count += 1

        print("\nHistory ID:", record["history_id"])
        print("Patient Name:", record["patient_name"])
        print("Diagnosis:", record["diagnosis"])
        print("Allergies:", record["allergies"])
        print("Medications:", record["medications"])
        print("Notes:", record["notes"])
        print("Recorded At:", record["recorded_at"])

    if count == 0:
        print("No medical history found for this patient.")