import streamlit as st
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Doctor, Patient, MedicalAppointment, Prescription, Medication

st.title("Medical Management System")
st.sidebar.header("Menu")

view_menu = st.sidebar.selectbox(
    "Select an option:",
    ["Doctors", "Patients", "Appointments", "Patient Prescriptions"]
)

add_menu = st.sidebar.selectbox(
    "Add New:",
    ["Add Doctor", "Add Patient", "Add Medication", "Create Prescription", "Create Appointment"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def format_timedelta(timedelta_value: timedelta) -> str:
    total_seconds = int(timedelta_value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    period = 'AM' if hours < 12 else 'PM'
    hours = hours % 12
    hours = hours if hours else 12
    return f"{hours:02}:{minutes:02} {period}"

def show_doctors():
    st.subheader("Doctors")
    with SessionLocal() as db:
        doctors = db.query(Doctor).all()
        if not doctors:
            st.write("No doctors found.")
        else:
            for doctor in doctors:
                st.write(f"{doctor.first_name} {doctor.last_name} - Specialization: {doctor.specialization}")

def show_patients():
    st.subheader("Patients")
    with SessionLocal() as db:
        patients = db.query(Patient).all()
        if not patients:
            st.write("No patients found.")
        else:
            for patient in patients:
                st.write(f"Name: {patient.first_name} {patient.last_name} - phone: {patient.phone} - Address: {patient.address} - Email: {patient.email}")

def show_appointments():
    st.subheader("Appointments")
    with SessionLocal() as db:
        appointments = (
            db.query(
                MedicalAppointment,
                Doctor.first_name.label('doctor_first_name'),
                Doctor.last_name.label('doctor_last_name'),
                Patient.first_name.label('patient_first_name'),
                Patient.last_name.label('patient_last_name')
            )
            .join(Doctor, MedicalAppointment.doctor_id == Doctor.id)
            .join(Patient, MedicalAppointment.patient_id == Patient.patient_id)
            .all()
        )
        if not appointments:
            st.write("No appointments found.")
        else:
            for appointment in appointments:
                date_str = appointment[0].appointment_date.strftime('%d %b %Y')
                time_str = format_timedelta(appointment[0].appointment_time) 
                st.write(f"{date_str} at {time_str} - Doctor: {appointment.doctor_first_name} {appointment.doctor_last_name} - Patient: {appointment.patient_first_name} {appointment.patient_last_name}")

def show_prescriptions():
    st.subheader("Prescriptions")
    patient_id = st.number_input("Patient ID", min_value=1, step=1)
    if st.button("Get Prescriptions"):
        with SessionLocal() as db:
            prescriptions = db.query(Prescription).filter(Prescription.patient_id == patient_id).all()
            if not prescriptions:
                st.write("No prescriptions found for this patient.")
            else:
                for prescription in prescriptions:
                    st.write(f"Date: {prescription.prescription_date} - Doctor ID: {prescription.doctor_id} - Notes: {prescription.notes}")

def add_doctor():
    st.subheader("Add Doctor")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    specialization = st.text_input("Specialization")
    phone = st.text_input("Phone")
    address = st.text_area("Address")
    email = st.text_input("Email")
    
    if st.button("Save Doctor"):
        with SessionLocal() as db:
            new_doctor = Doctor(
                first_name=first_name,
                last_name=last_name,
                specialization=specialization,
                phone=phone,
                address=address,
                email=email
            )
            db.add(new_doctor)
            db.commit()
            st.success("Doctor added successfully.")

def add_patient():
    st.subheader("Add Patient")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    birth_date = st.date_input("Birth Date", value=date.today())
    phone = st.text_input("Phone")
    address = st.text_area("Address")
    email = st.text_input("Email")
    
    if st.button("Save Patient"):
        with SessionLocal() as db:
            new_patient = Patient(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                phone=phone,
                address=address,
                email=email
            )
            db.add(new_patient)
            db.commit()
            st.success("Patient added successfully.")

def add_medication():
    st.subheader("Add Medication")
    name = st.text_input("Medication Name")
    description = st.text_area("Description")
    
    if st.button("Save Medication"):
        with SessionLocal() as db:
            new_medication = Medication(name=name, description=description)
            db.add(new_medication)
            db.commit()
            st.success("Medication added successfully.")

def create_prescription():
    st.subheader("Create Prescription")
    with SessionLocal() as db:
        patients = db.query(Patient).all()
        doctors = db.query(Doctor).all()
        medications = db.query(Medication).all()
        
        selected_patient_id = st.selectbox("Select Patient", [(patient.id, f"{patient.first_name} {patient.last_name}") for patient in patients])
        selected_doctor_id = st.selectbox("Select Doctor", [(doctor.id, f"{doctor.first_name} {doctor.last_name}") for doctor in doctors])
        selected_medication_id = st.selectbox("Select Medication", [(medication.id, medication.name) for medication in medications])
        
        prescription_date = st.date_input("Prescription Date")
        notes = st.text_area("Notes")
        
        if st.button("Save Prescription"):
            new_prescription = Prescription(
                patient_id=selected_patient_id,
                doctor_id=selected_doctor_id,
                prescription_date=prescription_date,
                notes=notes
            )
            with SessionLocal() as db:
                db.add(new_prescription)
                db.commit()
            st.success("Prescription created successfully.")

def create_appointment():
    st.subheader("Create Appointment")
    with SessionLocal() as db:
        patients = db.query(Patient).all()
        doctors = db.query(Doctor).all()
        
        selected_patient_id = st.selectbox("Select Patient", [(patient.id, f"{patient.first_name} {patient.last_name}") for patient in patients])
        selected_doctor_id = st.selectbox("Select Doctor", [(doctor.id, f"{doctor.first_name} {doctor.last_name}") for doctor in doctors])
        
        appointment_date = st.date_input("Appointment Date")
        appointment_time = st.time_input("Appointment Time")
        consultation_type = st.text_input("Consultation Type")
        
        if st.button("Create Appointment"):
            new_appointment = MedicalAppointment(
                patient_id=selected_patient_id,
                doctor_id=selected_doctor_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                consultation_type=consultation_type
            )
            with SessionLocal() as db:
                db.add(new_appointment)
                db.commit()
            st.success("Appointment created successfully!")

if view_menu == "Doctors":
    show_doctors()
elif view_menu == "Patients":
    show_patients()
elif view_menu == "Appointments":
    show_appointments()
elif view_menu == "Patient Prescriptions":
    show_prescriptions()

if add_menu == "Add Doctor":
    add_doctor()
elif add_menu == "Add Patient":
    add_patient()
elif add_menu == "Add Medication":
    add_medication()
elif add_menu == "Create Prescription":
    create_prescription()
elif add_menu == "Create Appointment":
    create_appointment()
