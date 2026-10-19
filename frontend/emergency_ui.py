import streamlit as st
from frontend.database_ui import get_collection


def show_emergency_page():
    st.title("🚨 Emergency Management")
    st.write("Register and monitor hospital emergency visits.")

    emergency_collection = get_collection("emergency_visits")
    patients = get_collection("patients")

    patient_list = list(patients.find({}, {"_id": 0}))

    with st.expander("➕ Register Emergency Visit", expanded=True):
        with st.form("emergency_form"):
            patient_options = {
                f"{p.get('name', 'Unknown')} ({p.get('patient_id', 'No ID')})":
                p.get("patient_id")
                for p in patient_list
            }

            patient_options["Unknown / Unregistered Patient"] = None

            patient_choice = st.selectbox(
                "Select Patient",
                list(patient_options.keys())
            )

            emergency_id = st.text_input("Emergency ID *")
            emergency_date = st.date_input("Visit Date")

            severity = st.selectbox(
                "Severity",
                ["Low", "Medium", "High", "Critical"]
            )

            symptoms = st.text_area("Symptoms")
            treatment = st.text_area("Treatment Provided")

            status = st.selectbox(
                "Visit Status",
                ["Under Treatment", "Admitted", "Discharged"]
            )

            submitted = st.form_submit_button("Register Emergency Visit")

            if submitted:
                if not emergency_id.strip():
                    st.error("Emergency ID is required.")
                else:
                    try:
                        emergency = {
                            "emergency_id": emergency_id.strip(),
                            "patient_id": patient_options[patient_choice],
                            "visit_date": str(emergency_date),
                            "severity": severity,
                            "symptoms": symptoms.strip(),
                            "treatment": treatment.strip(),
                            "status": status
                        }

                        emergency_collection.insert_one(emergency)

                        st.success("Emergency visit registered successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Unable to register emergency visit: {e}")

    st.divider()
    st.subheader("📋 Emergency Visit Records")

    try:
        records = list(
            emergency_collection.find({}, {"_id": 0})
        )

        if records:
            st.dataframe(
                records,
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Total emergency visits: {len(records)}")
        else:
            st.info("No emergency visits found.")

    except Exception as e:
        st.error(f"Unable to retrieve emergency records: {e}")