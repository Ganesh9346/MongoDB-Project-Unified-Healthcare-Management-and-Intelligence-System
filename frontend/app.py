import streamlit as st
from frontend.database_ui import get_dashboard_counts
from frontend.patients_ui import show_patients_page
from frontend.doctors_ui import show_doctors_page
from frontend.appointments_ui import show_appointments_page
from frontend.medical_history_ui import show_medical_history_page
from frontend.pharmacy_ui import show_pharmacy_page
from frontend.laboratory_ui import show_laboratory_page
from frontend.admissions_ui import show_admissions_page
from frontend.emergency_ui import show_emergency_page
from frontend.billing_ui import show_billing_page
from frontend.follow_ups_ui import show_follow_ups_page
from frontend.equipment_ui import show_equipment_page
from frontend.blood_bank_ui import show_blood_bank_page
from frontend.analytics_ui import show_analytics_page
# Page configuration
st.set_page_config(
    page_title="MediCore | Healthcare Management",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #167D9A;
    }

    .subtitle {
        font-size: 16px;
        color: #64748b;
    }

    div[data-testid="stMetric"] {
        background-color: #f0f7fa;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #d9e9ef;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🏥 MediCore")
st.sidebar.caption("Healthcare Management System")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Patients",
        "Doctors",
        "Appointments",
        "Medical History",
        "Pharmacy",
        "Laboratory",
        "Admissions",
        "Emergency",
        "Billing",
        "Follow-ups",
        "Equipment",
        "Blood Bank",
        "Analytics"
    ]
)

st.sidebar.divider()
st.sidebar.info("Unified Healthcare Management System")

# Dashboard
if page == "Dashboard":
    st.markdown(
        '<div class="main-title">MediCore Dashboard</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Healthcare Management and Intelligence System</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("Welcome to MediCore 👋")
    st.write(
        "Manage hospital information through a centralized interface. "
        "Use the sidebar to navigate between healthcare modules."
    )

    try:
        counts = get_dashboard_counts()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Patients", counts["Patients"])
        col2.metric("Doctors", counts["Doctors"])
        col3.metric("Appointments", counts["Appointments"])
        col4.metric("Medicines", counts["Medicines"])

    except Exception as e:
        st.error(f"Unable to load dashboard data: {e}")
    

    st.divider()

    st.subheader("Healthcare Management Modules")

    modules = [
        ("🧑‍⚕️", "Patients", "Register and manage patient records."),
        ("👨‍⚕️", "Doctors", "Manage doctor information."),
        ("📅", "Appointments", "Manage patient appointments."),
        ("📋", "Medical History", "Maintain medical history records."),
        ("💊", "Pharmacy", "Manage medicine inventory."),
        ("🧪", "Laboratory", "Manage laboratory tests."),
        ("🛏️", "Admissions", "Manage hospital admissions."),
        ("🚨", "Emergency", "Manage emergency visits."),
        ("💳", "Billing", "Manage bills and payments."),
        ("🔔", "Follow-ups", "Manage patient follow-ups."),
        ("🩺", "Equipment", "Manage medical equipment."),
        ("🩸", "Blood Bank", "Manage blood bank inventory."),
        ("📊", "Analytics", "View hospital reports.")
    ]

    for start in range(0, len(modules), 3):
        columns = st.columns(3)

        for column, module in zip(columns, modules[start:start + 3]):
            with column:
                with st.container(border=True):
                    st.markdown(f"### {module[0]} {module[1]}")
                    st.write(module[2])

# Placeholder pages
elif page == "Patients":
    show_patients_page()

elif page == "Doctors":
    show_doctors_page()

elif page == "Appointments":
    show_appointments_page()

elif page == "Medical History":
    show_medical_history_page()
elif page == "Pharmacy":
    show_pharmacy_page()
elif page == "Laboratory":
    show_laboratory_page()

elif page == "Admissions":
    show_admissions_page()

elif page == "Emergency":
    show_emergency_page()

elif page == "Billing":
    show_billing_page()

elif page == "Follow-ups":
    show_follow_ups_page()

elif page == "Equipment":
    show_equipment_page()

elif page == "Blood Bank":
    show_blood_bank_page()

elif page == "Analytics":
    show_analytics_page()

else:
    st.title(page)
    st.info(f"The {page} interface will be developed next.")