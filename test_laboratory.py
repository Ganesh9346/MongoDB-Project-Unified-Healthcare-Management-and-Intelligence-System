from modules.laboratory import (
    register_lab_test,
    view_all_lab_tests,
    search_lab_tests_by_patient,
    record_lab_result,
    update_lab_test_status
)


while True:
    print("\n===== MEDICORE: LABORATORY MANAGEMENT =====")
    print("1. Register Laboratory Test")
    print("2. View All Laboratory Tests")
    print("3. Search Tests by Patient ID")
    print("4. Record Test Result")
    print("5. Update Test Status")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

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
        print("Exiting Laboratory Management.")
        break

    else:
        print("Invalid choice. Try again.")