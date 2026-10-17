from config.database import blood_bank_collection
from pymongo.errors import DuplicateKeyError
from datetime import datetime


VALID_BLOOD_GROUPS = [
    "A+", "A-", "B+", "B-",
    "AB+", "AB-", "O+", "O-"
]


def add_blood_stock():
    print("\n--- Add Blood Stock ---")

    blood_group = input("Enter Blood Group: ").strip().upper()

    if blood_group not in VALID_BLOOD_GROUPS:
        print("Invalid blood group.")
        return

    try:
        units = int(input("Enter Available Units: "))

        if units < 0:
            print("Units cannot be negative.")
            return

    except ValueError:
        print("Enter a valid number of units.")
        return

    blood_record = {
        "blood_group": blood_group,
        "units": units,
        "updated_at": datetime.now()
    }

    try:
        blood_bank_collection.insert_one(blood_record)
        print("Blood stock added successfully!")

    except DuplicateKeyError:
        print("This blood group already exists. Use Update Stock instead.")


def view_blood_stock():
    print("\n--- Blood Bank Inventory ---")

    records = blood_bank_collection.find().sort("blood_group", 1)
    count = 0

    for record in records:
        count += 1

        print(
            f"Blood Group: {record['blood_group']} | "
            f"Available Units: {record['units']}"
        )

    if count == 0:
        print("No blood stock records found.")


def search_blood_stock():
    print("\n--- Search Blood Stock ---")

    blood_group = input("Enter Blood Group: ").strip().upper()

    if blood_group not in VALID_BLOOD_GROUPS:
        print("Invalid blood group.")
        return

    record = blood_bank_collection.find_one(
        {"blood_group": blood_group}
    )

    if record:
        print(f"Blood Group: {record['blood_group']}")
        print(f"Available Units: {record['units']}")
    else:
        print("No inventory record found for this blood group.")


def update_blood_stock():
    print("\n--- Update Blood Stock ---")

    blood_group = input("Enter Blood Group: ").strip().upper()

    if blood_group not in VALID_BLOOD_GROUPS:
        print("Invalid blood group.")
        return

    record = blood_bank_collection.find_one(
        {"blood_group": blood_group}
    )

    if not record:
        print("Blood group not found. Add its stock first.")
        return

    print("1. Add Units")
    print("2. Remove Units")

    choice = input("Enter your choice: ").strip()

    if choice not in ["1", "2"]:
        print("Invalid choice.")
        return

    try:
        units = int(input("Enter Number of Units: "))

        if units <= 0:
            print("Units must be greater than zero.")
            return

    except ValueError:
        print("Enter a valid number of units.")
        return

    if choice == "1":
        result = blood_bank_collection.update_one(
            {
                "blood_group": blood_group,
                "units": record["units"]
            },
            {
                "$inc": {"units": units},
                "$set": {"updated_at": datetime.now()}
            }
        )

    else:
        result = blood_bank_collection.update_one(
            {
                "blood_group": blood_group,
                "units": {"$gte": units}
            },
            {
                "$inc": {"units": -units},
                "$set": {"updated_at": datetime.now()}
            }
        )

    if result.modified_count == 1:
        print("Blood stock updated successfully!")
    else:
        print("Stock changed or insufficient units. Check the current stock and try again.")


def view_low_blood_stock():
    print("\n--- Low Blood Stock ---")

    try:
        minimum_units = int(
            input("Enter minimum stock threshold: ")
        )

        if minimum_units < 0:
            print("Threshold cannot be negative.")
            return

    except ValueError:
        print("Enter a valid number.")
        return

    records = blood_bank_collection.find(
        {"units": {"$lte": minimum_units}}
    ).sort("blood_group", 1)

    count = 0

    for record in records:
        count += 1

        print(
            f"Blood Group: {record['blood_group']} | "
            f"Available Units: {record['units']}"
        )

    if count == 0:
        print("No blood groups are below the specified threshold.")