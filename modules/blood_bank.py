from config.database import blood_bank_collection
from datetime import datetime
from pymongo.errors import PyMongoError


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

        if units <= 0:
            print("Units must be greater than zero.")
            return

    except ValueError:
        print("Enter a valid number of units.")
        return

    try:
        existing_record = blood_bank_collection.find_one(
            {"blood_group": blood_group}
        )

        if existing_record:
            blood_bank_collection.update_one(
                {"_id": existing_record["_id"]},
                {
                    "$inc": {"units": units},
                    "$set": {"updated_at": datetime.now()}
                }
            )

            print(
                f"Stock updated! New total: "
                f"{existing_record['units'] + units} units"
            )

        else:
            blood_bank_collection.insert_one({
                "blood_group": blood_group,
                "units": units,
                "updated_at": datetime.now()
            })

            print("Blood stock added successfully!")

    except PyMongoError as error:
        print(f"Failed to register blood stock: {error}")


def view_blood_stock():
    print("\n--- Blood Bank Inventory ---")

    try:
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

    except PyMongoError as error:
        print(f"Failed to retrieve blood stock: {error}")


def search_blood_stock():
    print("\n--- Search Blood Stock ---")

    blood_group = input("Enter Blood Group: ").strip().upper()

    if blood_group not in VALID_BLOOD_GROUPS:
        print("Invalid blood group.")
        return

    try:
        record = blood_bank_collection.find_one(
            {"blood_group": blood_group}
        )

        if record:
            print(f"Blood Group: {record['blood_group']}")
            print(f"Available Units: {record['units']}")
        else:
            print("No inventory record found.")

    except PyMongoError as error:
        print(f"Search failed: {error}")


def update_blood_stock():
    print("\n--- Update Blood Stock ---")

    blood_group = input("Enter Blood Group: ").strip().upper()

    if blood_group not in VALID_BLOOD_GROUPS:
        print("Invalid blood group.")
        return

    try:
        record = blood_bank_collection.find_one(
            {"blood_group": blood_group}
        )

        if not record:
            print("Blood group not found. Add stock first.")
            return

        print("1. Add Units")
        print("2. Remove Units")

        choice = input("Enter your choice: ").strip()

        if choice not in ["1", "2"]:
            print("Invalid choice.")
            return

        units = int(input("Enter Number of Units: "))

        if units <= 0:
            print("Units must be greater than zero.")
            return

        if choice == "1":
            result = blood_bank_collection.update_one(
                {"_id": record["_id"]},
                {
                    "$inc": {"units": units},
                    "$set": {"updated_at": datetime.now()}
                }
            )

        else:
            result = blood_bank_collection.update_one(
                {
                    "_id": record["_id"],
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
            print("Insufficient stock or stock has changed.")

    except ValueError:
        print("Enter a valid number.")

    except PyMongoError as error:
        print(f"Failed to update stock: {error}")


def view_low_blood_stock():
    print("\n--- Low Blood Stock ---")

    try:
        minimum_units = int(
            input("Enter minimum stock threshold: ")
        )

        if minimum_units < 0:
            print("Threshold cannot be negative.")
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

    except ValueError:
        print("Enter a valid number.")

    except PyMongoError as error:
        print(f"Failed to retrieve low stock: {error}")