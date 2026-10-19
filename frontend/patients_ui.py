import streamlit as st
from frontend.database_ui import get_collection
from datetime import datetime


def show_patients_page():
    st.title("🧑‍⚕️ Patient Management")
    st.write("Register, view, search, and manage patient records.")

    patients = get_collection("patients")

    # Registration form
    with st.expander("➕ Register New Patient", expanded=True):
        with st.form("patient_registration_form"):
            col1, col2 = st.columns(2)

            with col1:
                patient_id = st.text_input("Patient ID *")
                name = st.text_input("Full Name *")
                age = st.number_input("Age", min_value=0, max_value=120, value=18)
                gender = st.selectbox(
                    "Gender",
                    ["Male", "Female", "Other"]
                )

            with col2:
                phone = st.text_input("Phone Number")
                email = st.text_input("Email")
                blood_group = st.selectbox(
                    "Blood Group",
                    ["Unknown", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
                )

            address = st.text_area("Address")

            submitted = st.form_submit_button("Register Patient")

            if submitted:
                if not patient_id.strip() or not name.strip():
                    st.error("Patient ID and Full Name are required.")
                else:
                    try:
                        patient = {
                            "patient_id": patient_id.strip(),
                            "name": name.strip(),
                            "age": age,
                            "gender": gender,
                            "phone": phone.strip(),
                            "email": email.strip(),
                            "blood_group": blood_group,
                            "address": address.strip(),
                            "created_at": datetime.now()
                        }

                        patients.insert_one(patient)
                        st.success(f"Patient {name} registered successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Unable to register patient: {e}")

    st.divider()

    # Search patients
    st.subheader("🔍 Search Patients")
    search_term = st.text_input(
        "Search by patient ID or name",
        key="patient_search"
    )

    if search_term.strip():
        query = {
            "$or": [
                {"patient_id": {"$regex": search_term.strip(), "$options": "i"}},
                {"name": {"$regex": search_term.strip(), "$options": "i"}}
            ]
        }
    else:
        query = {}

    # Display patients
    st.subheader("📋 Patient Records")

    try:
        patient_list = list(
            patients.find(query, {"_id": 0}).sort("name", 1)
        )

        if patient_list:
            st.dataframe(
                patient_list,
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Total records displayed: {len(patient_list)}")
        else:
            st.info("No patient records found.")

    except Exception as e:
        st.error(f"Unable to retrieve patient records: {e}")