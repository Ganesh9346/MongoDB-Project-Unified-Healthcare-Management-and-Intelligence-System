from modules.analytics import (
    hospital_overview,
    appointment_report,
    pharmacy_report,
    billing_report,
    emergency_report,
    bed_availability_report
)

while True:
    print("\n===== Hospital Analytics and Reports =====")
    print("1. Hospital Overview")
    print("2. Appointment Report")
    print("3. Pharmacy Report")
    print("4. Billing Report")
    print("5. Emergency Report")
    print("6. Bed Availability Report")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        hospital_overview()
    elif choice == "2":
        appointment_report()
    elif choice == "3":
        pharmacy_report()
    elif choice == "4":
        billing_report()
    elif choice == "5":
        emergency_report()
    elif choice == "6":
        bed_availability_report()
    elif choice == "0":
        break
    else:
        print("Invalid choice.")