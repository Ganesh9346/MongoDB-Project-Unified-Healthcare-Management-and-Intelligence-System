import streamlit as st
from frontend.database_ui import get_collection


def show_doctors_page():
    st.title("👨‍⚕️ Doctors Management")
    st.write("Register and view hospital doctors.")

    doctors = get_collection("doctors")

    # Register doctor
    with st.expander("➕ Register New Doctor", expanded=True):
        with st.form("doctor_registration_form"):
            col1, col2 = st.columns(2)

            with col1:
                doctor_id = st.text_input("Doctor ID *")
                name = st.text_input("Doctor Name *")
                specialization = st.text_input("Specialization *")

            with col2:
                phone = st.text_input("Phone Number")
                email = st.text_input("Email")
                experience = st.number_input(
                    "Experience (years)",
                    min_value=0,
                    max_value=70,
                    value=0
                )

            submitted = st.form_submit_button("Register Doctor")

            if submitted:
                if not doctor_id.strip() or not name.strip() or not specialization.strip():
                    st.error("Doctor ID, Doctor Name, and Specialization are required.")
                else:
                    try:
                        doctor = {
                            "doctor_id": doctor_id.strip(),
                            "name": name.strip(),
                            "specialization": specialization.strip(),
                            "phone": phone.strip(),
                            "email": email.strip(),
                            "experience": experience
                        }

                        doctors.insert_one(doctor)
                        st.success(f"Doctor {name} registered successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Unable to register doctor: {e}")

    st.divider()

    # View and search doctors
    st.subheader("🔍 Search Doctors")
    search_term = st.text_input(
        "Search by doctor ID, name, or specialization"
    )

    if search_term.strip():
        query = {
            "$or": [
                {"doctor_id": {"$regex": search_term.strip(), "$options": "i"}},
                {"name": {"$regex": search_term.strip(), "$options": "i"}},
                {"specialization": {"$regex": search_term.strip(), "$options": "i"}}
            ]
        }
    else:
        query = {}

    st.subheader("📋 Doctor Records")

    try:
        doctor_list = list(
            doctors.find(query, {"_id": 0}).sort("name", 1)
        )

        if doctor_list:
            st.dataframe(
                doctor_list,
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Total doctors displayed: {len(doctor_list)}")
        else:
            st.info("No doctor records found.")

    except Exception as e:
        st.error(f"Unable to retrieve doctor records: {e}")