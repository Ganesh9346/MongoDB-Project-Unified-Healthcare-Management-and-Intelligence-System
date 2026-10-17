from modules.equipment import (
    add_equipment,
    view_all_equipment,
    search_equipment,
    update_equipment_status
)

while True:
    print("\n===== Medical Equipment Management =====")
    print("1. Add Equipment")
    print("2. View All Equipment")
    print("3. Search Equipment")
    print("4. Update Equipment Status")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

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