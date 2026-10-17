from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select database
db = client["MediCoreDB"]

# Select patients collection
# patients_collection = db["patients"]

# Create patients collection with MongoDB schema validation
# MongoDB Schema Validation for Patients

patient_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "patient_id",
            "name",
            "age",
            "gender",
            "phone",
            "blood_group",
            "address"
        ],
        "properties": {
            "patient_id": {
                "bsonType": "string"
            },
            "name": {
                "bsonType": "string",
                "minLength": 1
            },
            "age": {
                "bsonType": ["int", "long"],
                "minimum": 0,
                "maximum": 130
            },
            "gender": {
                "bsonType": "string",
                "minLength": 1
            },
            "phone": {
                "bsonType": "string",
                "minLength": 1
            },
            "blood_group": {
                "bsonType": "string",
                "minLength": 1
            },
            "address": {
                "bsonType": "string",
                "minLength": 1
            }
        }
    }
}

# Apply validation to an existing collection or create a new one
if "patients" in db.list_collection_names():
    db.command({
        "collMod": "patients",
        "validator": patient_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })
else:
    db.create_collection(
        "patients",
        validator=patient_validator,
        validationLevel="strict",
        validationAction="error"
    )

# Select patients collection
patients_collection = db["patients"]

# Select appointments collection
# MongoDB Schema Validation for Appointments

appointment_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "appointment_id",
            "patient_id",
            "patient_name",
            "doctor_id",
            "doctor_name",
            "appointment_date",
            "appointment_time",
            "reason",
            "status",
            "created_at"
        ],
        "properties": {
            "appointment_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_name": {
                "bsonType": "string",
                "minLength": 1
            },
            "doctor_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "doctor_name": {
                "bsonType": "string",
                "minLength": 1
            },
            "appointment_date": {
                "bsonType": "string",
                "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
            },
            "appointment_time": {
                "bsonType": "string",
                "pattern": "^(?:[01]\\d|2[0-3]):[0-5]\\d$"
            },
            "reason": {
                "bsonType": "string",
                "minLength": 1
            },
            "status": {
                "enum": ["Scheduled", "Cancelled"]
            },
            "created_at": {
                "bsonType": "date"
            }
        }
    }
}

# Apply validation to an existing collection or create a new one
if "appointments" in db.list_collection_names():
    db.command({
        "collMod": "appointments",
        "validator": appointment_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })
else:
    db.create_collection(
        "appointments",
        validator=appointment_validator,
        validationLevel="strict",
        validationAction="error"
    )

# Select appointments collection
appointments_collection = db["appointments"]

# Create a unique index on appointment_id
appointments_collection.create_index(
    "appointment_id",
    unique=True
)


# Select medical history collection
# MongoDB Schema Validation for Medical History

medical_history_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "history_id",
            "patient_id",
            "patient_name",
            "diagnosis",
            "allergies",
            "medications",
            "notes",
            "recorded_at"
        ],
        "properties": {
            "history_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_name": {
                "bsonType": "string",
                "minLength": 1
            },
            "diagnosis": {
                "bsonType": "string",
                "minLength": 1
            },
            "allergies": {
                "bsonType": "string",
                "minLength": 1
            },
            "medications": {
                "bsonType": "string",
                "minLength": 1
            },
            "notes": {
                "bsonType": "string",
                "minLength": 1
            },
            "recorded_at": {
                "bsonType": "date"
            }
        }
    }
}

# Apply validation to the medical_history collection
if "medical_history" in db.list_collection_names():
    db.command({
        "collMod": "medical_history",
        "validator": medical_history_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })
else:
    db.create_collection(
        "medical_history",
        validator=medical_history_validator,
        validationLevel="strict",
        validationAction="error"
    )

# Select medical history collection
medical_history_collection = db["medical_history"]

# Create a unique index on history_id
medical_history_collection.create_index(
    "history_id",
    unique=True
)

# Select medicines collection
# MongoDB Schema Validation for Medicines

