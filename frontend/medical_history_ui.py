import streamlit as st
from frontend.database_ui import get_collection


def show_medical_history_page():
    st.title("📋 Medical History Management")
    st.write("Record and view patients' medical history.")

    history_collection = get_collection("medical_history")
    patients = get_collection("patients")

    patient_list = list(patients.find({}, {"_id": 0}))

    if not patient_list:
        st.warning("Register a patient before adding medical history.")
        return

    patient_options = {
        f"{p.get('name', 'Unknown')} ({p.get('patient_id', 'No ID')})":
        p.get("patient_id")
        for p in patient_list
    }

    with st.expander("➕ Add Medical History", expanded=True):
        with st.form("medical_history_form"):
            patient_choice = st.selectbox(
                "Select Patient",
                list(patient_options.keys())
            )

            history_id = st.text_input("History ID *")
            diagnosis = st.text_input("Diagnosis *")
            symptoms = st.text_area("Symptoms")
            treatment = st.text_area("Treatment")
            notes = st.text_area("Additional Notes")

            submitted = st.form_submit_button("Save Medical History")

            if submitted:
                if not history_id.strip() or not diagnosis.strip():
                    st.error("History ID and Diagnosis are required.")
                else:
                    try:
                        history = {
                            "history_id": history_id.strip(),
                            "patient_id": patient_options[patient_choice],
                            "diagnosis": diagnosis.strip(),
                            "symptoms": symptoms.strip(),
                            "treatment": treatment.strip(),
                            "notes": notes.strip()
                        }

                        history_collection.insert_one(history)

                        st.success("Medical history saved successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Unable to save medical history: {e}")

    st.divider()
    st.subheader("📚 Medical History Records")

    try:
        records = list(
            history_collection.find({}, {"_id": 0})
        )

        if records:
            st.dataframe(
                records,
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Total records: {len(records)}")
        else:
            st.info("No medical history records found.")

    except Exception as e:
        st.error(f"Unable to retrieve medical history: {e}")