import streamlit as st
import pandas as pd
import plotly.express as px

from frontend.database_ui import get_collection


def show_analytics_page():
    st.title("📊 Hospital Analytics")
    st.write("Analyze hospital records and operational statistics.")

    # Refresh analytics
    if st.button("Refresh Analytics"):
        st.rerun()

    st.divider()

    # Collection counts
    collection_names = {
        "Patients": "patients",
        "Doctors": "doctors",
        "Appointments": "appointments",
        "Medical History": "medical_history",
        "Medicines": "medicines",
        "Laboratory Tests": "lab_tests",
        "Admissions": "admissions",
        "Emergency Visits": "emergency_visits",
        "Bills": "bills",
        "Follow-Ups": "follow_ups",
        "Equipment": "equipment",
        "Blood Bank": "blood_bank"
    }

    st.subheader("Hospital Records")

    columns = st.columns(3)

    for index, (label, collection_name) in enumerate(
        collection_names.items()
    ):
        try:
            count = get_collection(
                collection_name
            ).count_documents({})

            with columns[index % 3]:
                st.metric(label, count)

        except Exception:
            with columns[index % 3]:
                st.metric(label, "Unavailable")

    st.divider()

    # Patient blood group chart
    st.subheader("Patient Blood Group Distribution")

    try:
        patients = list(
            get_collection("patients").find(
                {},
                {"_id": 0, "blood_group": 1}
            )
        )

        blood_groups = [
            patient.get("blood_group")
            for patient in patients
            if patient.get("blood_group")
        ]

        if blood_groups:
            df_blood = pd.DataFrame({
                "Blood Group": blood_groups
            })

            blood_counts = (
                df_blood["Blood Group"]
                .value_counts()
                .rename_axis("Blood Group")
                .reset_index(name="Patients")
            )

            fig = px.bar(
                blood_counts,
                x="Blood Group",
                y="Patients",
                title="Patients by Blood Group"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info(
                "No patient blood group data is available yet."
            )

    except Exception as error:
        st.warning(f"Could not load blood group chart: {error}")

    st.divider()

    # Appointment status chart
    st.subheader("Appointment Status Distribution")

    try:
        appointments = list(
            get_collection("appointments").find(
                {},
                {"_id": 0, "status": 1}
            )
        )

        statuses = [
            appointment.get("status")
            for appointment in appointments
            if appointment.get("status")
        ]

        if statuses:
            df_status = pd.DataFrame({
                "Status": statuses
            })

            status_counts = (
                df_status["Status"]
                .value_counts()
                .rename_axis("Status")
                .reset_index(name="Appointments")
            )

            fig = px.pie(
                status_counts,
                names="Status",
                values="Appointments",
                title="Appointments by Status"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info(
                "No appointment status data is available yet."
            )

    except Exception as error:
        st.warning(f"Could not load appointment chart: {error}")

    st.divider()

    # Recent appointments
    st.subheader("Recent Appointments")

    try:
        recent_appointments = list(
            get_collection("appointments").find(
                {},
                {"_id": 0}
            ).limit(10)
        )

        if recent_appointments:
            st.dataframe(
                pd.DataFrame(recent_appointments),
                use_container_width=True
            )
        else:
            st.info("No appointment records found.")

    except Exception as error:
        st.warning(f"Could not load appointments: {error}")