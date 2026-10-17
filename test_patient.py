from modules.patients import (
    register_patient,
    view_all_patients,
    search_patient,
    update_patient,
    delete_patient
)

while True:
    print("\n===== MEDICORE: PATIENT MANAGEMENT =====")
    print("1. Register Patient")
    print("2. View All Patients")
    print("3. Search Patient")
    print("4. Update Patient")
    print("5. Delete Patient")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        register_patient()

    elif choice == "2":
        view_all_patients()

    elif choice == "3":
        search_patient()

    elif choice == "4":
        update_patient()

    elif choice == "5":
        delete_patient()

    elif choice == "0":
        print("Exiting Patient Management.")
        break

    else:
        print("Invalid choice. Try again.")