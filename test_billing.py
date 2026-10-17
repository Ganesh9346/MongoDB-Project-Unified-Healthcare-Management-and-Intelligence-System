from modules.billing import (
    generate_bill,
    view_all_bills,
    search_bills_by_patient,
    record_payment,
    view_pending_payments
)

while True:
    print("\n===== Billing and Payments =====")
    print("1. Generate Bill")
    print("2. View All Bills")
    print("3. Search Bills by Patient ID")
    print("4. Record Payment")
    print("5. View Pending Payments")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        generate_bill()
    elif choice == "2":
        view_all_bills()
    elif choice == "3":
        search_bills_by_patient()
    elif choice == "4":
        record_payment()
    elif choice == "5":
        view_pending_payments()
    elif choice == "0":
        break
    else:
        print("Invalid choice.")