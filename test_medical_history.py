from modules.medical_history import (
    add_medical_history,
    view_all_medical_history,
    view_patient_history
)


while True:
    print("\n===== MEDICORE: MEDICAL HISTORY =====")
    print("1. Add Medical History")
    print("2. View All Medical History")
    print("3. View History by Patient ID")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        add_medical_history()

    elif choice == "2":
        view_all_medical_history()

    elif choice == "3":
        view_patient_history()

    elif choice == "0":
        print("Exiting Medical History Management.")
        break

    else:
        print("Invalid choice. Try again.")