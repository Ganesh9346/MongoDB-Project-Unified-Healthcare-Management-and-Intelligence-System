from modules.patients import (
    register_patient,
    view_all_patients,
    search_patient,
    update_patient,
    delete_patient
)

from modules.doctors import (
    register_doctor,
    view_all_doctors,
    search_doctor,
    update_doctor,
    delete_doctor
)

from modules.appointments import (
    book_appointment,
    view_all_appointments,
    search_appointment,
    cancel_appointment
)

from modules.medical_history import (
    add_medical_history,
    view_all_medical_history,
    view_patient_history
)

from modules.pharmacy import (
    add_medicine,
    view_all_medicines,
    search_medicine,
    update_medicine_stock,
    view_low_stock_medicines,
    delete_medicine
)

from modules.laboratory import (
    register_lab_test,
    view_all_lab_tests,
    search_lab_tests_by_patient,
    record_lab_result,
    update_lab_test_status
)

from modules.admissions import (
    add_bed,
    view_all_beds,
    view_available_beds,
    admit_patient,
    view_admitted_patients,
    discharge_patient
)

from modules.emergency import (
    register_emergency_visit,
    view_all_emergency_visits,
    search_emergency_visits,
    update_emergency_status
)

from modules.billing import (
    generate_bill,
    view_all_bills,
    search_bills_by_patient,
    record_payment,
    view_pending_payments
)

from modules.follow_ups import (
    schedule_follow_up,
    view_all_follow_ups,
    search_follow_ups_by_patient,
    update_follow_up_status
)

from modules.equipment import (
    add_equipment,
    view_all_equipment,
    search_equipment,
    update_equipment_status
)

from modules.blood_bank import (
    add_blood_stock,
    view_blood_stock,
    search_blood_stock,
    update_blood_stock,
    view_low_blood_stock
)

from modules.analytics import (
    hospital_overview,
    appointment_report,
    pharmacy_report,
    billing_report,
    emergency_report,
    bed_availability_report
)


def patient_menu():
    while True:
        print("\n--- Patient Management ---")
        print("1. Register Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ").strip()

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
            break
        else:
            print("Invalid choice.")


def doctor_appointment_menu():
    while True:
        print("\n--- Doctor and Appointment Management ---")
        print("1. Register Doctor")
        print("2. View Doctors")
        print("3. Search Doctor")
        print("4. Update Doctor")
        print("5. Delete Doctor")
        print("6. Book Appointment")
        print("7. View Appointments")
        print("8. Search Appointment")
        print("9. Cancel Appointment")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ").strip()

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
        elif choice == "6":
            book_appointment()
        elif choice == "7":
            view_all_appointments()
        elif choice == "8":
            search_appointment()
        elif choice == "9":
            cancel_appointment()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def medical_history_menu():
    while True:
        print("\n--- Medical History Management ---")
        print("1. Add Medical History")
        print("2. View All Medical History")
        print("3. Search Patient Medical History")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_medical_history()
        elif choice == "2":
            view_all_medical_history()
        elif choice == "3":
            view_patient_history()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def pharmacy_menu():
    while True:
        print("\n--- Pharmacy and Medicine Inventory ---")
        print("1. Add Medicine")
        print("2. View Medicines")
        print("3. Search Medicine")
        print("4. Update Medicine Stock")
        print("5. View Low Stock")
        print("6. Delete Medicine")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_medicine()
        elif choice == "2":
            view_all_medicines()
        elif choice == "3":
            search_medicine()
        elif choice == "4":
            update_medicine_stock()
        elif choice == "5":
            view_low_stock_medicines()
        elif choice == "6":
            delete_medicine()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def laboratory_menu():
    while True:
        print("\n--- Laboratory Management ---")
        print("1. Register Lab Test")
        print("2. View All Lab Tests")
        print("3. Search Tests by Patient ID")
        print("4. Record Lab Result")
        print("5. Update Lab Test Status")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            register_lab_test()
        elif choice == "2":
            view_all_lab_tests()
        elif choice == "3":
            search_lab_tests_by_patient()
        elif choice == "4":
            record_lab_result()
        elif choice == "5":
            update_lab_test_status()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def admission_menu():
    while True:
        print("\n--- Bed and Admission Management ---")
        print("1. Add Bed")
        print("2. View All Beds")
        print("3. View Available Beds")
        print("4. Admit Patient")
        print("5. View Admitted Patients")
        print("6. Discharge Patient")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ").strip()

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
            break
        else:
            print("Invalid choice.")