medicines_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "medicine_id",
            "name",
            "category",
            "manufacturer",
            "price",
            "quantity",
            "reorder_level",
            "expiry_date",
            "created_at"
        ],
        "properties": {
            "medicine_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "name": {
                "bsonType": "string",
                "minLength": 1
            },
            "category": {
                "bsonType": "string",
                "minLength": 1
            },
            "manufacturer": {
                "bsonType": "string",
                "minLength": 1
            },
            "price": {
                "bsonType": ["double", "int", "long", "decimal"],
                "minimum": 0
            },
            "quantity": {
                "bsonType": ["int", "long"],
                "minimum": 0
            },
            "reorder_level": {
                "bsonType": ["int", "long"],
                "minimum": 0
            },
            "expiry_date": {
                "bsonType": "string",
                "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
            },
            "created_at": {
                "bsonType": "date"
            }
        }
    }
}

# Apply validation to the medicines collection
if "medicines" in db.list_collection_names():
    db.command({
        "collMod": "medicines",
        "validator": medicines_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })
else:
    db.create_collection(
        "medicines",
        validator=medicines_validator,
        validationLevel="strict",
        validationAction="error"
    )

# Select medicines collection
medicines_collection = db["medicines"]

# Create a unique index on medicine_id
medicines_collection.create_index(
    "medicine_id",
    unique=True
)

# MongoDB Schema Validation for Emergency Visits

emergency_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "emergency_id",
            "patient_id",
            "patient_name",
            "symptoms",
            "priority",
            "status",
            "visit_time",
            "discharge_time"
        ],
        "properties": {
            "emergency_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_name": {
                "bsonType": "string",
                "minLength": 1
            },
            "symptoms": {
                "bsonType": "string",
                "minLength": 1
            },
            "priority": {
                "bsonType": "string",
                "enum": [
                    "Low",
                    "Medium",
                    "High",
                    "Critical"
                ]
            },
            "status": {
                "bsonType": "string",
                "enum": [
                    "Under Treatment",
                    "Discharged"
                ]
            },
            "visit_time": {
                "bsonType": "date"
            },
            "discharge_time": {
                "bsonType": ["date", "null"]
            }
        }
    }
}

# Apply validation to the emergency_visits collection
if "emergency_visits" in db.list_collection_names():
    db.command({
        "collMod": "emergency_visits",
        "validator": emergency_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })
else:
    db.create_collection(
        "emergency_visits",
        validator=emergency_validator,
        validationLevel="strict",
        validationAction="error"
    )

# Select emergency visits collection
emergency_visits_collection = db["emergency_visits"]

# Prevent duplicate emergency IDs
emergency_visits_collection.create_index(
    "emergency_id",
    unique=True
)
# Select laboratory tests collection
# MongoDB Schema Validation for Laboratory Tests

lab_tests_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "test_id",
            "patient_id",
            "patient_name",
            "test_name",
            "doctor_name",
            "result",
            "status",
            "created_at"
        ],
        "properties": {
            "test_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_name": {
                "bsonType": "string",
                "minLength": 1
            },
            "test_name": {
                "bsonType": "string",
                "minLength": 1
            },
            "doctor_name": {
                "bsonType": "string",
                "minLength": 1
            },
            "result": {
                "bsonType": "string",
                "minLength": 1
            },
            "status": {
                "bsonType": "string",
                "enum": [
                    "Requested",
                    "In Progress",
                    "Completed",
                    "Cancelled"
                ]
            },
            "created_at": {
                "bsonType": "date"
            },
            "result_recorded_at": {
                "bsonType": "date"
            }
        }
    }
}

# Apply validation to the laboratory tests collection
if "lab_tests" in db.list_collection_names():
    db.command({
        "collMod": "lab_tests",
        "validator": lab_tests_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })
else:
    db.create_collection(
        "lab_tests",
        validator=lab_tests_validator,
        validationLevel="strict",
        validationAction="error"
    )

# Select laboratory tests collection
lab_tests_collection = db["lab_tests"]

# Create a unique index on test_id
lab_tests_collection.create_index(
    "test_id",
    unique=True
)

# MongoDB Schema Validation for Billing

