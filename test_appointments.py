from modules.appointments import (
    book_appointment,
    view_all_appointments,
    search_appointment,
    cancel_appointment
)

while True:
    print("\n===== MEDICORE: APPOINTMENT MANAGEMENT =====")
    print("1. Book Appointment")
    print("2. View All Appointments")
    print("3. Search Appointment")
    print("4. Cancel Appointment")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        book_appointment()

    elif choice == "2":
        view_all_appointments()

    elif choice == "3":
        search_appointment()

    elif choice == "4":
        cancel_appointment()

    elif choice == "0":
        print("Exiting Appointment Management.")
        break

    else:
        print("Invalid choice. Try again.")