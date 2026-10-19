from config.database import db


def get_collection(collection_name):
    """Return a MongoDB collection for the frontend."""
    return db[collection_name]


def get_dashboard_counts():
    """Get record counts for the dashboard."""

    return {
        "Patients": get_collection("patients").count_documents({}),
        "Doctors": get_collection("doctors").count_documents({}),
        "Appointments": get_collection("appointments").count_documents({}),
        "Medicines": get_collection("medicines").count_documents({})
    }