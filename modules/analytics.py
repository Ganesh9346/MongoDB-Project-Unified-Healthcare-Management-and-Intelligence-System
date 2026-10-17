from config.database import (
    patients_collection,
    doctors_collection,
    appointments_collection,
    medical_history_collection,
    medicines_collection,
    lab_tests_collection,
    beds_collection,
    admissions_collection,
    emergency_visits_collection,
    bills_collection,
    follow_ups_collection,
    equipment_collection,
    blood_bank_collection
)


def hospital_overview():
    print("\n========== HOSPITAL OVERVIEW ==========")

    print("Total Patients:", patients_collection.count_documents({}))
    print("Total Doctors:", doctors_collection.count_documents({}))
    print("Total Appointments:", appointments_collection.count_documents({}))
    print("Medical History Records:", medical_history_collection.count_documents({}))
    print("Total Medicines:", medicines_collection.count_documents({}))
    print("Laboratory Tests:", lab_tests_collection.count_documents({}))
    print("Total Beds:", beds_collection.count_documents({}))
    print("Active Admissions:", admissions_collection.count_documents(
        {"status": "Admitted"}
    ))
    print("Emergency Visits:", emergency_visits_collection.count_documents({}))
    print("Total Bills:", bills_collection.count_documents({}))
    print("Scheduled Follow-Ups:", follow_ups_collection.count_documents(
        {"status": "Scheduled"}
    ))
    print("Medical Equipment Records:", equipment_collection.count_documents({}))

    total_blood_units = sum(
        record["units"]
        for record in blood_bank_collection.find({}, {"units": 1})
    )

    print("Total Blood Units:", total_blood_units)


def appointment_report():
    print("\n========== APPOINTMENT REPORT ==========")

    pipeline = [
        {
            "$group": {
                "_id": "$status",
                "total": {"$sum": 1}
            }
        }
    ]

    results = appointments_collection.aggregate(pipeline)

    for result in results:
        print(f"{result['_id']}: {result['total']}")


def pharmacy_report():
    print("\n========== PHARMACY REPORT ==========")

    pipeline = [
        {
            "$group": {
                "_id": None,
                "total_medicines": {"$sum": 1},
                "total_stock": {"$sum": "$quantity"}
            }
        }
    ]

    results = list(medicines_collection.aggregate(pipeline))

    if not results:
        print("No medicine records found.")
        return

    report = results[0]

    print("Medicine Records:", report["total_medicines"])
    print("Total Stock Quantity:", report["total_stock"])


def billing_report():
    print("\n========== BILLING REPORT ==========")

    pipeline = [
        {
            "$group": {
                "_id": None,
                "total_billed": {"$sum": "$total_amount"},
                "total_paid": {"$sum": "$paid_amount"},
                "total_pending": {"$sum": "$balance"}
            }
        }
    ]

    result = list(bills_collection.aggregate(pipeline))

    if not result:
        print("No billing records found.")
        return

    report = result[0]

    print(f"Total Billed: ₹{report['total_billed']:.2f}")
    print(f"Total Paid: ₹{report['total_paid']:.2f}")
    print(f"Outstanding Balance: ₹{report['total_pending']:.2f}")


def emergency_report():
    print("\n========== EMERGENCY REPORT ==========")

    pipeline = [
        {
            "$group": {
                "_id": {
                    "priority": "$priority",
                    "status": "$status"
                },
                "total_visits": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "_id.priority": 1
            }
        }
    ]

    results = list(emergency_visits_collection.aggregate(pipeline))

    if not results:
        print("No emergency visits found.")
        return

    for result in results:
        print(
            f"Priority: {result['_id']['priority']} | "
            f"Status: {result['_id']['status']} | "
            f"Total Visits: {result['total_visits']}"
        )


