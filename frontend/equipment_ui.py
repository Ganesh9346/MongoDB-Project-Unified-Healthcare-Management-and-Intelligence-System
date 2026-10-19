import streamlit as st
import pandas as pd
from frontend.database_ui import get_collection


def show_equipment_page():
    st.title("🏥 Equipment Management")
    st.write("View and manage hospital medical equipment.")

    equipment_collection = get_collection("equipment")

    # Register equipment
    st.subheader("Register New Equipment")

    with st.form("equipment_form"):
        equipment_id = st.text_input("Equipment ID")
        equipment_name = st.text_input("Equipment Name")

        category = st.selectbox(
            "Equipment Category",
            [
                "Diagnostic",
                "Monitoring",
                "Life Support",
                "Surgical",
                "Other"
            ]
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            step=1
        )

        condition = st.selectbox(
            "Equipment Condition",
            ["Good", "Under Maintenance", "Damaged"]
        )

        location = st.text_input("Equipment Location")

        submitted = st.form_submit_button("Register Equipment")

        if submitted:
            if not equipment_id.strip() or not equipment_name.strip():
                st.error("Please enter the Equipment ID and Equipment Name.")

            elif equipment_collection.find_one(
                {"equipment_id": equipment_id.strip()}
            ):
                st.error("Equipment ID already exists.")

            else:
                equipment = {
                    "equipment_id": equipment_id.strip(),
                    "equipment_name": equipment_name.strip(),
                    "category": category,
                    "quantity": quantity,
                    "condition": condition,
                    "location": location.strip()
                }

                equipment_collection.insert_one(equipment)

                st.success("Equipment registered successfully!")
                st.rerun()

    # Display equipment
    st.divider()
    st.subheader("Equipment Inventory")

    records = list(
        equipment_collection.find({}, {"_id": 0})
    )

    if records:
        st.dataframe(
            pd.DataFrame(records),
            use_container_width=True
        )
    else:
        st.info("No equipment records found.")