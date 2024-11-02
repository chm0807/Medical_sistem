from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import Doctor, Patient, MedicalAppointment, Prescription, Medication
from app.schemas import DoctorCreate, PatientCreate, MedicalAppointmentCreate, PrescriptionCreate, MedicationCreate
from app.database import get_db
from datetime import timedelta

router = APIRouter()

def get_doctor_or_404(db: Session, doctor_id: int):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

def get_patient_or_404(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

def get_medical_appointment_or_404(db: Session, appointment_id: int):
    appointment = db.query(MedicalAppointment).filter(MedicalAppointment.appointment_id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

def get_medication_or_404(db: Session, medication_id: int):
    medication = db.query(Medication).filter(Medication.medication_id == medication_id).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication

def format_appointment_time(appointment_time: timedelta) -> str:
    total_seconds = int(appointment_time.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{hours:02}:{minutes:02}"

@router.get("/doctors/", response_model=List[DoctorCreate])
def list_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).all()

@router.post("/doctors/", response_model=DoctorCreate)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = Doctor(**doctor.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

@router.delete("/doctors/{doctor_id}", response_model=dict)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = get_doctor_or_404(db, doctor_id)
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor deleted"}

@router.get("/patients/", response_model=List[PatientCreate])
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

@router.post("/patients/", response_model=PatientCreate)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

@router.delete("/patients/{patient_id}", response_model=dict)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient_or_404(db, patient_id)
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted"}

@router.get("/appointments/", response_model=List[MedicalAppointmentCreate])
def list_medical_appointments(db: Session = Depends(get_db)):
    appointments = db.query(MedicalAppointment).all()
    for appointment in appointments:
        appointment.appointment_time = format_appointment_time(appointment.appointment_time)
    return appointments

@router.post("/appointments/", response_model=MedicalAppointmentCreate)
def create_medical_appointment(appointment: MedicalAppointmentCreate, db: Session = Depends(get_db)):
    if not db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first():
        raise HTTPException(status_code=404, detail="Doctor not found")
    if not db.query(Patient).filter(Patient.patient_id == appointment.patient_id).first():
        raise HTTPException(status_code=404, detail="Patient not found")
    
    new_appointment = MedicalAppointment(**appointment.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

@router.delete("/appointments/{appointment_id}", response_model=dict)
def delete_medical_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = get_medical_appointment_or_404(db, appointment_id)
    db.delete(appointment)
    db.commit()
    return {"message": "Appointment deleted"}

@router.get("/medications/", response_model=List[MedicationCreate])
def list_medications(db: Session = Depends(get_db)):
    return db.query(Medication).all()

@router.post("/medications/", response_model=MedicationCreate)
def create_medication(medication: MedicationCreate, db: Session = Depends(get_db)):
    new_medication = Medication(**medication.dict())
    db.add(new_medication)
    db.commit()
    db.refresh(new_medication)
    return new_medication

@router.delete("/medications/{medication_id}", response_model=dict)
def delete_medication(medication_id: int, db: Session = Depends(get_db)):
    medication = get_medication_or_404(db, medication_id)
    db.delete(medication)
    db.commit()
    return {"message": "Medication deleted"}

@router.get("/prescriptions/", response_model=List[PrescriptionCreate])
def list_prescriptions(patient_id: int = None, doctor_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Prescription)
    
    if patient_id:
        query = query.filter(Prescription.patient_id == patient_id)
    if doctor_id:
        query = query.filter(Prescription.doctor_id == doctor_id)
        
    return query.all()

@router.post("/prescriptions/", response_model=PrescriptionCreate)
def create_prescription(prescription: PrescriptionCreate, db: Session = Depends(get_db)):
    if not db.query(Doctor).filter(Doctor.id == prescription.doctor_id).first():
        raise HTTPException(status_code=404, detail="Doctor not found")
    if not db.query(Patient).filter(Patient.patient_id == prescription.patient_id).first():
        raise HTTPException(status_code=404, detail="Patient not found")
    
    new_prescription = Prescription(**prescription.dict())
    db.add(new_prescription)
    db.commit()
    db.refresh(new_prescription)
    return new_prescription

@router.delete("/prescriptions/{prescription_id}", response_model=dict)
def delete_prescription(prescription_id: int, db: Session = Depends(get_db)):
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    db.delete(prescription)
    db.commit()
    return {"message": "Prescription deleted"}
