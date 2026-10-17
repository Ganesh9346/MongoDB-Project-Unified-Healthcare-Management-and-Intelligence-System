from config.database import equipment_collection
from pymongo.errors import DuplicateKeyError
from datetime import datetime


def add_equipment():
    print("\n--- Add Medical Equipment ---")

    equipment_id = input("Enter Equipment ID: ").strip()
    name = input("Enter Equipment Name: ").strip()
    department = input("Enter Department: ").strip()

    try:
        quantity = int(input("Enter Quantity: "))

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

    except ValueError:
        print("Enter a valid quantity.")
        return

    if not all([equipment_id, name, department]):
        print("All fields are required.")
        return

    equipment = {
        "equipment_id": equipment_id,
        "name": name,
        "department": department,
        "quantity": quantity,
        "status": "Available",
        "created_at": datetime.now()
    }

    try:
        equipment_collection.insert_one(equipment)
        print("Medical equipment added successfully!")

    except DuplicateKeyError:
        print("This Equipment ID already exists.")


def view_all_equipment():
    print("\n--- Medical Equipment Inventory ---")

    equipment_list = equipment_collection.find()
    count = 0

    for item in equipment_list:
        count += 1

        print(
            f"ID: {item['equipment_id']} | "
            f"Name: {item['name']} | "
            f"Department: {item['department']} | "
            f"Quantity: {item['quantity']} | "
            f"Status: {item['status']}"
        )

    if count == 0:
        print("No medical equipment found.")


def search_equipment():
    print("\n--- Search Medical Equipment ---")

    equipment_id = input("Enter Equipment ID: ").strip()

    item = equipment_collection.find_one(
        {"equipment_id": equipment_id}
    )

    if item:
        print(f"Equipment ID: {item['equipment_id']}")
        print(f"Name: {item['name']}")
        print(f"Department: {item['department']}")
        print(f"Quantity: {item['quantity']}")
        print(f"Status: {item['status']}")
    else:
        print("Equipment not found.")


def update_equipment_status():
    print("\n--- Update Equipment Status ---")

    equipment_id = input("Enter Equipment ID: ").strip()

    item = equipment_collection.find_one(
        {"equipment_id": equipment_id}
    )

    if not item:
        print("Equipment not found.")
        return

    print("1. Available")
    print("2. In Use")
    print("3. Under Maintenance")

    choice = input("Select new status: ").strip()

    statuses = {
        "1": "Available",
        "2": "In Use",
        "3": "Under Maintenance"
    }

    if choice not in statuses:
        print("Invalid choice.")
        return

    equipment_collection.update_one(
        {"equipment_id": equipment_id},
        {
            "$set": {
                "status": statuses[choice],
                "updated_at": datetime.now()
            }
        }
    )

    print("Equipment status updated successfully!")