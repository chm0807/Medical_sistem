from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(length=100), nullable=False)
    last_name = Column(String(length=100), nullable=False)
    specialization = Column(String(length=100), nullable=False)
    phone = Column(String(length=15), nullable=False)
    address = Column(String(length=255), nullable=False)
    email = Column(String(length=100), unique=True, nullable=False)
    medical_appointments = relationship("MedicalAppointment", back_populates="doctor", cascade="all, delete-orphan")

class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(length=100), nullable=False)
    last_name = Column(String(length=100), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    phone = Column(String(length=15), nullable=False)
    address = Column(String(length=255), nullable=False)
    email = Column(String(length=100), unique=True, nullable=False)
    medical_appointments = relationship("MedicalAppointment", back_populates="patient", cascade="all, delete-orphan")

class MedicalAppointment(Base):
    __tablename__ = "medical_appointments"

    appointment_id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    appointment_time = Column(String(length=5), nullable=False)
    consultation_type = Column(String(length=100), nullable=False)
    doctor = relationship("Doctor", back_populates="medical_appointments")
    patient = relationship("Patient", back_populates="medical_appointments")

class Medication(Base):
    __tablename__ = "medications"

    medication_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100), nullable=False)
    description = Column(String(length=255), nullable=True)

class Prescription(Base):
    __tablename__ = "prescriptions"

    prescription_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    prescription_date = Column(DateTime, nullable=False)
    notes = Column(String(length=255), nullable=True)
