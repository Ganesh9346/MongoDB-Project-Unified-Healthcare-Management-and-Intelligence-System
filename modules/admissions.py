from config.database import (
    beds_collection,
    admissions_collection,
    patients_collection
)
from pymongo.errors import DuplicateKeyError
from datetime import datetime


def add_bed():
    print("\n--- Add Hospital Bed ---")

    bed_id = input("Enter Bed ID: ").strip()
    ward = input("Enter Ward Name: ").strip()
    bed_type = input("Enter Bed Type (General/ICU/Private): ").strip()

    if not all([bed_id, ward, bed_type]):
        print("All fields are required.")
        return

    bed = {
        "bed_id": bed_id,
        "ward": ward,
        "bed_type": bed_type,
        "status": "Available"
    }

    try:
        beds_collection.insert_one(bed)
        print("Bed added successfully!")

    except DuplicateKeyError:
        print("This Bed ID already exists.")


def view_all_beds():
    print("\n--- Hospital Beds ---")

    beds = beds_collection.find()
    count = 0

    for bed in beds:
        count += 1
        print(
            f"Bed ID: {bed['bed_id']} | "
            f"Ward: {bed['ward']} | "
            f"Type: {bed['bed_type']} | "
            f"Status: {bed['status']}"
        )

    if count == 0:
        print("No beds registered.")


def view_available_beds():
    print("\n--- Available Beds ---")

    beds = beds_collection.find({
        "status": "Available"
    })

    count = 0

    for bed in beds:
        count += 1
        print(
            f"Bed ID: {bed['bed_id']} | "
            f"Ward: {bed['ward']} | "
            f"Type: {bed['bed_type']}"
        )

    if count == 0:
        print("No beds are currently available.")


def admit_patient():
    print("\n--- Admit Patient ---")

    admission_id = input("Enter Admission ID: ").strip()
    patient_id = input("Enter Patient ID: ").strip()
    bed_id = input("Enter Bed ID: ").strip()

    if not all([admission_id, patient_id, bed_id]):
        print("All fields are required.")
        return

    patient = patients_collection.find_one({
        "patient_id": patient_id
    })

    if not patient:
        print("Patient not found. Register the patient first.")
        return

    bed = beds_collection.find_one({
        "bed_id": bed_id
    })

    if not bed:
        print("Bed not found.")
        return

    if bed["status"] != "Available":
        print("This bed is not available.")
        return

    admission = {
        "admission_id": admission_id,
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "bed_id": bed_id,
        "ward": bed["ward"],
        "admission_date": datetime.now(),
        "discharge_date": None,
        "status": "Admitted"
    }

    try:
        # Reserve the bed only if it is still available.
        bed_result = beds_collection.update_one(
            {
                "bed_id": bed_id,
                "status": "Available"
            },
            {
                "$set": {"status": "Occupied"}
            }
        )

        if bed_result.modified_count == 0:
            print("This bed is no longer available.")
            return

        try:
            admissions_collection.insert_one(admission)
            print("Patient admitted successfully!")

        except DuplicateKeyError:
            # Restore the bed if the admission ID already exists.
            beds_collection.update_one(
                {"bed_id": bed_id, "status": "Occupied"},
                {"$set": {"status": "Available"}}
            )
            print("This Admission ID already exists.")

    except Exception as e:
        print("Admission failed:", e)


def view_admitted_patients():
    print("\n--- Admitted Patients ---")

    admissions = admissions_collection.find({
        "status": "Admitted"
    })

    count = 0

    for admission in admissions:
        count += 1
        print(
            f"Admission ID: {admission['admission_id']} | "
            f"Patient: {admission['patient_name']} | "
            f"Patient ID: {admission['patient_id']} | "
            f"Bed ID: {admission['bed_id']} | "
            f"Ward: {admission['ward']} | "
            f"Admitted: {admission['admission_date']}"
        )

    if count == 0:
        print("No patients are currently admitted.")


def discharge_patient():
    print("\n--- Discharge Patient ---")

    admission_id = input("Enter Admission ID: ").strip()

    admission = admissions_collection.find_one({
        "admission_id": admission_id,
        "status": "Admitted"
    })

    if not admission:
        print("Active admission not found.")
        return

    # Release the bed only if it is currently occupied.
    bed_result = beds_collection.update_one(
        {
            "bed_id": admission["bed_id"],
            "status": "Occupied"
        },
        {
            "$set": {"status": "Available"}
        }
    )

    if bed_result.modified_count == 0:
        print("Bed status is inconsistent. Please check the records.")
        return

    admissions_collection.update_one(
        {"admission_id": admission_id},
        {
            "$set": {
                "status": "Discharged",
                "discharge_date": datetime.now()
            }
        }
    )

    print("Patient discharged and bed released successfully!")