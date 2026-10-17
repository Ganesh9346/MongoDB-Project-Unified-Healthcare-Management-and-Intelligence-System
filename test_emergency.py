from modules.emergency import (
    register_emergency_visit,
    view_all_emergency_visits,
    search_emergency_visits,
    update_emergency_status
)

while True:
    print("\n===== Emergency Visit Management =====")
    print("1. Register Emergency Visit")
    print("2. View All Emergency Visits")
    print("3. Search Visits by Patient ID")
    print("4. Update Emergency Status")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

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