bills_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "bill_id",
            "patient_id",
            "patient_name",
            "consultation_fee",
            "medicine_charges",
            "laboratory_charges",
            "bed_charges",
            "total_amount",
            "paid_amount",
            "balance",
            "payment_status",
            "created_at"
        ],
        "properties": {
            "bill_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_name": {
                "bsonType": "string",
                "minLength": 1
            },
            "consultation_fee": {
                "bsonType": ["double", "int", "long", "decimal"],
                "minimum": 0
            },
            "medicine_charges": {
                "bsonType": ["double", "int", "long", "decimal"],
                "minimum": 0
            },
            "laboratory_charges": {
                "bsonType": ["double", "int", "long", "decimal"],
                "minimum": 0
            },
            "bed_charges": {
                "bsonType": ["double", "int", "long", "decimal"],
                "minimum": 0
            },
            "total_amount": {
                "bsonType": ["double", "int", "long", "decimal"],
                "minimum": 0
            },
            "paid_amount": {
                "bsonType": ["double", "int", "long", "decimal"],
                "minimum": 0
            },
            "balance": {
                "bsonType": ["double", "int", "long", "decimal"],
                "minimum": 0
            },
            "payment_status": {
                "bsonType": "string",
                "enum": [
                    "Pending",
                    "Partially Paid",
                    "Paid"
                ]
            },
            "created_at": {
                "bsonType": "date"
            },
            "last_payment_date": {
                "bsonType": "date"
            }
        }
    }
}

# Apply validation to the bills collection
if "bills" in db.list_collection_names():
    db.command({
        "collMod": "bills",
        "validator": bills_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })
else:
    db.create_collection(
        "bills",
        validator=bills_validator,
        validationLevel="strict",
        validationAction="error"
    )

# Select bills collection
bills_collection = db["bills"]

# Prevent duplicate bill IDs
bills_collection.create_index(
    "bill_id",
    unique=True
)

# MongoDB Schema Validation for Patient Follow-Ups

follow_ups_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "follow_up_id",
            "patient_id",
            "patient_name",
            "follow_up_date",
            "reason",
            "status",
            "created_at"
        ],
        "properties": {
            "follow_up_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_name": {
                "bsonType": "string",
                "minLength": 1
            },
            "follow_up_date": {
                "bsonType": "date"
            },
            "reason": {
                "bsonType": "string",
                "minLength": 1
            },
            "status": {
                "bsonType": "string",
                "enum": [
                    "Scheduled",
                    "Completed",
                    "Cancelled",
                    "Missed"
                ]
            },
            "created_at": {
                "bsonType": "date"
            }
        }
    }
}

# Apply validation to the follow_ups collection
if "follow_ups" in db.list_collection_names():
    db.command({
        "collMod": "follow_ups",
        "validator": follow_ups_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })
else:
    db.create_collection(
        "follow_ups",
        validator=follow_ups_validator,
        validationLevel="strict",
        validationAction="error"
    )

# Select follow-ups collection
follow_ups_collection = db["follow_ups"]

# Prevent duplicate follow-up IDs
follow_ups_collection.create_index(
    "follow_up_id",
    unique=True
)

# MongoDB Schema Validation for Medical Equipment

equipment_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "equipment_id",
            "name",
            "department",
            "quantity",
            "status",
            "created_at"
        ],
        "properties": {
            "equipment_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "name": {
                "bsonType": "string",
                "minLength": 1
            },
            "department": {
                "bsonType": "string",
                "minLength": 1
            },
            "quantity": {
                "bsonType": ["int", "long"],
                "minimum": 1
            },
            "status": {
                "bsonType": "string",
                "enum": [
                    "Available",
                    "In Use",
                    "Under Maintenance"
                ]
            },
            "created_at": {
                "bsonType": "date"
            },
            "updated_at": {
                "bsonType": "date"
            }
        }
    }
}

# Apply validation to the medical_equipment collection
if "medical_equipment" in db.list_collection_names():
    db.command({
        "collMod": "medical_equipment",
        "validator": equipment_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })
else:
    db.create_collection(
        "medical_equipment",
        validator=equipment_validator,
        validationLevel="strict",
        validationAction="error"
    )

# Select medical equipment collection
equipment_collection = db["medical_equipment"]

# Prevent duplicate equipment IDs
equipment_collection.create_index(
    "equipment_id",
    unique=True
)

# MongoDB Schema Validation for Blood Bank

blood_bank_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "blood_group",
            "units",
            "updated_at"
        ],
        "properties": {
            "blood_group": {
                "bsonType": "string",
                "enum": [
                    "A+", "A-",
                    "B+", "B-",
                    "AB+", "AB-",
                    "O+", "O-"
                ]
            },
            "units": {
                "bsonType": ["int", "long"],
                "minimum": 0
            },
            "updated_at": {
                "bsonType": "date"
            }
        }
    }
}

