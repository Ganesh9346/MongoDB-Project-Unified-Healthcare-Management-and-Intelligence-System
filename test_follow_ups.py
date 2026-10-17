from modules.follow_ups import (
    schedule_follow_up,
    view_all_follow_ups,
    search_follow_ups_by_patient,
    update_follow_up_status
)

while True:
    print("\n===== Patient Follow-Up Management =====")
    print("1. Schedule Follow-Up")
    print("2. View All Follow-Ups")
    print("3. Search by Patient ID")
    print("4. Update Follow-Up Status")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

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