def emergency_menu():
    while True:
        print("\n--- Emergency Visit Management ---")
        print("1. Register Emergency Visit")
        print("2. View All Emergency Visits")
        print("3. Search by Patient ID")
        print("4. Update Emergency Status")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            register_emergency_visit()
        elif choice == "2":
            view_all_emergency_visits()
        elif choice == "3":
            search_emergency_visits()
        elif choice == "4":
            update_emergency_status()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def billing_menu():
    while True:
        print("\n--- Billing and Payments ---")
        print("1. Generate Bill")
        print("2. View All Bills")
        print("3. Search Bills by Patient ID")
        print("4. Record Payment")
        print("5. View Pending Payments")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ").strip()

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


def follow_up_menu():
    while True:
        print("\n--- Patient Follow-Up Management ---")
        print("1. Schedule Follow-Up")
        print("2. View All Follow-Ups")
        print("3. Search by Patient ID")
        print("4. Update Follow-Up Status")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            schedule_follow_up()
        elif choice == "2":
            view_all_follow_ups()
        elif choice == "3":
            search_follow_ups_by_patient()
        elif choice == "4":
            update_follow_up_status()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def equipment_menu():
    while True:
        print("\n--- Medical Equipment Management ---")
        print("1. Add Equipment")
        print("2. View All Equipment")
        print("3. Search Equipment")
        print("4. Update Equipment Status")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_equipment()
        elif choice == "2":
            view_all_equipment()
        elif choice == "3":
            search_equipment()
        elif choice == "4":
            update_equipment_status()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def blood_bank_menu():
    while True:
        print("\n--- Blood Bank Inventory ---")
        print("1. Add Blood Stock")
        print("2. View Blood Stock")
        print("3. Search Blood Group")
        print("4. Update Blood Stock")
        print("5. View Low Blood Stock")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_blood_stock()
        elif choice == "2":
            view_blood_stock()
        elif choice == "3":
            search_blood_stock()
        elif choice == "4":
            update_blood_stock()
        elif choice == "5":
            view_low_blood_stock()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def analytics_menu():
    while True:
        print("\n--- Hospital Analytics and Reports ---")
        print("1. Hospital Overview")
        print("2. Appointment Report")
        print("3. Pharmacy Report")
        print("4. Billing Report")
        print("5. Emergency Report")
        print("6. Bed Availability Report")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ").strip()

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


def main():
    while True:
        print("\n========================================")
        print(" MEDICORE - HEALTHCARE MANAGEMENT SYSTEM")
        print("========================================")
        print("1. Patient Management")
        print("2. Doctor and Appointment Management")
        print("3. Medical History Management")
        print("4. Pharmacy and Medicine Inventory")
        print("5. Laboratory Management")
        print("6. Bed and Admission Management")
        print("7. Emergency Visit Management")
        print("8. Billing and Payments")
        print("9. Patient Follow-Up Management")
        print("10. Medical Equipment Management")
        print("11. Blood Bank Inventory")
        print("12. Hospital Analytics and Reports")
        print("0. Exit")

        choice = input("Select a module: ").strip()

        if choice == "1":
            patient_menu()
        elif choice == "2":
            doctor_appointment_menu()
        elif choice == "3":
            medical_history_menu()
        elif choice == "4":
            pharmacy_menu()
        elif choice == "5":
            laboratory_menu()
        elif choice == "6":
            admission_menu()
        elif choice == "7":
            emergency_menu()
        elif choice == "8":
            billing_menu()
        elif choice == "9":
            follow_up_menu()
        elif choice == "10":
            equipment_menu()
        elif choice == "11":
            blood_bank_menu()
        elif choice == "12":
            analytics_menu()
        elif choice == "0":
            print("Thank you for using MediCore!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()