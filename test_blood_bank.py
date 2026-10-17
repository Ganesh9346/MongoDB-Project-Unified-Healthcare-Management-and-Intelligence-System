from modules.blood_bank import (
    add_blood_stock,
    view_blood_stock,
    search_blood_stock,
    update_blood_stock,
    view_low_blood_stock
)

while True:
    print("\n===== Blood Bank Management =====")
    print("1. Add Blood Stock")
    print("2. View All Blood Stock")
    print("3. Search by Blood Group")
    print("4. Update Blood Stock")
    print("5. View Low Blood Stock")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

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