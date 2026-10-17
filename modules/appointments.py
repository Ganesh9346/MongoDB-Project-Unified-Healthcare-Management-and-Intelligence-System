from config.database import (
    appointments_collection,
    patients_collection,
    doctors_collection
)
from pymongo.errors import DuplicateKeyError
from datetime import datetime


def book_appointment():
    print("\n--- Book Appointment ---")

    appointment_id = input("Enter Appointment ID: ").strip()
    patient_id = input("Enter Patient ID: ").strip()
    doctor_id = input("Enter Doctor ID: ").strip()
    appointment_date = input(
        "Enter appointment date (YYYY-MM-DD): "
    ).strip()
    appointment_time = input(
        "Enter appointment time (HH:MM, 24-hour format): "
    ).strip()
    reason = input("Enter appointment reason: ").strip()

    if not all([
        appointment_id,
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        reason
    ]):
        print("All fields are required.")
        return

    # Check whether the patient exists
    patient = patients_collection.find_one({
        "patient_id": patient_id
    })

    if not patient:
        print("Patient not found. Register the patient first.")
        return

    # Check whether the doctor exists
    doctor = doctors_collection.find_one({
        "doctor_id": doctor_id
    })

    if not doctor:
        print("Doctor not found. Register the doctor first.")
        return

    # Validate date and time
    try:
        appointment_datetime = datetime.strptime(
            f"{appointment_date} {appointment_time}",
            "%Y-%m-%d %H:%M"
        )

    except ValueError:
        print("Invalid date or time format.")
        return

    if appointment_datetime < datetime.now():
        print("Appointment must be in the future.")
        return

    # Create appointment document
    appointment = {
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "doctor_id": doctor_id,
        "doctor_name": doctor["name"],
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
        "reason": reason,
        "status": "Scheduled",
        "created_at": datetime.now()
    }

    try:
        appointments_collection.insert_one(appointment)
        print("Appointment booked successfully!")

    except DuplicateKeyError:
        print("This appointment ID already exists.")

def view_all_appointments():
    print("\n--- All Appointments ---")

    appointments = appointments_collection.find()
    count = 0

    for appointment in appointments:
        count += 1

        print("\nAppointment ID:", appointment["appointment_id"])
        print("Patient:", appointment["patient_name"])
        print("Doctor:", appointment["doctor_name"])
        print("Date:", appointment["appointment_date"])
        print("Time:", appointment["appointment_time"])
        print("Reason:", appointment["reason"])
        print("Status:", appointment["status"])

    if count == 0:
        print("No appointments found.")

def search_appointment():
    print("\n--- Search Appointment ---")

    appointment_id = input("Enter Appointment ID: ").strip()

    appointment = appointments_collection.find_one({
        "appointment_id": appointment_id
    })

    if appointment:
        print("\nAppointment Found!")
        print("Appointment ID:", appointment["appointment_id"])
        print("Patient:", appointment["patient_name"])
        print("Doctor:", appointment["doctor_name"])
        print("Date:", appointment["appointment_date"])
        print("Time:", appointment["appointment_time"])
        print("Reason:", appointment["reason"])
        print("Status:", appointment["status"])
    else:
        print("Appointment not found.")

def cancel_appointment():
    print("\n--- Cancel Appointment ---")

    appointment_id = input("Enter Appointment ID: ").strip()

    appointment = appointments_collection.find_one({
        "appointment_id": appointment_id
    })

    if not appointment:
        print("Appointment not found.")
        return

    if appointment["status"] == "Cancelled":
        print("This appointment is already cancelled.")
        return

    result = appointments_collection.update_one(
        {"appointment_id": appointment_id},
        {"$set": {"status": "Cancelled"}}
    )

    if result.modified_count > 0:
        print("Appointment cancelled successfully.")
    else:
        print("Appointment status was not changed.")