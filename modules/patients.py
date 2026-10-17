from config.database import patients_collection
from pymongo.errors import DuplicateKeyError

def register_patient():
    print("\n--- Register Patient ---")

    patient_id = input("Enter Patient ID: ").strip()
    name = input("Enter Patient Name: ").strip()

    try:
        age = int(input("Enter Age: "))

        if age < 0 or age > 130:
            print("Age must be between 0 and 130.")
            return

    except ValueError:
        print("Invalid age. Please enter a whole number.")
        return

    gender = input("Enter Gender: ").strip()
    phone = input("Enter Phone Number: ").strip()
    blood_group = input("Enter Blood Group: ").strip().upper()
    address = input("Enter Address: ").strip()

    if not all([
        patient_id,
        name,
        gender,
        phone,
        blood_group,
        address
    ]):
        print("All fields are required.")
        return

    patient = {
        "patient_id": patient_id,
        "name": name,
        "age": age,
        "gender": gender,
        "phone": phone,
        "blood_group": blood_group,
        "address": address
    }

    try:
        result = patients_collection.insert_one(patient)

        print("\nPatient registered successfully!")
        print("MongoDB Document ID:", result.inserted_id)

    except DuplicateKeyError:
        print("Error: This Patient ID already exists.")

def view_all_patients():
    print("\n--- All Registered Patients ---")

    patients = patients_collection.find()

    count = 0

    for patient in patients:
        count += 1

        print("\nPatient ID:", patient["patient_id"])
        print("Name:", patient["name"])
        print("Age:", patient["age"])
        print("Gender:", patient["gender"])
        print("Phone:", patient["phone"])
        print("Blood Group:", patient["blood_group"])
        print("Address:", patient["address"])

    if count == 0:
        print("No patients found.")

def search_patient():
    print("\n--- Search Patient ---")

    patient_id = input("Enter Patient ID: ").strip()

    patient = patients_collection.find_one(
        {"patient_id": patient_id}
    )

    if patient:
        print("\nPatient Found!")
        print("Patient ID:", patient["patient_id"])
        print("Name:", patient["name"])
        print("Age:", patient["age"])
        print("Gender:", patient["gender"])
        print("Phone:", patient["phone"])
        print("Blood Group:", patient["blood_group"])
        print("Address:", patient["address"])
    else:
        print("Patient not found.")

def update_patient():
    print("\n--- Update Patient ---")

    patient_id = input("Enter Patient ID to update: ").strip()

    patient = patients_collection.find_one(
        {"patient_id": patient_id}
    )

    if patient is None:
        print("Patient not found.")
        return

    print("Leave a field empty to keep its existing value.")

    name = input("New Name: ").strip()
    age = input("New Age: ").strip()
    gender = input("New Gender: ").strip()
    phone = input("New Phone: ").strip()
    blood_group = input("New Blood Group: ").strip()
    address = input("New Address: ").strip()

    updated_data = {}

    if name:
        updated_data["name"] = name

    if age:
        try:
            updated_age = int(age)

            if updated_age < 0 or updated_age > 130:
                print("Age must be between 0 and 130.")
                return

            updated_data["age"] = updated_age

        except ValueError:
            print("Invalid age. Enter a whole number.")
            return

    if gender:
        updated_data["gender"] = gender

    if phone:
        updated_data["phone"] = phone

    if blood_group:
        updated_data["blood_group"] = blood_group.upper()

    if address:
        updated_data["address"] = address

    if not updated_data:
        print("No changes entered.")
        return

    result = patients_collection.update_one(
        {"patient_id": patient_id},
        {"$set": updated_data}
    )

    if result.modified_count > 0:
        print("Patient updated successfully.")
    else:
        print("No changes were made.")

def delete_patient():
    print("\n--- Delete Patient ---")

    patient_id = input("Enter Patient ID to delete: ").strip()

    patient = patients_collection.find_one(
        {"patient_id": patient_id}
    )

    if patient is None:
        print("Patient not found.")
        return

    print("Patient Name:", patient["name"])

    confirm = input(
        "Confirm deletion? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        result = patients_collection.delete_one(
            {"patient_id": patient_id}
        )

        if result.deleted_count == 1:
            print("Patient deleted successfully.")
        else:
            print("Patient could not be deleted.")

    else:
        print("Deletion cancelled.")