import streamlit as st
from frontend.database_ui import get_collection


def show_laboratory_page():
    st.title("🧪 Laboratory Management")
    st.write("Record and view laboratory tests.")

    lab_tests = get_collection("lab_tests")
    patients = get_collection("patients")

    patient_list = list(patients.find({}, {"_id": 0}))

    # Register laboratory test
    with st.expander("➕ Add Laboratory Test", expanded=True):
        with st.form("laboratory_form"):
            patient_options = {
                f"{p.get('name', 'Unknown')} ({p.get('patient_id', 'No ID')})":
                p.get("patient_id")
                for p in patient_list
            }

            if patient_options:
                patient_choice = st.selectbox(
                    "Select Patient",
                    list(patient_options.keys())
                )
            else:
                patient_choice = None
                st.warning("No patients found. Register a patient first.")

            test_id = st.text_input("Test ID *")
            test_name = st.text_input("Test Name *")
            test_date = st.date_input("Test Date")
            result = st.text_area("Test Result")
            status = st.selectbox(
                "Test Status",
                ["Pending", "In Progress", "Completed"]
            )

            submitted = st.form_submit_button("Save Laboratory Test")

            if submitted:
                if not patient_options:
                    st.error("Register a patient before adding a test.")
                elif not test_id.strip() or not test_name.strip():
                    st.error("Test ID and Test Name are required.")
                else:
                    try:
                        test_document = {
                            "test_id": test_id.strip(),
                            "patient_id": patient_options[patient_choice],
                            "test_name": test_name.strip(),
                            "test_date": str(test_date),
                            "result": result.strip(),
                            "status": status
                        }

                        lab_tests.insert_one(test_document)

                        st.success("Laboratory test saved successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Unable to save laboratory test: {e}")

    st.divider()

    # Display laboratory tests
    st.subheader("📋 Laboratory Records")

    try:
        records = list(
            lab_tests.find({}, {"_id": 0}).sort("test_date", -1)
        )

        if records:
            st.dataframe(
                records,
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Total laboratory records: {len(records)}")
        else:
            st.info("No laboratory records found.")

    except Exception as e:
        st.error(f"Unable to retrieve laboratory records: {e}")