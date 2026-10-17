
from modules.doctors import (
    register_doctor,
    view_all_doctors,
    search_doctor,
    update_doctor,
    delete_doctor
)
while True:
    print("\n===== MEDICORE: DOCTOR MANAGEMENT =====")
    print("1. Register Doctor")
    print("2. View All Doctors")
    print("3. Search Doctor")
    print("4. Update Doctor")
    print("5. Delete Doctor")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        register_doctor()

    elif choice == "2":
        view_all_doctors()

    elif choice == "3":
        search_doctor()

    elif choice == "4":
        update_doctor()

    elif choice == "5":
        delete_doctor()
    
    elif choice == "0":
        print("Exiting Doctor Management.")
        break

    else:
        print("Invalid choice. Try again.")