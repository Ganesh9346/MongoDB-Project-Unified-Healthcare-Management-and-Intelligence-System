import streamlit as st
from frontend.database_ui import get_collection
from datetime import date, datetime


def show_billing_page():
    st.title("💳 Billing Management")
    st.write("Create and view hospital bills and payment records.")

    bills = get_collection("bills")
    patients = get_collection("patients")

    # Fetch patients from MongoDB
    patient_list = list(patients.find({}, {"_id": 0}))

    # Create a bill
    with st.expander("➕ Create New Bill", expanded=True):

        with st.form("billing_form"):

            # Patient selection
            patient_options = {
                f"{p.get('name', 'Unknown')} ({p.get('patient_id', 'No ID')})":
                p.get("patient_id")
                for p in patient_list
                if p.get("patient_id") is not None
            }

            if patient_options:
                patient_choice = st.selectbox(
                    "Select Patient",
                    options=list(patient_options.keys())
                )
            else:
                patient_choice = None
                st.warning(
                    "No patients found. Register a patient first."
                )

            bill_id = st.text_input("Bill ID *")

            bill_date = st.date_input(
                "Bill Date",
                value=date.today()
            )

            # Charges
            col1, col2 = st.columns(2)

            with col1:
                consultation_fee = st.number_input(
                    "Consultation Fee (₹)",
                    min_value=0.0,
                    value=0.0,
                    step=100.0
                )

                laboratory_charges = st.number_input(
                    "Laboratory Charges (₹)",
                    min_value=0.0,
                    value=0.0,
                    step=50.0
                )

                bed_charges = st.number_input(
                    "Bed Charges (₹)",
                    min_value=0.0,
                    value=0.0,
                    step=100.0
                )

            with col2:
                medicine_charges = st.number_input(
                    "Medicine Charges (₹)",
                    min_value=0.0,
                    value=0.0,
                    step=50.0
                )

                other_charges = st.number_input(
                    "Other Charges (₹)",
                    min_value=0.0,
                    value=0.0,
                    step=50.0
                )

                paid_amount = st.number_input(
                    "Amount Paid (₹)",
                    min_value=0.0,
                    value=0.0,
                    step=100.0
                )

            # Calculate total bill
            total_amount = (
                consultation_fee
                + medicine_charges
                + laboratory_charges
                + bed_charges
                + other_charges
            )

            # Calculate outstanding balance
            balance = total_amount - paid_amount

            st.metric(
                "Total Bill Amount",
                f"₹{total_amount:,.2f}"
            )

            st.metric(
                "Outstanding Balance",
                f"₹{balance:,.2f}"
            )

            # Payment status
            payment_status = st.selectbox(
                "Payment Status",
                ["Pending", "Partially Paid", "Paid"]
            )

            submitted = st.form_submit_button("Create Bill")

            if submitted:

                if not patient_options:
                    st.error(
                        "Register a patient before creating a bill."
                    )

                elif not bill_id.strip():
                    st.error("Bill ID is required.")

                elif bills.find_one(
                    {"bill_id": bill_id.strip()}
                ):
                    st.error("This Bill ID already exists.")

                elif paid_amount > total_amount:
                    st.error(
                        "Amount paid cannot exceed the total bill amount."
                    )

                else:
                    try:
                        # Retrieve selected patient details
                        patient_id = patient_options[patient_choice]

                        selected_patient = next(
                            (
                                p for p in patient_list
                                if p.get("patient_id") == patient_id
                            ),
                            None
                        )

                        if selected_patient is None:
                            st.error("Selected patient could not be found.")

                        else:
                            patient_name = selected_patient.get(
                                "name", "Unknown"
                            )

                            # Determine payment status from amounts
                            if paid_amount == 0:
                                actual_payment_status = "Pending"

                            elif paid_amount < total_amount:
                                actual_payment_status = "Partially Paid"

                            else:
                                actual_payment_status = "Paid"

                            # Build bill document
                            bill = {
                                "bill_id": bill_id.strip(),
                                "patient_id": patient_id,
                                "patient_name": patient_name,
                                "bill_date": str(bill_date),
                                "consultation_fee": float(
                                    consultation_fee
                                ),
                                "medicine_charges": float(
                                    medicine_charges
                                ),
                                "laboratory_charges": float(
                                    laboratory_charges
                                ),
                                "bed_charges": float(bed_charges),
                                "total_amount": float(total_amount),
                                "paid_amount": float(paid_amount),
                                "balance": float(balance),
                                "payment_status": actual_payment_status,
                                "created_at": datetime.now()
                            }

                            # Insert into MongoDB
                            bills.insert_one(bill)

                            st.success("Bill created successfully!")

                            st.rerun()

                    except Exception as e:
                        st.error(f"Unable to create bill: {e}")

    # Display billing records
    st.divider()

    st.subheader("📋 Billing Records")

    try:
        records = list(
            bills.find({}, {"_id": 0})
        )

        if records:

            st.dataframe(
                records,
                use_container_width=True,
                hide_index=True
            )

            total_billed = sum(
                float(record.get("total_amount", 0))
                for record in records
            )

            total_paid = sum(
                float(record.get("paid_amount", 0))
                for record in records
            )

            total_balance = sum(
                float(record.get("balance", 0))
                for record in records
            )

            # Summary metrics
            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Billed",
                f"₹{total_billed:,.2f}"
            )

            col2.metric(
                "Total Collected",
                f"₹{total_paid:,.2f}"
            )

            col3.metric(
                "Outstanding Balance",
                f"₹{total_balance:,.2f}"
            )

            st.caption(f"Total bills: {len(records)}")

        else:
            st.info("No billing records found.")

    except Exception as e:
        st.error(f"Unable to retrieve billing records: {e}")