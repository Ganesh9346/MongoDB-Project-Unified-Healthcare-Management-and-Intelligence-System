import streamlit as st
from frontend.database_ui import get_collection


def show_appointments_page():
    st.title("📅 Appointments Management")
    st.write("Schedule and view patient appointments.")

    appointments = get_collection("appointments")
    patients = get_collection("patients")
    doctors = get_collection("doctors")

    # Fetch existing patients and doctors
    patient_list = list(patients.find({}, {"_id": 0}))
    doctor_list = list(doctors.find({}, {"_id": 0}))

    if not patient_list:
        st.warning("Register a patient before scheduling an appointment.")
        return

    if not doctor_list:
        st.warning("Register a doctor before scheduling an appointment.")
        return

    with st.expander("➕ Schedule Appointment", expanded=True):
        with st.form("appointment_form"):
            patient_options = {
                f"{p.get('name', 'Unknown')} ({p.get('patient_id', 'No ID')})":
                p.get("patient_id")
                for p in patient_list
            }

            doctor_options = {
                f"{d.get('name', 'Unknown')} ({d.get('doctor_id', 'No ID')})":
                d.get("doctor_id")
                for d in doctor_list
            }

            patient_choice = st.selectbox(
                "Select Patient",
                list(patient_options.keys())
            )

            doctor_choice = st.selectbox(
                "Select Doctor",
                list(doctor_options.keys())
            )

            col1, col2 = st.columns(2)

            with col1:
                appointment_id = st.text_input("Appointment ID *")
                appointment_date = st.date_input("Appointment Date")

            with col2:
                appointment_time = st.time_input("Appointment Time")
                status = st.selectbox(
                    "Status",
                    ["Scheduled", "Completed", "Cancelled"]
                )

            reason = st.text_area("Reason for Appointment")

            submitted = st.form_submit_button("Schedule Appointment")

            if submitted:
                if not appointment_id.strip():
                    st.error("Appointment ID is required.")
                else:
                    try:
                        appointment = {
                            "appointment_id": appointment_id.strip(),
                            "patient_id": patient_options[patient_choice],
                            "doctor_id": doctor_options[doctor_choice],
                            "appointment_date": str(appointment_date),
                            "appointment_time": str(appointment_time),
                            "status": status,
                            "reason": reason.strip()
                        }

                        appointments.insert_one(appointment)

                        st.success("Appointment scheduled successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Unable to schedule appointment: {e}")

    st.divider()

    st.subheader("📋 Appointment Records")

    try:
        appointment_list = list(
            appointments.find({}, {"_id": 0}).sort("appointment_date", -1)
        )

        if appointment_list:
            st.dataframe(
                appointment_list,
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Total appointments: {len(appointment_list)}")
        else:
            st.info("No appointments found.")

    except Exception as e:
        st.error(f"Unable to retrieve appointments: {e}")