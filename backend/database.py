from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# ==============================
# DATABASE CONNECTION
# ==============================
DATABASE_URL = "sqlite:///./medintel_ai.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ==============================
# USER TABLE
# ==============================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    diagnoses = relationship("DiagnosisHistory", back_populates="user")
    chats = relationship("ChatHistory", back_populates="user")


# ==============================
# DIAGNOSIS HISTORY TABLE
# ==============================
class DiagnosisHistory(Base):
    __tablename__ = "diagnosis_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    dataset = Column(String)
    predicted_disease = Column(String)
    confidence = Column(Float)
    uncertainty = Column(Float)
    uncertainty_level = Column(String)

    uploaded_image = Column(String)
    gradcam_image = Column(String)
    pdf_report = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="diagnoses")


# ==============================
# CHAT HISTORY TABLE
# ==============================
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    disease_context = Column(String)
    user_query = Column(Text)
    bot_response = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chats")


# ==============================
# ADMIN ANALYTICS LOG TABLE
# ==============================
class AdminLog(Base):
    __tablename__ = "admin_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String)
    event_description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


# ==============================
# CREATE DATABASE TABLES
# ==============================
def init_db():
    Base.metadata.create_all(bind=engine)


# ==============================
# GET DB SESSION
# ==============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()