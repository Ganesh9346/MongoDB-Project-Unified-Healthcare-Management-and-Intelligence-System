from modules.pharmacy import (
    add_medicine,
    view_all_medicines,
    search_medicine,
    update_medicine_stock,
    view_low_stock_medicines,
    delete_medicine
)


while True:
    print("\n===== MEDICORE: PHARMACY MANAGEMENT =====")
    print("1. Add Medicine")
    print("2. View All Medicines")
    print("3. Search Medicine")
    print("4. Update Medicine Stock")
    print("5. View Low-Stock Medicines")
    print("6. Delete Medicine")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

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
        print("Exiting Pharmacy Management.")
        break

    else:
        print("Invalid choice. Try again.")