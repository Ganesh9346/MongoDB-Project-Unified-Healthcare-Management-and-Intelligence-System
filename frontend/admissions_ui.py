import streamlit as st
from frontend.database_ui import get_collection


def show_admissions_page():
    st.title("🏥 Admissions Management")
    st.write("Register and view patient hospital admissions.")

    admissions = get_collection("admissions")
    patients = get_collection("patients")

    patient_list = list(patients.find({}, {"_id": 0}))

    if not patient_list:
        st.warning("Register a patient before creating an admission.")
        return

    patient_options = {
        f"{p.get('name', 'Unknown')} ({p.get('patient_id', 'No ID')})":
        p.get("patient_id")
        for p in patient_list
    }

    with st.expander("➕ Register Admission", expanded=True):
        with st.form("admission_form"):
            patient_choice = st.selectbox(
                "Select Patient",
                list(patient_options.keys())
            )

            admission_id = st.text_input("Admission ID *")
            admission_date = st.date_input("Admission Date")
            reason = st.text_area("Reason for Admission")
            ward = st.text_input("Ward")
            status = st.selectbox(
                "Admission Status",
                ["Admitted", "Discharged"]
            )

            submitted = st.form_submit_button("Save Admission")

            if submitted:
                if not admission_id.strip():
                    st.error("Admission ID is required.")
                else:
                    try:
                        admission = {
                            "admission_id": admission_id.strip(),
                            "patient_id": patient_options[patient_choice],
                            "admission_date": str(admission_date),
                            "reason": reason.strip(),
                            "ward": ward.strip(),
                            "status": status
                        }

                        admissions.insert_one(admission)

                        st.success("Admission registered successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Unable to register admission: {e}")

    st.divider()
    st.subheader("📋 Admission Records")

    try:
        records = list(
            admissions.find({}, {"_id": 0})
        )

        if records:
            st.dataframe(
                records,
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Total admissions: {len(records)}")
        else:
            st.info("No admission records found.")

    except Exception as e:
        st.error(f"Unable to retrieve admissions: {e}")