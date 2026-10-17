from config.database import lab_tests_collection, patients_collection
from pymongo.errors import DuplicateKeyError
from datetime import datetime


def register_lab_test():
    print("\n--- Register Laboratory Test ---")

    test_id = input("Enter Test ID: ").strip()
    patient_id = input("Enter Patient ID: ").strip()
    test_name = input("Enter Test Name: ").strip()
    doctor_name = input("Enter Referring Doctor Name: ").strip()

    if not all([test_id, patient_id, test_name, doctor_name]):
        print("All fields are required.")
        return

    patient = patients_collection.find_one({
        "patient_id": patient_id
    })

    if not patient:
        print("Patient not found. Register the patient first.")
        return

    lab_test = {
        "test_id": test_id,
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "test_name": test_name,
        "doctor_name": doctor_name,
        "result": "Pending",
        "status": "Requested",
        "created_at": datetime.now()
    }

    try:
        lab_tests_collection.insert_one(lab_test)
        print("Laboratory test registered successfully!")

    except DuplicateKeyError:
        print("This Test ID already exists.")


def view_all_lab_tests():
    print("\n--- All Laboratory Tests ---")

    tests = lab_tests_collection.find()
    count = 0

    for test in tests:
        count += 1

        print("\nTest ID:", test["test_id"])
        print("Patient ID:", test["patient_id"])
        print("Patient Name:", test["patient_name"])
        print("Test Name:", test["test_name"])
        print("Referring Doctor:", test["doctor_name"])
        print("Result:", test["result"])
        print("Status:", test["status"])

    if count == 0:
        print("No laboratory tests found.")


def search_lab_tests_by_patient():
    print("\n--- Search Laboratory Tests by Patient ---")

    patient_id = input("Enter Patient ID: ").strip()

    tests = lab_tests_collection.find({
        "patient_id": patient_id
    })

    count = 0

    for test in tests:
        count += 1

        print("\nTest ID:", test["test_id"])
        print("Test Name:", test["test_name"])
        print("Result:", test["result"])
        print("Status:", test["status"])

    if count == 0:
        print("No laboratory tests found for this patient.")


def record_lab_result():
    print("\n--- Record Laboratory Result ---")

    test_id = input("Enter Test ID: ").strip()

    test = lab_tests_collection.find_one({
        "test_id": test_id
    })

    if not test:
        print("Laboratory test not found.")
        return

    if test["status"] == "Completed":
        print("This test is already completed.")
        return

    result = input("Enter Test Result: ").strip()

    if not result:
        print("Result cannot be empty.")
        return

    lab_tests_collection.update_one(
        {"test_id": test_id},
        {
            "$set": {
                "result": result,
                "status": "Completed",
                "result_recorded_at": datetime.now()
            }
        }
    )

    print("Laboratory result recorded successfully!")


def update_lab_test_status():
    print("\n--- Update Laboratory Test Status ---")

    test_id = input("Enter Test ID: ").strip()

    test = lab_tests_collection.find_one({
        "test_id": test_id
    })

    if not test:
        print("Laboratory test not found.")
        return

    print("1. Requested")
    print("2. In Progress")
    print("3. Completed")
    print("4. Cancelled")

    choice = input("Select new status: ").strip()

    statuses = {
        "1": "Requested",
        "2": "In Progress",
        "3": "Completed",
        "4": "Cancelled"
    }

    if choice not in statuses:
        print("Invalid status selection.")
        return

    new_status = statuses[choice]

    if new_status == "Completed" and test["result"] == "Pending":
        print("Record the test result before marking it completed.")
        return

    lab_tests_collection.update_one(
        {"test_id": test_id},
        {"$set": {"status": new_status}}
    )

    print("Laboratory test status updated successfully!")