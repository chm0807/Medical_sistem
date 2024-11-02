from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    phone: str
    address: str
    email: EmailStr

class DoctorCreate(DoctorBase):
    pass

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: datetime
    phone: str
    address: str
    email: EmailStr

class PatientCreate(PatientBase):
    pass

class MedicalAppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    appointment_time: str
    consultation_type: str


class MedicalAppointmentCreate(MedicalAppointmentBase):
    pass

class MedicationBase(BaseModel):
    name: str
    description: Optional[str] = None

class MedicationCreate(MedicationBase):
    pass

class PrescriptionBase(BaseModel):
    patient_id: int
    doctor_id: int
    prescription_date: datetime
    notes: Optional[str] = None

class PrescriptionCreate(PrescriptionBase):
    pass
