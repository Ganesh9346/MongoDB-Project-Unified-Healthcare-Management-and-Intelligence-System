from modules.admissions import (
    add_bed,
    view_all_beds,
    view_available_beds,
    admit_patient,
    view_admitted_patients,
    discharge_patient
)


while True:
    print("\n===== MEDICORE: BED AND ADMISSION MANAGEMENT =====")
    print("1. Add Bed")
    print("2. View All Beds")
    print("3. View Available Beds")
    print("4. Admit Patient")
    print("5. View Admitted Patients")
    print("6. Discharge Patient")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        add_bed()

    elif choice == "2":
        view_all_beds()

    elif choice == "3":
        view_available_beds()

    elif choice == "4":
        admit_patient()

    elif choice == "5":
        view_admitted_patients()

    elif choice == "6":
        discharge_patient()

    elif choice == "0":
        print("Exiting Bed and Admission Management.")
        break

    else:
        print("Invalid choice. Try again.")