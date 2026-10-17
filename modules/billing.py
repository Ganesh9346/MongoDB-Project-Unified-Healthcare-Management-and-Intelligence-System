from config.database import bills_collection, patients_collection
from pymongo.errors import DuplicateKeyError
from datetime import datetime


def generate_bill():
    print("\n--- Generate Patient Bill ---")

    bill_id = input("Enter Bill ID: ").strip()
    patient_id = input("Enter Patient ID: ").strip()

    if not bill_id or not patient_id:
        print("Bill ID and Patient ID are required.")
        return

    patient = patients_collection.find_one({"patient_id": patient_id})

    if not patient:
        print("Patient not found. Register the patient first.")
        return

    try:
        consultation_fee = float(input("Enter Consultation Fee: "))
        medicine_charges = float(input("Enter Medicine Charges: "))
        laboratory_charges = float(input("Enter Laboratory Charges: "))
        bed_charges = float(input("Enter Bed Charges: "))

        charges = [
            consultation_fee,
            medicine_charges,
            laboratory_charges,
            bed_charges
        ]

        if any(charge < 0 for charge in charges):
            print("Charges cannot be negative.")
            return

    except ValueError:
        print("Please enter valid numeric charges.")
        return

    total_amount = sum(charges)

    bill = {
        "bill_id": bill_id,
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "consultation_fee": consultation_fee,
        "medicine_charges": medicine_charges,
        "laboratory_charges": laboratory_charges,
        "bed_charges": bed_charges,
        "total_amount": total_amount,
        "paid_amount": 0.0,
        "balance": total_amount,
        "payment_status": "Pending",
        "created_at": datetime.now()
    }

    try:
        bills_collection.insert_one(bill)
        print("Bill generated successfully!")
        print(f"Total Amount: ₹{total_amount:.2f}")
    except DuplicateKeyError:
        print("This Bill ID already exists.")


def view_all_bills():
    print("\n--- All Patient Bills ---")

    bills = bills_collection.find().sort("created_at", -1)
    count = 0

    for bill in bills:
        count += 1
        print(
            f"Bill ID: {bill['bill_id']} | "
            f"Patient: {bill['patient_name']} | "
            f"Total: ₹{bill['total_amount']:.2f} | "
            f"Paid: ₹{bill['paid_amount']:.2f} | "
            f"Balance: ₹{bill['balance']:.2f} | "
            f"Status: {bill['payment_status']}"
        )

    if count == 0:
        print("No bills found.")


def search_bills_by_patient():
    print("\n--- Search Bills by Patient ---")

    patient_id = input("Enter Patient ID: ").strip()

    bills = bills_collection.find({"patient_id": patient_id})
    count = 0

    for bill in bills:
        count += 1
        print(
            f"Bill ID: {bill['bill_id']} | "
            f"Patient: {bill['patient_name']} | "
            f"Total: ₹{bill['total_amount']:.2f} | "
            f"Paid: ₹{bill['paid_amount']:.2f} | "
            f"Balance: ₹{bill['balance']:.2f} | "
            f"Status: {bill['payment_status']}"
        )

    if count == 0:
        print("No bills found for this patient.")


def record_payment():
    print("\n--- Record Payment ---")

    bill_id = input("Enter Bill ID: ").strip()

    bill = bills_collection.find_one({"bill_id": bill_id})

    if not bill:
        print("Bill not found.")
        return

    if bill["balance"] <= 0:
        print("This bill has already been fully paid.")
        return

    try:
        amount = float(input("Enter Payment Amount: "))

        if amount <= 0:
            print("Payment amount must be greater than zero.")
            return

        if amount > bill["balance"]:
            print(f"Payment cannot exceed the remaining balance of ₹{bill['balance']:.2f}.")
            return

    except ValueError:
        print("Please enter a valid payment amount.")
        return

    new_paid_amount = bill["paid_amount"] + amount
    new_balance = bill["total_amount"] - new_paid_amount

    if new_balance == 0:
        payment_status = "Paid"
    else:
        payment_status = "Partially Paid"

    bills_collection.update_one(
        {"bill_id": bill_id},
        {
            "$set": {
                "paid_amount": new_paid_amount,
                "balance": new_balance,
                "payment_status": payment_status,
                "last_payment_date": datetime.now()
            }
        }
    )

    print("Payment recorded successfully!")
    print(f"Total Paid: ₹{new_paid_amount:.2f}")
    print(f"Remaining Balance: ₹{new_balance:.2f}")
    print(f"Payment Status: {payment_status}")


def view_pending_payments():
    print("\n--- Pending Payments ---")

    bills = bills_collection.find(
        {"balance": {"$gt": 0}}
    )

    count = 0

    for bill in bills:
        count += 1
        print(
            f"Bill ID: {bill['bill_id']} | "
            f"Patient: {bill['patient_name']} | "
            f"Total: ₹{bill['total_amount']:.2f} | "
            f"Paid: ₹{bill['paid_amount']:.2f} | "
            f"Balance: ₹{bill['balance']:.2f}"
        )

    if count == 0:
        print("No pending payments.")