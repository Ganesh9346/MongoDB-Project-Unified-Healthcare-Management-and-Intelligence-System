from config.database import doctors_collection
from pymongo.errors import DuplicateKeyError


def register_doctor():
    print("\n--- Register Doctor ---")

    doctor_id = input("Enter Doctor ID: ").strip()
    name = input("Enter Doctor Name: ").strip()
    specialization = input("Enter Specialization: ").strip()
    department = input("Enter Department: ").strip()
    phone = input("Enter Phone Number: ").strip()

    try:
        experience = int(input("Enter Years of Experience: "))

        if experience < 0 or experience > 80:
            print("Experience must be between 0 and 80 years.")
            return

    except ValueError:
        print("Invalid experience. Enter a whole number.")
        return

    if not all([
        doctor_id,
        name,
        specialization,
        department,
        phone
    ]):
        print("All fields are required.")
        return

    doctor = {
        "doctor_id": doctor_id,
        "name": name,
        "specialization": specialization,
        "department": department,
        "phone": phone,
        "experience": experience,
        "available": True
    }

    try:
        result = doctors_collection.insert_one(doctor)

        print("\nDoctor registered successfully!")
        print("MongoDB Document ID:", result.inserted_id)

    except DuplicateKeyError:
        print("Error: This Doctor ID already exists.")

def view_all_doctors():
    print("\n--- All Doctors ---")

    doctors = doctors_collection.find()

    count = 0

    for doctor in doctors:
        count += 1

        print("\nDoctor", count)
        print("Doctor ID:", doctor["doctor_id"])
        print("Name:", doctor["name"])
        print("Specialization:", doctor["specialization"])
        print("Department:", doctor["department"])
        print("Phone:", doctor["phone"])
        print("Experience:", doctor["experience"], "years")
        print("Available:", doctor["available"])

    if count == 0:
        print("No doctors found.")

def search_doctor():
    print("\n--- Search Doctor ---")

    doctor_id = input("Enter Doctor ID: ").strip()

    doctor = doctors_collection.find_one({
        "doctor_id": doctor_id
    })

    if doctor:
        print("\nDoctor Found!")
        print("Doctor ID:", doctor["doctor_id"])
        print("Name:", doctor["name"])
        print("Specialization:", doctor["specialization"])
        print("Department:", doctor["department"])
        print("Phone:", doctor["phone"])
        print("Experience:", doctor["experience"], "years")
        print("Available:", doctor["available"])

    else:
        print("Doctor not found.")

def update_doctor():
    print("\n--- Update Doctor ---")

    doctor_id = input("Enter Doctor ID to update: ").strip()

    doctor = doctors_collection.find_one({
        "doctor_id": doctor_id
    })

    if not doctor:
        print("Doctor not found.")
        return

    print("\nLeave a field empty to keep its current value.")

    name = input("Enter New Name: ").strip()
    specialization = input("Enter New Specialization: ").strip()
    department = input("Enter New Department: ").strip()
    phone = input("Enter New Phone Number: ").strip()
    experience_input = input("Enter New Experience: ").strip()

    updated_data = {}

    if name:
        updated_data["name"] = name

    if specialization:
        updated_data["specialization"] = specialization

    if department:
        updated_data["department"] = department

    if phone:
        updated_data["phone"] = phone

    if experience_input:
        try:
            experience = int(experience_input)

            if experience < 0 or experience > 80:
                print("Experience must be between 0 and 80 years.")
                return

            updated_data["experience"] = experience

        except ValueError:
            print("Invalid experience. Enter a whole number.")
            return

    if not updated_data:
        print("No changes provided.")
        return

    result = doctors_collection.update_one(
        {"doctor_id": doctor_id},
        {"$set": updated_data}
    )

    if result.modified_count > 0:
        print("Doctor details updated successfully!")

    else:
        print("No changes were made.")

def delete_doctor():
    print("\n--- Delete Doctor ---")

    doctor_id = input("Enter Doctor ID to delete: ").strip()

    doctor = doctors_collection.find_one({
        "doctor_id": doctor_id
    })

    if not doctor:
        print("Doctor not found.")
        return

    print("Doctor Name:", doctor["name"])

    confirm = input("Are you sure you want to delete? (yes/no): ").strip().lower()

    if confirm == "yes":
        result = doctors_collection.delete_one({
            "doctor_id": doctor_id
        })

        if result.deleted_count > 0:
            print("Doctor deleted successfully!")
        else:
            print("Doctor could not be deleted.")
    else:
        print("Deletion cancelled.")