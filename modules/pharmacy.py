from config.database import medicines_collection
from pymongo.errors import DuplicateKeyError
from datetime import datetime


def add_medicine():
    print("\n--- Add Medicine ---")

    medicine_id = input("Enter Medicine ID: ").strip()
    name = input("Enter Medicine Name: ").strip()
    category = input("Enter Category: ").strip()
    manufacturer = input("Enter Manufacturer: ").strip()

    try:
        price = float(input("Enter Price per Unit: "))
        quantity = int(input("Enter Stock Quantity: "))
        reorder_level = int(input("Enter Low-Stock Alert Level: "))

        if price < 0 or quantity < 0 or reorder_level < 0:
            print("Price, quantity, and reorder level cannot be negative.")
            return

    except ValueError:
        print("Invalid input. Enter numeric values for price and stock.")
        return

    expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ").strip()

    if not all([
        medicine_id,
        name,
        category,
        manufacturer,
        expiry_date
    ]):
        print("All fields are required.")
        return

    try:
        datetime.strptime(expiry_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid expiry date. Use YYYY-MM-DD.")
        return

    medicine = {
        "medicine_id": medicine_id,
        "name": name,
        "category": category,
        "manufacturer": manufacturer,
        "price": price,
        "quantity": quantity,
        "reorder_level": reorder_level,
        "expiry_date": expiry_date,
        "created_at": datetime.now()
    }

    try:
        medicines_collection.insert_one(medicine)
        print("Medicine added successfully!")

    except DuplicateKeyError:
        print("This Medicine ID already exists.")


def view_all_medicines():
    print("\n--- Medicine Inventory ---")

    medicines = medicines_collection.find()
    count = 0

    for medicine in medicines:
        count += 1

        print("\nMedicine ID:", medicine["medicine_id"])
        print("Name:", medicine["name"])
        print("Category:", medicine["category"])
        print("Manufacturer:", medicine["manufacturer"])
        print("Price:", medicine["price"])
        print("Quantity:", medicine["quantity"])
        print("Reorder Level:", medicine["reorder_level"])
        print("Expiry Date:", medicine["expiry_date"])

    if count == 0:
        print("No medicines found.")


def search_medicine():
    print("\n--- Search Medicine ---")

    medicine_id = input("Enter Medicine ID: ").strip()

    medicine = medicines_collection.find_one({
        "medicine_id": medicine_id
    })

    if medicine:
        print("\nMedicine Found!")
        print("Medicine ID:", medicine["medicine_id"])
        print("Name:", medicine["name"])
        print("Category:", medicine["category"])
        print("Manufacturer:", medicine["manufacturer"])
        print("Price:", medicine["price"])
        print("Quantity:", medicine["quantity"])
        print("Reorder Level:", medicine["reorder_level"])
        print("Expiry Date:", medicine["expiry_date"])
    else:
        print("Medicine not found.")


def update_medicine_stock():
    print("\n--- Update Medicine Stock ---")

    medicine_id = input("Enter Medicine ID: ").strip()

    medicine = medicines_collection.find_one({
        "medicine_id": medicine_id
    })

    if not medicine:
        print("Medicine not found.")
        return

    print("Current Stock:", medicine["quantity"])

    try:
        new_quantity = int(input("Enter New Stock Quantity: "))

        if new_quantity < 0:
            print("Stock quantity cannot be negative.")
            return

    except ValueError:
        print("Enter a valid whole number.")
        return

    medicines_collection.update_one(
        {"medicine_id": medicine_id},
        {"$set": {"quantity": new_quantity}}
    )

    print("Medicine stock updated successfully!")


def view_low_stock_medicines():
    print("\n--- Low-Stock Medicines ---")

    medicines = medicines_collection.find({
        "$expr": {
            "$lte": ["$quantity", "$reorder_level"]
        }
    })

    count = 0

    for medicine in medicines:
        count += 1

        print("\nMedicine:", medicine["name"])
        print("Medicine ID:", medicine["medicine_id"])
        print("Current Stock:", medicine["quantity"])
        print("Reorder Level:", medicine["reorder_level"])

    if count == 0:
        print("No low-stock medicines found.")


def delete_medicine():
    print("\n--- Delete Medicine ---")

    medicine_id = input("Enter Medicine ID: ").strip()

    medicine = medicines_collection.find_one({
        "medicine_id": medicine_id
    })

    if not medicine:
        print("Medicine not found.")
        return

    confirm = input(
        f"Delete {medicine['name']}? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        medicines_collection.delete_one({
            "medicine_id": medicine_id
        })
        print("Medicine deleted successfully!")
    else:
        print("Deletion cancelled.")