# Apply validation to the blood_bank collection
if "blood_bank" in db.list_collection_names():
    db.command({
        "collMod": "blood_bank",
        "validator": blood_bank_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })
else:
    db.create_collection(
        "blood_bank",
        validator=blood_bank_validator,
        validationLevel="strict",
        validationAction="error"
    )

# Select blood bank collection
blood_bank_collection = db["blood_bank"]

# Prevent duplicate blood group records
blood_bank_collection.create_index(
    "blood_group",
    unique=True
)
# Create a unique index on test_id


# Select beds collection
# MongoDB Schema Validation for Hospital Beds

beds_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "bed_id",
            "ward",
            "bed_type",
            "status"
        ],
        "properties": {
            "bed_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "ward": {
                "bsonType": "string",
                "minLength": 1
            },
            "bed_type": {
                "bsonType": "string",
                "enum": ["General", "ICU", "Private"]
            },
            "status": {
                "bsonType": "string",
                "enum": ["Available", "Occupied"]
            }
        }
    }
}

# Apply validation to the beds collection
if "beds" in db.list_collection_names():
    db.command({
        "collMod": "beds",
        "validator": beds_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })
else:
    db.create_collection(
        "beds",
        validator=beds_validator,
        validationLevel="strict",
        validationAction="error"
    )

# Select beds collection
beds_collection = db["beds"]

# Prevent duplicate bed IDs
beds_collection.create_index(
    "bed_id",
    unique=True
)

# Select admissions collection
# MongoDB Schema Validation for Admissions

admissions_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "admission_id",
            "patient_id",
            "patient_name",
            "bed_id",
            "ward",
            "admission_date",
            "discharge_date",
            "status"
        ],
        "properties": {
            "admission_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "patient_name": {
                "bsonType": "string",
                "minLength": 1
            },
            "bed_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "ward": {
                "bsonType": "string",
                "minLength": 1
            },
            "admission_date": {
                "bsonType": "date"
            },
            "discharge_date": {
                "bsonType": ["date", "null"]
            },
            "status": {
                "bsonType": "string",
                "enum": ["Admitted", "Discharged"]
            }
        }
    }
}

# Apply validation to the admissions collection
if "admissions" in db.list_collection_names():
    db.command({
        "collMod": "admissions",
        "validator": admissions_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })
else:
    db.create_collection(
        "admissions",
        validator=admissions_validator,
        validationLevel="strict",
        validationAction="error"
    )

# Select admissions collection
admissions_collection = db["admissions"]

# Prevent duplicate admission IDs
admissions_collection.create_index(
    "admission_id",
    unique=True
)
# Create a unique index on patient_id
patients_collection.create_index(
    "patient_id",
    unique=True
)
# Select doctors collection
# MongoDB Schema Validation for Doctors

doctor_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "doctor_id",
            "name",
            "specialization",
            "department",
            "phone",
            "experience",
            "available"
        ],
        "properties": {
            "doctor_id": {
                "bsonType": "string",
                "minLength": 1
            },
            "name": {
                "bsonType": "string",
                "minLength": 1
            },
            "specialization": {
                "bsonType": "string",
                "minLength": 1
            },
            "department": {
                "bsonType": "string",
                "minLength": 1
            },
            "phone": {
                "bsonType": "string",
                "minLength": 1
            },
            "experience": {
                "bsonType": ["int", "long"],
                "minimum": 0,
                "maximum": 80
            },
            "available": {
                "bsonType": "bool"
            }
        }
    }
}

# Apply validation to an existing collection or create a new one
if "doctors" in db.list_collection_names():
    db.command({
        "collMod": "doctors",
        "validator": doctor_validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })
else:
    db.create_collection(
        "doctors",
        validator=doctor_validator,
        validationLevel="strict",
        validationAction="error"
    )

# Select doctors collection
# MongoDB Schema Validation for Doctors



# Select doctors collection
doctors_collection = db["doctors"]

# Create a unique index on doctor_id
doctors_collection.create_index(
    "doctor_id",
    unique=True
)
# Test connection
try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")

except Exception as e:
    print("MongoDB connection failed:", e)