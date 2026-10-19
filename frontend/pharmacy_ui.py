import streamlit as st
from frontend.database_ui import get_collection


def show_pharmacy_page():
    st.title("💊 Pharmacy Management")
    st.write("Manage medicine inventory and view available medicines.")

    medicines = get_collection("medicines")

    # Register medicine
    with st.expander("➕ Add New Medicine", expanded=True):
        with st.form("medicine_form"):
            col1, col2 = st.columns(2)

            with col1:
                medicine_id = st.text_input("Medicine ID *")
                name = st.text_input("Medicine Name *")
                category = st.text_input("Category")

            with col2:
                quantity = st.number_input(
                    "Quantity",
                    min_value=0,
                    value=0
                )
                price = st.number_input(
                    "Price per Unit",
                    min_value=0.0,
                    value=0.0,
                    step=1.0
                )
                expiry_date = st.date_input("Expiry Date")

            submitted = st.form_submit_button("Add Medicine")

            if submitted:
                if not medicine_id.strip() or not name.strip():
                    st.error("Medicine ID and Medicine Name are required.")
                else:
                    try:
                        medicine = {
                            "medicine_id": medicine_id.strip(),
                            "name": name.strip(),
                            "category": category.strip(),
                            "quantity": quantity,
                            "price": price,
                            "expiry_date": str(expiry_date)
                        }

                        medicines.insert_one(medicine)
                        st.success(f"{name} added successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Unable to add medicine: {e}")

    st.divider()

    # Search medicines
    st.subheader("🔍 Search Medicines")
    search_term = st.text_input(
        "Search by medicine ID or name",
        key="medicine_search"
    )

    if search_term.strip():
        query = {
            "$or": [
                {
                    "medicine_id": {
                        "$regex": search_term.strip(),
                        "$options": "i"
                    }
                },
                {
                    "name": {
                        "$regex": search_term.strip(),
                        "$options": "i"
                    }
                }
            ]
        }
    else:
        query = {}

    # Display inventory
    st.subheader("📦 Medicine Inventory")

    try:
        medicine_list = list(
            medicines.find(query, {"_id": 0}).sort("name", 1)
        )

        if medicine_list:
            st.dataframe(
                medicine_list,
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Medicines displayed: {len(medicine_list)}")
        else:
            st.info("No medicines found.")

    except Exception as e:
        st.error(f"Unable to retrieve medicines: {e}")