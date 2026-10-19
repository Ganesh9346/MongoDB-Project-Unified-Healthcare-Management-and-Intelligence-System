import streamlit as st
import pandas as pd
from frontend.database_ui import get_collection


def show_follow_ups_page():
    st.title("📅 Patient Follow-Up Management")
    st.write("Schedule and manage patient follow-up visits.")

    follow_ups = get_collection("follow_ups")
    patients = get_collection("patients")

    # Register a follow-up
    st.subheader("Schedule a Follow-Up")

    patient_records = list(
        patients.find({}, {"patient_id": 1, "name": 1, "_id": 0})
    )

    if not patient_records:
        st.warning("Please register a patient before scheduling a follow-up.")
    else:
        patient_options = {
            f"{p.get('patient_id')} - {p.get('name', 'Unknown')}":
            p.get("patient_id")
            for p in patient_records
        }

        with st.form("follow_up_form"):
            selected_patient = st.selectbox(
                "Select Patient",
                options=list(patient_options.keys())
            )

            follow_up_date = st.date_input("Follow-Up Date")
            purpose = st.text_input("Purpose of Follow-Up")
            status = st.selectbox(
                "Status",
                ["Scheduled", "Completed", "Cancelled"]
            )
            notes = st.text_area("Notes")

            submitted = st.form_submit_button("Schedule Follow-Up")

            if submitted:
                if not purpose.strip():
                    st.error("Please enter the purpose of the follow-up.")
                else:
                    follow_up = {
                        "patient_id": patient_options[selected_patient],
                        "follow_up_date": str(follow_up_date),
                        "purpose": purpose.strip(),
                        "status": status,
                        "notes": notes.strip()
                    }

                    follow_ups.insert_one(follow_up)

                    st.success("Follow-up scheduled successfully!")
                    st.rerun()

    # Display existing follow-ups
    st.divider()
    st.subheader("Existing Follow-Ups")

    records = list(follow_ups.find({}, {"_id": 0}))

    if records:
        st.dataframe(
            pd.DataFrame(records),
            use_container_width=True
        )
    else:
        st.info("No follow-up records found.")