import streamlit as st
import pandas as pd
from datetime import datetime

from frontend.database_ui import get_collection


def show_blood_bank_page():
    st.title("🩸 Blood Bank Management")
    st.write("Manage blood group inventory and blood bank records.")

    blood_bank = get_collection("blood_bank")

    # Register blood stock
    st.subheader("Register Blood Stock")

    with st.form("blood_bank_form"):

        blood_id = st.text_input("Blood Record ID")

        blood_group = st.selectbox(
            "Blood Group",
            ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        )

        units = st.number_input(
            "Available Units",
            min_value=0,
            step=1
        )

        collection_date = st.date_input("Collection Date")

        expiry_date = st.date_input("Expiry Date")

        status = st.selectbox(
            "Status",
            ["Available", "Reserved", "Expired"]
        )

        submitted = st.form_submit_button("Register Blood Stock")

        if submitted:

            if not blood_id.strip():
                st.error("Please enter a Blood Record ID.")

            elif expiry_date < collection_date:
                st.error(
                    "Expiry date cannot be earlier than collection date."
                )

            elif blood_bank.find_one(
                {"blood_id": blood_id.strip()}
            ):
                st.error("This Blood Record ID already exists.")

            else:
                # Prepare the blood bank record
                record = {
                    "blood_id": blood_id.strip(),
                    "blood_group": blood_group,
                    "units": int(units),
                    "collection_date": str(collection_date),
                    "expiry_date": str(expiry_date),
                    "status": status,
                    "updated_at": datetime.now()
                }

                # Insert the record into MongoDB
                try:
                    blood_bank.insert_one(record)

                    st.success(
                        "Blood stock registered successfully!"
                    )

                    st.rerun()

                except Exception as error:
                    st.error(
                        f"Failed to register blood stock: {error}"
                    )

    # Display blood bank records
    st.divider()
    st.subheader("Blood Bank Inventory")

    try:
        records = list(
            blood_bank.find({}, {"_id": 0})
        )

        if records:
            df = pd.DataFrame(records)

            st.dataframe(
                df,
                use_container_width=True
            )
        else:
            st.info("No blood bank records found.")

    except Exception as error:
        st.error(f"Failed to load blood bank records: {error}")